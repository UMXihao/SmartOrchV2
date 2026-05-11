# pip install datasets transformers matplotlib numpy tqdm

from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# =========================
# 配置
# =========================

# Arena-Hard v0.1 官方 question.jsonl
ARENA_HARD_URL = (
    "https://raw.githubusercontent.com/lmarena/arena-hard-auto/main/"
    "data/arena-hard-v0.1/question.jsonl"
)

TOKENIZER_NAME = "bert-base-uncased"

BATCH_SIZE = 1000
SAVE_PATH = "arena_hard_token_length_distribution.png"

# Arena-Hard 的用户输入字段是 prompt
TEXT_FIELD = "prompt"


# =========================
# 加载 Arena-Hard 数据和 tokenizer
# =========================

dataset = load_dataset(
    "json",
    data_files=ARENA_HARD_URL,
    split="train"
)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)


# =========================
# 构造待统计文本
# =========================

texts = []

for example in dataset:
    text = example[TEXT_FIELD]
    texts.append(text)


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

print("Dataset: Arena-Hard")
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

plot_lengths = lengths[lengths > 0]

bins = np.logspace(
    np.log10(plot_lengths.min()),
    np.log10(plot_lengths.max()),
    50
)

plt.figure(figsize=(9, 5))

plt.hist(
    plot_lengths,
    bins=bins,
    color="#BFD4FD",
    edgecolor="#3160A8",
    alpha=0.85
)

plt.xscale("log")

plt.xlabel("Token length")
plt.ylabel("Count")
plt.title("Arena-Hard Token Length Distribution")

plt.xticks(
    [1, 10, 100, 1000, 10000],
    ["1", "10", "100", "1K", "10K"]
)

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
