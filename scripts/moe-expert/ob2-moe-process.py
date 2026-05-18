import re
import csv
from pathlib import Path


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


if __name__ == "__main__":
    merge_moe_files(
        input_dir="test",                 # 26 个 txt 文件所在目录
        output_csv="moe_activation_test.csv"
    )
