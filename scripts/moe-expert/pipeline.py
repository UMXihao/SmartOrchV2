"""
start llama.cpp server
build/bin/llama-server -m ${model_path}

using llama-server to finish bench mark
"""

import requests
import time
from tqdm import tqdm
from datasets import load_dataset

import numpy as np
import re
import csv
from pathlib import Path
import pandas as pd

def top6(file_name, id):
# 读取 CSV
    df = pd.read_csv(file_name)

    # 找出所有 layer 列
    layer_cols = [col for col in df.columns if col.startswith("layer_")]

    # 每层取 top6 expert_id
    top6_experts = {}

    for layer in layer_cols:
        top6 = df.nlargest(6, layer)[["expert_id", layer]]
        # top6_experts[layer] = top6["expert_id"].tolist()
        top6_experts[layer] = sorted(top6["expert_id"].tolist())

    # 转成 DataFrame，方便查看和保存
    result = pd.DataFrame(top6_experts)
    # 保存结果
    result.to_csv("squad-request/top6_experts_request" + str(id) + ".csv", index=False)

def percentile(data, percentile):
    return float(np.percentile(data, percentile, method="linear"))

def extract_layer_id(filename: str) -> int:
    """
    从文件名中提取层编号。
    例如 decode_ffn_moe_argsort-1.txt -> 1
    """
    match = re.search(r"-(\d+)\.txt$", filename)
    if not match:
        raise ValueError(f"无法从文件名中提取层编号: {filename}")
    return int(match.group(1))


def read_counts(file_path: Path) -> list[int]:
    """
    读取单个 txt 文件中的 63 行激活次数。
    """
    with file_path.open("r", encoding="utf-8") as f:
        counts = [int(line.strip()) for line in f if line.strip()]

    if len(counts) != 63:
        raise ValueError(f"{file_path.name} 中有 {len(counts)} 行，不是 63 行")

    return counts

def merge_moe_files(input_dir: str, output_csv: str):
    input_path = Path(input_dir)

    files = sorted(
        input_path.glob("prefill_ffn_moe_argsort-*.txt"),
        key=lambda p: extract_layer_id(p.name)
    )

    if len(files) != 25:
        raise ValueError(f"找到 {len(files)} 个文件，不是 26 个")

    # layer_data[layer_id] = 该层的 64 个专家激活次数
    layer_data = {}

    for file in files:
        layer_id = extract_layer_id(file.name)
        layer_data[layer_id] = read_counts(file)

    layer_ids = sorted(layer_data.keys())

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        header = ["expert_id"] + [f"layer_{layer_id}" for layer_id in layer_ids]
        writer.writerow(header)

        for expert_id in range(63):
            row = [expert_id]
            for layer_id in layer_ids:
                row.append(layer_data[layer_id][expert_id])
            writer.writerow(row)

    print(f"已保存到: {output_csv}")

def delete_moe_files(input_dir: str):
    target_path = Path(input_dir)

    if not target_path.exists():
        print(f"目录不存在: {input_dir}")
        return

    if not target_path.is_dir():
        print(f"不是有效目录: {input_dir}")
        return

    pattern = "prefill_ffn_moe_argsort-*.txt"
    files = list(target_path.glob(pattern))

    if not files:
        print("没有找到匹配文件")
        return

    for file in files:
        try:
            file.unlink()
            print(f"已删除: {file}")
        except Exception as e:
            print(f"删除失败: {file}, 原因: {e}")

    print(f"完成，共删除 {len(files)} 个文件")

# def main():
url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

squad_val = load_dataset("squad", split="validation")

for i in tqdm(range(100)):
    # for i in tqdm(range(len(squad_val))):
    context = squad_val[i]["context"]
    question = squad_val[i]["question"]
    # 构造输入文本
    input_text = f"Context: {context}\nQuestion: {question}\nAnswer: "
    data = {"prompt": input_text, "n_predict": 1, "stop": "\n"}

    requests.post(url, headers=headers, json=data)

    # 整合prefill的采集文件
    moe_activation_output = "moe_activation_request" + str(i)
    merge_moe_files("/home/lili-5090/Sean/SmartOrchV2", moe_activation_output)

    # 融合完删除prefill的采集文件
    delete_moe_files("/home/lili-5090/Sean/SmartOrchV2")

    # top6 选择
    top6(moe_activation_output, i)

# if __name__ == "__main__":
#     main()
