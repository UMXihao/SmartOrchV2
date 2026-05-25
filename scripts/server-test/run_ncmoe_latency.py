#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逐个调整 llama-server 的 -ncmoe 参数，并测试模型在 SQuAD 上的推理精度。

默认执行：
  -ncmoe 8, 9, ..., 27
  每个配置启动一次 server -> 等待 /completion 可用 -> 跑精度测试 -> 保存结果 -> 关闭 server

使用示例：
  python run_ncmoe_eval.py \
    --server-bin ./build/bin/llama-server \
    --model models/deepseek-v2-lite-chat-q4_0.gguf \
    --num-samples 100

跑完整 SQuAD validation：
  python run_ncmoe_eval.py --full
"""

import argparse
import csv
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from datasets import load_dataset
import evaluate
from tqdm import tqdm

import numpy as np
HEADERS = {"Content-Type": "application/json"}


def build_server_cmd(args: argparse.Namespace, ncmoe: int) -> List[str]:
    """构造 llama-server 启动命令。"""
    cmd = [
        args.server_bin,
        "-m",
        args.model,
        "-ncmoe",
        str(ncmoe),
    ]

    # 默认保持你的原始启动命令，不额外向 llama-server 传 --port。
    # 如果你确实需要给 server 显式传端口，请加 --pass-port-to-server。
    if args.pass_port_to_server and args.port is not None:
        cmd += ["--port", str(args.port)]

    if args.extra_server_args:
        cmd += args.extra_server_args

    return cmd


def start_server(cmd: List[str], log_path: Path) -> Tuple[subprocess.Popen, object]:
    """启动 server，并把 stdout/stderr 写入日志文件。"""
    log_file = open(log_path, "w", encoding="utf-8")

    # Linux/macOS：创建新进程组，方便后面杀掉 server 及其子进程。
    if os.name != "nt":
        proc = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            preexec_fn=os.setsid,
        )
    else:
        proc = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

    return proc, log_file


def stop_server(proc: Optional[subprocess.Popen], log_file: Optional[object] = None) -> None:
    """尽量优雅地关闭 server。"""
    if proc is None:
        return

    if proc.poll() is None:
        try:
            if os.name != "nt":
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            else:
                proc.terminate()
            proc.wait(timeout=20)
        except Exception:
            try:
                if os.name != "nt":
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                else:
                    proc.kill()
                proc.wait(timeout=10)
            except Exception:
                pass

    if log_file is not None:
        try:
            log_file.flush()
            log_file.close()
        except Exception:
            pass


def wait_until_ready(
    base_url: str,
    proc: subprocess.Popen,
    startup_timeout: int,
    poll_interval: float = 2.0,
) -> None:
    """
    等待 server 可用。
    这里直接请求 /completion，避免不同 llama-server 版本 /health 接口不一致。
    """
    deadline = time.time() + startup_timeout
    url = f"{base_url}/completion"
    last_error = ""

    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"server 进程提前退出，returncode={proc.returncode}")

        try:
            payload = {
                "prompt": "Hello\nAnswer:",
                "n_predict": 1,
                "stop": "\n",
            }
            resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
            if resp.status_code == 200:
                return
            last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as exc:
            last_error = repr(exc)

        time.sleep(poll_interval)

    raise TimeoutError(f"server 在 {startup_timeout}s 内未就绪，最后错误：{last_error}")


def post_completion_with_retry(
    url: str,
    payload: Dict,
    request_timeout: int,
    retries: int,
    retry_sleep: float,
):
    """请求 /completion，失败时重试。返回生成文本和单条耗时。"""
    last_error = None

    for attempt in range(retries + 1):
        start = time.time()
        try:
            response = requests.post(
                url,
                headers=HEADERS,
                json=payload,
                timeout=request_timeout,
            )
            response.raise_for_status()
            latency = time.time() - start
            # content = response.json().get("content", "")
            return response, latency
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(retry_sleep)

    raise RuntimeError(f"/completion 请求失败，已重试 {retries} 次：{last_error}")

def trimmed_mean_np(arr):
    arr = np.asarray(arr)

    if arr.size <= 6:
        raise ValueError("数组长度必须大于 6")

    sorted_arr = np.sort(arr)
    trimmed = sorted_arr[3:-3]

    return np.mean(trimmed)

def percentile(data, percentile):
    return float(np.percentile(data, percentile, method="linear"))


def evaluate_squad_for_current_server(
    base_url: str,
    squad_val,
    metric,
    num_samples: int,
    n_predict: int,
    request_timeout: int,
    retries: int,
    save_predictions_path: Path,
) -> Dict:
    """对当前已启动的 server 执行 SQuAD 精度测试。"""
    completion_url = f"{base_url}/completion"

    predictions = []
    references = []
    prefill = []
    decode = []

    for i in tqdm(range(num_samples), desc="SQuAD eval", ncols=100):
        context = squad_val[i]["context"]
        question = squad_val[i]["question"]
        answers = squad_val[i]["answers"]
        question_id = squad_val[i]["id"]

        input_text = f"Context: {context}\nQuestion: {question}\nAnswer: "
        payload = {
            "prompt": input_text,
            "n_predict": n_predict,
            "stop": "\n",
        }

        response = []
        try:
            response, latency = post_completion_with_retry(
                completion_url,
                payload,
                request_timeout=request_timeout,
                retries=retries,
                retry_sleep=2.0,
            )
        except Exception as exc:
            # 为了不中断整组评测，失败样本记为空答案，同时记录错误。
            response = ""

        references.append({"answers": answers, "id": question_id})
        predictions.append({"prediction_text": response.json().get("content"), "id": question_id})
        prompt_ms = response.json().get("timings").get("prompt_ms")
        predicted_per_token_ms = response.json().get("timings").get("predicted_per_token_ms")
        prefill.append(prompt_ms)
        decode.append(predicted_per_token_ms)

    result = metric.compute(predictions=predictions, references=references)

    total_tokens_or_samples = len(predictions)

    detail = {
        "metrics": result,
        "num_samples": total_tokens_or_samples,
        "ttft": trimmed_mean_np(prefill),
        "tpot": trimmed_mean_np(decode),
        "predictions": predictions,
        "references": references,
    }

    with open(save_predictions_path, "w", encoding="utf-8") as f:
        json.dump(detail, f, ensure_ascii=False, indent=2)

    return {
        "exact_match": result.get("exact_match"),
        "f1": result.get("f1"),
        "num_samples": total_tokens_or_samples,
        "ttft": trimmed_mean_np(prefill),
        "tpot": trimmed_mean_np(decode),
    }


def append_jsonl(path: Path, row: Dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: List[Dict]) -> None:
    fieldnames = [
        "ncmoe",
        "status",
        "exact_match",
        "f1",
        "num_samples",
        "ttft",
        "tpot",
        "elapsed_s",
        "error",
        "log_path",
        "prediction_path",
    ]

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Loop over -ncmoe values and evaluate llama-server on SQuAD."
    )

    parser.add_argument("--server-bin", default="/home/lili-5090/Sean/llama.cpp/build/bin/llama-server")
    parser.add_argument("--model", default="/home/lili-5090/Sean/llama.cpp/models/deepseek-v2-lite-chat-q4_0.gguf")

    parser.add_argument("--ncmoe-start", type=int, default=1)
    parser.add_argument("--ncmoe-end", type=int, default=27)

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument(
        "--pass-port-to-server",
        action="store_true",
        help="默认不把 --port 传给 llama-server；需要显式指定 server 端口时再开启。",
    )

    parser.add_argument("--num-samples", type=int, default=10)
    parser.add_argument(
        "--full",
        action="store_true",
        help="测试完整 SQuAD validation；设置后忽略 --num-samples。",
    )

    parser.add_argument("--n-predict", type=int, default=128)
    parser.add_argument("--startup-timeout", type=int, default=600)
    parser.add_argument("--request-timeout", type=int, default=120)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--cooldown", type=float, default=3.0)

    parser.add_argument("--output-dir", default="ncmoe_latency_results")

    # 例如需要传 llama-server 其他参数：
    # --extra-server-args --ctx-size 4096 --threads 16
    parser.add_argument(
        "--extra-server-args",
        nargs=argparse.REMAINDER,
        default=[],
        help="追加传给 llama-server 的参数；必须放在命令最后。",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    output_dir = Path(args.output_dir)
    log_dir = output_dir / "logs"
    pred_dir = output_dir / "predictions"
    log_dir.mkdir(parents=True, exist_ok=True)
    pred_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / "results.jsonl"
    csv_path = output_dir / "results.csv"

    if jsonl_path.exists():
        jsonl_path.unlink()

    base_url = f"http://{args.host}:{args.port}"

    print("Loading SQuAD validation dataset...")
    squad_val = load_dataset("squad", split="validation")
    metric = evaluate.load("squad")

    num_samples = len(squad_val) if args.full else min(args.num_samples, len(squad_val))
    print(f"num_samples = {num_samples}")
    print(f"base_url = {base_url}")
    print(f"output_dir = {output_dir.resolve()}")

    all_rows: List[Dict] = []

    for ncmoe in range(args.ncmoe_start, args.ncmoe_end + 1):
        print("\n" + "=" * 80)
        print(f"Start evaluating -ncmoe {ncmoe}")
        print("=" * 80)

        log_path = log_dir / f"server_ncmoe_{ncmoe}.log"
        pred_path = pred_dir / f"predictions_ncmoe_{ncmoe}.json"
        cmd = build_server_cmd(args, ncmoe)

        print("Server command:")
        print(" ".join(cmd))

        proc = None
        log_file = None
        started_at = time.time()

        row: Dict = {
            "ncmoe": ncmoe,
            "status": "failed",
            "exact_match": None,
            "f1": None,
            "num_samples": num_samples,
            "ttft": None,
            "tpot": None,
            "elapsed_s": None,
            "error": "",
            "log_path": str(log_path),
            "prediction_path": str(pred_path),
        }

        try:
            proc, log_file = start_server(cmd, log_path)
            wait_until_ready(
                base_url=base_url,
                proc=proc,
                startup_timeout=args.startup_timeout,
            )

            metrics = evaluate_squad_for_current_server(
                base_url=base_url,
                squad_val=squad_val,
                metric=metric,
                num_samples=num_samples,
                n_predict=args.n_predict,
                request_timeout=args.request_timeout,
                retries=args.retries,
                save_predictions_path=pred_path,
            )

            row.update(metrics)
            row["status"] = "ok"

            print(
                f"[ncmoe={ncmoe}] "
                f"EM={row['exact_match']:.4f}, "
                f"F1={row['f1']:.4f}, "
                f"tpot={row['tpot']}"
            )

        except KeyboardInterrupt:
            row["error"] = "KeyboardInterrupt"
            row["elapsed_s"] = time.time() - started_at
            append_jsonl(jsonl_path, row)
            all_rows.append(row)
            write_csv(csv_path, all_rows)
            print("收到 KeyboardInterrupt，正在关闭当前 server...")
            stop_server(proc, log_file)
            return 130

        except Exception as exc:
            row["error"] = repr(exc)
            print(f"[ncmoe={ncmoe}] failed: {row['error']}", file=sys.stderr)

        finally:
            row["elapsed_s"] = time.time() - started_at
            stop_server(proc, log_file)
            append_jsonl(jsonl_path, row)
            all_rows.append(row)
            write_csv(csv_path, all_rows)

            if args.cooldown > 0:
                time.sleep(args.cooldown)

    print("\n全部评测完成。")
    print(f"CSV 汇总：{csv_path}")
    print(f"JSONL 汇总：{jsonl_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
