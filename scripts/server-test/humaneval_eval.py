#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HumanEval 精度评估脚本（llama.cpp /completion 端点）

功能：
- 读取 bigcode/humanevalpack Python 测试集
- 调用本地 llama-server /completion 进行代码生成
- 使用 evaluate 的 code_eval 计算 pass@k

注意：该指标会在本机执行模型生成代码，请在隔离环境里运行！
"""

import os
import json
import time
import argparse
from typing import List, Dict, Any
import requests
from tqdm import tqdm
from datasets import load_dataset
import evaluate

# 默认服务端配置
DEFAULT_URL = "http://127.0.0.1:8080/completion"
DEFAULT_HEADERS = {"Content-Type": "application/json"}

# 按 BigCode 的评测习惯，为 Python 设定 Stop Words，避免模型生成多余定义/测试等噪声
# 参考 bigcode-evaluation-harness 的 humanevalpack.py：LANGUAGE_TO_STOP_WORDS['python']
# https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/bigcode_eval/tasks/humanevalpack.py
PY_STOP_WORDS = ["\nclass", "\ndef", "\n#", "\n@", "\nprint", "\nif", "\nassert"]

def parse_args():
    parser = argparse.ArgumentParser(description="HumanEval 精度评估（llama.cpp /completion）")
    parser.add_argument("--url", type=str, default=DEFAULT_URL, help="llama-server /completion 地址")
    parser.add_argument("--n-predict", type=int, default=256, help="最大生成 token 数")
    parser.add_argument("--temperature", type=float, default=0.2, help="采样温度")
    parser.add_argument("--top-p", type=float, default=0.95, help="top-p")
    parser.add_argument("--num-tasks", type=int, default=100, help="评估题目数量（从开头截取）")
    parser.add_argument("--num-samples-per-task", type=int, default=1, help="每题生成样本数（>1 才能评 pass@k>1）")
    parser.add_argument("--k", type=int, nargs="+", default=[1], help="评估的 k 值列表，例如 --k 1 10 100")
    parser.add_argument("--timeout", type=float, default=300.0, help="HTTP 请求超时（秒）")
    parser.add_argument("--save-jsonl", type=str, default="humaneval_predictions.jsonl",
                        help="保存原始生成到 JSONL 文件（含 task_id 与 completion）")
    return parser.parse_args()


def call_llama_completion(url: str, headers: Dict[str, str], prompt: str,
                          n_predict: int, temperature: float, top_p: float,
                          timeout: float) -> str:
    """调用 llama-server 的 /completion 端点获取补全文本。"""
    payload = {
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": temperature,
        "top_p": top_p,
        # 传入一组 stop words，减少生成跑偏的几率（尤其是产生 class、def、assert 等）
        # https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/bigcode_eval/tasks/humanevalpack.py
        "stop": PY_STOP_WORDS,
        # 关闭流式，确保一次返回完整 JSON
        "stream": False,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    # 不同版本的 llama-server 可能返回 "content" 或 OpenAI 风格的 "choices[0]['text']"；两者都兼容。
    # https://gitee.com/canleng/llama.cpp/blob/master/examples/server/README.md
    if isinstance(data, dict):
        if "content" in data and isinstance(data["content"], str):
            return data["content"]
        if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
            choice = data["choices"][0]
            if isinstance(choice, dict) and "text" in choice:
                return choice["text"]

    # 兜底：将整个 JSON 序列化为字符串（不推荐，但防止结构异常）
    return json.dumps(data, ensure_ascii=False)


def post_process_completion(text: str) -> str:
    """
    轻量后处理：
    - 去除代码块围栏 ```python / ```
    - 去掉前后空白
    """
    t = text.strip()
    # 移除 Markdown 代码块
    if t.startswith("```"):
        t = t.lstrip("`")
        # 去掉可能的语言标签
        if t.lower().startswith("python"):
            t = t[len("python"):].lstrip()
        if "```" in t:
            t = t[:t.rfind("```")].strip()
    return t.strip()


def main():
    args = parse_args()

    # 1) 加载数据集（Python split 与原始 HumanEval Python 等价；字段包含 prompt/test/entry_point 等）[1](https://huggingface.co/datasets/bigcode/humanevalpack)
    ds = load_dataset("bigcode/humanevalpack", "python")["test"]

    # 只取前 num_tasks 条
    num_tasks = min(args.num_tasks, len(ds))
    tasks = [ds[i] for i in range(num_tasks)]

    # 2) 组装 references（测试用例脚本字符串）
    references: List[str] = [ex["test"] for ex in tasks]

    # 3) 为每个任务收集若干候选（predictions 的格式：List[List[str]]，每个子列表是该任务的多个候选）
    predictions: List[List[str]] = []

    # 保存原始生成，便于复查
    jsonl_fp = open(args.save_jsonl, "w", encoding="utf-8")

    start = time.time()
    for ex in tqdm(tasks, desc=f"Generating ({num_tasks} tasks x {args.num_samples_per_task} samples)"):
        prompt: str = ex["prompt"]  # HumanEval 的题目前缀（含函数签名与文档）[1](https://huggingface.co/datasets/bigcode/humanevalpack)
        task_id: str = ex["task_id"]

        candidates_for_task: List[str] = []
        for s in range(args.num_samples_per_task):
            completion = call_llama_completion(
                url=args.url,
                headers=DEFAULT_HEADERS,
                prompt=prompt,
                n_predict=args.n_predict,
                temperature=args.temperature,
                top_p=args.top_p,
                timeout=args.timeout
            )

            completion = post_process_completion(completion)

            # 关键：将 prompt 与模型生成拼接，形成“可运行的候选解决方案”。
            # code_eval 在评估时就是把候选 + 测试代码拼接后执行。[3](https://github.com/huggingface/evaluate/blob/main/metrics/code_eval/code_eval.py)
            candidate_program = prompt + "\n" + completion

            candidates_for_task.append(candidate_program)

            # 记录到 JSONL
            jsonl_fp.write(json.dumps({
                "task_id": task_id,
                "sample_id": s,
                "prompt_prefix": prompt,
                "completion": completion
            }, ensure_ascii=False) + "\n")

        predictions.append(candidates_for_task)

    jsonl_fp.close()
    gen_secs = time.time() - start

    # 4) 计算 pass@k（需要设置 HF_ALLOW_CODE_EVAL=1；脚本内也强制设置一次）
    # https://github.com/huggingface/evaluate/blob/main/metrics/code_eval/code_eval.py
    os.environ["HF_ALLOW_CODE_EVAL"] = "1"

    code_eval = evaluate.load("code_eval")  # HumanEval 评测指标（会执行代码，注意安全）
    pass_at_k, results = code_eval.compute(
        references=references,
        predictions=predictions,
        k=args.k,
        timeout=20.0 # 可根据机器性能调整并发与超时（默认超时 3s 在官方实现里；此处沿用 evaluate 内部默认）
    )

    print("\n================ Evaluation Summary ================\n")
    print(f"Tasks evaluated        : {num_tasks}")
    print(f"Samples per task       : {args.num_samples_per_task}")
    print(f"Generation time (s)    : {gen_secs:.2f}")
    print(f"Pass@k                 : {pass_at_k}")  # 形如 {'pass@1': 0.XX, 'pass@10': 0.YY}
    print(f"Raw generations saved  : {args.save_jsonl}")
    print("\n===================================================\n")


if __name__ == "__main__":
    main()

# 只跑 100 道题、每题一个样本
# python humaneval_eval.py --num-tasks 100 --num-samples-per-task 1 --k 1  --n-predict 256
'''
Tasks evaluated        : 100
Samples per task       : 1
Generation time (s)    : 4627.86
Pass@k                 : {'pass@1': 0.01}
Raw generations saved  : humaneval_predictions.jsonl
'''

# python humaneval_eval.py --num-tasks 100 --num-samples-per-task 1 --k 1  --n-predict 256 --temperature 0.2 --top-p 0.95

# python humaneval_eval.py --num-tasks 164 --num-samples-per-task 10 --k 1 10

