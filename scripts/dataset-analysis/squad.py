# pip install datasets transformers matplotlib numpy tqdm

from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# =========================
# 配置
# =========================

DATASET_NAME = "squad_v2"
SPLIT = "train"          # 可改为 "validation"
TOKENIZER_NAME = "bert-base-uncased"

# 统计对象：
# "question"：只统计问题长度
# "context"：只统计文章上下文长度
# "input"：统计 question + context 的总输入长度，更适合大模型 QA 输入
TEXT_FIELD = "input"

BATCH_SIZE = 1000
SAVE_PATH = "squad_v2_token_length_distribution.png"


# =========================
# 加载数据和 tokenizer
# =========================

dataset = load_dataset(DATASET_NAME, split=SPLIT)
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)


# =========================
# 构造待统计文本
# =========================

def build_text(example):
    if TEXT_FIELD == "question":
        return example["question"]
    elif TEXT_FIELD == "context":
        return example["context"]
    elif TEXT_FIELD == "input":
        return example["question"] + "\n\n" + example["context"]
    else:
        raise ValueError("TEXT_FIELD must be one of: question, context, input")


texts = [build_text(x) for x in dataset]


# =========================
# 分批统计 token 长度
# =========================

lengths = []

for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Tokenizing"):
    batch_texts = texts[i:i + BATCH_SIZE]

    encoded = tokenizer(
        batch_texts,
        add_special_tokens=False,
        truncation=False
    )

    batch_lengths = [len(ids) for ids in encoded["input_ids"]]
    lengths.extend(batch_lengths)

lengths = np.array(lengths)


# =========================
# 统计指标
# =========================

median_len = np.percentile(lengths, 50)
p90_len = np.percentile(lengths, 90)
p99_len = np.percentile(lengths, 99)

print(f"Dataset: {DATASET_NAME}")
print(f"Split: {SPLIT}")
print(f"Tokenizer: {TOKENIZER_NAME}")
print(f"Text field: {TEXT_FIELD}")
print(f"Samples: {len(lengths)}")
print(f"Min length: {lengths.min():.0f}")
print(f"Max length: {lengths.max():.0f}")
print(f"Mean length: {lengths.mean():.2f}")
print(f"Median: {median_len:.1f}")
print(f"P90: {p90_len:.1f}")
print(f"P99: {p99_len:.1f}")


# =========================
# 绘图
# =========================

# log-scale 横轴不能包含 0
plot_lengths = lengths[lengths > 0]

# 按 log 空间分桶，类似示例图
bins = np.logspace(
    np.log10(plot_lengths.min()),
    np.log10(plot_lengths.max()),
    50
)

plt.figure(figsize=(9, 5))

plt.hist(
    plot_lengths,
    bins=bins,
    edgecolor="black",
    alpha=0.75
)

plt.xscale("log")

plt.xlabel("Token length")
plt.ylabel("Count")
plt.title(f"SQuAD 2.0 Token Length Distribution ({TEXT_FIELD})")

# x 轴刻度可按需要调整
plt.xticks(
    [1, 10, 100, 1000, 10000],
    ["1", "10", "100", "1K", "10K"]
)

# 统计信息框
stats_text = (
    f"Median: {median_len:.1f}\n"
    f"P90: {p90_len:.1f}\n"
    f"P99: {p99_len:.1f}"
)

plt.text(
    0.68,
    0.72,
    stats_text,
    transform=plt.gca().transAxes,
    fontsize=12,
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=0.8
    )
)

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(SAVE_PATH, dpi=300)
plt.show()

print(f"Figure saved to: {SAVE_PATH}")