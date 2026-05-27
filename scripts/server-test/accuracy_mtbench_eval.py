import requests
from tqdm import tqdm
from datasets import load_dataset
import evaluate
import time

import json
from pathlib import Path
from typing import Any


def read_json_or_jsonl(file_path: str | Path) -> list[Any]:
    """
    读取 .json 或 .jsonl 文件。

    .json:
        文件整体是一个 JSON 对象或数组。

    .jsonl:
        每一行是一个独立 JSON 对象。
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    suffix = path.suffix.lower()

    if suffix == ".jsonl":
        data = []

        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()

                # 跳过空行
                if not line:
                    continue

                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"第 {line_no} 行不是合法 JSON: {e}"
                    ) from e

        return data

    elif suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            obj = json.load(f)

        # 统一返回 list，方便后续处理
        if isinstance(obj, list):
            return obj
        return [obj]

    else:
        raise ValueError(
            f"不支持的文件类型: {suffix}，请使用 .json 或 .jsonl 文件"
        )

# 加载 ROUGE 评测指标
rouge = evaluate.load("rouge")

predictions = []
references = []

source = read_json_or_jsonl("my-local-model_mtbench_answer.jsonl")

judge = read_json_or_jsonl("mtbench_judge_details.jsonl")

for i in tqdm(range(10)):
    turns = source[i]["choices"][0]["turns"]
    predict = "".join(turns)
    reference_summary = judge[i]["judge_output"]

    predictions.append(predict)
    references.append(reference_summary.strip())

# 计算 ROUGE
results = rouge.compute(
    predictions=predictions,
    references=references,
    use_stemmer=True
)

print("\n===== 推理精度评测结果 =====")
for k, v in results.items():
    print(f"{k}: {v:.4f}")
