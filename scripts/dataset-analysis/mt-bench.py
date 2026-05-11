# pip install datasets transformers matplotlib numpy tqdm

from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# =========================
# 配置
# =========================

# 官方 FastChat MT-Bench question.jsonl
MT_BENCH_URL = (
    "https://raw.githubusercontent.com/lm-sys/FastChat/main/"
    "fastchat/llm_judge/data/mt_bench/question.jsonl"
)

TOKENIZER_NAME = "bert-base-uncased"
BATCH_SIZE = 1000
SAVE_PATH = "mt_bench_token_length_distribution.png"

# 统计方式：
# "conversation"：每条 MT-Bench 样本的多轮 turns 拼接后统计总长度
# "turn"：把每一轮用户问题单独作为一个样本统计
STAT_MODE = "conversation"


# =========================
# 加载 MT-Bench 数据和 tokenizer
# =========================

dataset = load_dataset(
    "json",
    data_files=MT_BENCH_URL,
    split="validation"
)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)


# =========================
# 构造待统计文本
# =========================

texts = []

for example in dataset:
    turns = example["turns"]

    if STAT_MODE == "conversation":
        # 将多轮用户问题拼接为一个完整样本
        text = "\n\n".join(
            [f"User turn {i + 1}: {turn}" for i, turn in enumerate(turns)]
        )
        texts.append(text)

    elif STAT_MODE == "turn":
        # 每一轮用户问题单独统计
        texts.extend(turns)

    else:
        raise ValueError("STAT_MODE must be one of: conversation, turn")


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

print("Dataset: MT-Bench")
print(f"Tokenizer: {TOKENIZER_NAME}")
print(f"Stat mode: {STAT_MODE}")
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
plt.title(f"MT-Bench Token Length Distribution ({STAT_MODE})")

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
