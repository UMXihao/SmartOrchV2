import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# =========================
# 1. 读取数据
# =========================
csv_file = "multi_request_top6_overlap.csv"
df = pd.read_csv(csv_file)

# 兼容 layer 是整数或 "layer_0" 这种格式
def parse_layer(x):
    if isinstance(x, str) and "_" in x:
        return int(x.split("_")[-1])
    return int(x)

df["layer_id"] = df["layer"].apply(parse_layer)
df["overlap_rate"] = df["overlap_rate"].astype(float)

# =========================
# 2. 统计信息
# =========================
total = len(df)
gt_08 = (df["overlap_rate"] > 0.8).sum()
gt_05 = (df["overlap_rate"] > 0.5).sum()
eq_00 = (df["overlap_rate"] == 0.0).sum()

print(f"> 0.8: {gt_08}/{total}")
print(f"> 0.5: {gt_05}/{total}")
print(f"= 0.0: {eq_00}/{total}")

# =========================
# 3. 论文风格设置
# =========================
mpl.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.linewidth": 0.8,
})

# =========================
# 4. 给 x 轴加轻微抖动，避免点完全重叠
# =========================
rng = np.random.default_rng(42)
x = df["layer_id"].to_numpy(dtype=float)
y = df["overlap_rate"].to_numpy()
x_jitter = x + rng.uniform(-0.18, 0.18, size=len(df))

# =========================
# 5. 绘图
# =========================
fig, ax = plt.subplots(figsize=(6.8, 2.9))

# 全部散点
ax.scatter(
    x_jitter,
    y,
    s=2,
    alpha=0.28,
    color="0.35",
    linewidths=0,
    rasterized=True,   # 点很多时对论文 PDF 更友好
)

# 参考线
ax.axhline(0.8, color="0.25", linestyle="--", linewidth=1.0)
ax.axhline(0.5, color="0.45", linestyle="--", linewidth=1.0)

# 坐标轴
layer_min = df["layer_id"].min()
layer_max = df["layer_id"].max()

ax.set_xlim(layer_min - 0.5, layer_max + 0.5)
ax.set_ylim(-0.02, 1.02)

ax.set_xlabel("Layer")
ax.set_ylabel("Similarity (Overlap@6)")

xticks = np.arange(layer_min, layer_max + 1, 2)
ax.set_xticks(xticks)
ax.set_yticks(np.linspace(0, 1.0, 6))

ax.grid(axis="y", color="0.9", linewidth=0.8)

# 去掉上右边框
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 图内文字说明
ax.text(layer_min + 0.2, 0.82, "> 0.8", fontsize=9, color="0.25", va="bottom")
ax.text(layer_min + 0.2, 0.52, "> 0.5", fontsize=9, color="0.45", va="bottom")

plt.tight_layout(pad=0.4)

# 保存
# plt.savefig("request_app_similarity_scatter.pdf", bbox_inches="tight")
# plt.savefig("request_app_similarity_scatter.png", dpi=300, bbox_inches="tight")
plt.show()
