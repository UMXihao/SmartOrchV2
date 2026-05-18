import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap, BoundaryNorm

# =========================
# 1. 输入文件
# =========================
dataset_files = {
    "dataset_1": "dataset_1_top6.csv",
    "dataset_2": "dataset_2_top6.csv",
    "dataset_3": "dataset_3_top6.csv",
    "dataset_4": "dataset_4_top6.csv",
}

# =========================
# 2. 读取数据
# 每个文件格式：
# layer_0, layer_1, ..., layer_24
# 每列 6 个 expert id
# =========================
data = {}
for name, path in dataset_files.items():
    df = pd.read_csv(path)
    layer_cols = sorted(
        df.columns,
        key=lambda x: int(str(x).split("_")[-1])
    )
    data[name] = df[layer_cols]

layer_cols = list(next(iter(data.values())).columns)
num_layers = len(layer_cols)

# =========================
# 3. 构造 “expert × layer” 的共享次数矩阵
# count_matrix[expert, layer] = 该 expert 在该层被多少个数据集选入 top6
# =========================
all_experts = set()
for df in data.values():
    for col in layer_cols:
        all_experts.update(df[col].dropna().astype(int).tolist())

all_experts = sorted(all_experts)
expert_to_idx = {eid: i for i, eid in enumerate(all_experts)}

count_matrix = np.zeros((len(all_experts), num_layers), dtype=int)

for layer_idx, layer in enumerate(layer_cols):
    # 统计这一层每个 expert 出现在多少个数据集的 top6 中
    layer_counter = {}

    for dataset_name, df in data.items():
        experts = set(df[layer].dropna().astype(int).tolist())
        for eid in experts:
            layer_counter[eid] = layer_counter.get(eid, 0) + 1

    for eid, cnt in layer_counter.items():
        row_idx = expert_to_idx[eid]
        count_matrix[row_idx, layer_idx] = cnt

# =========================
# 4. 只保留“至少在某一层被 2 个及以上数据集共享过”的专家
# 避免图太稀疏
# =========================
shared_mask = (count_matrix.max(axis=1) >= 2)
plot_matrix = count_matrix[shared_mask]
plot_experts = np.array(all_experts)[shared_mask]

# 按“总共享强度”排序，让图更紧凑
sort_idx = np.argsort(-plot_matrix.sum(axis=1))
plot_matrix = plot_matrix[sort_idx]
plot_experts = plot_experts[sort_idx]

# =========================
# 5. 统计每层共享专家数量
# “共享专家”定义为在该层被至少 2 个数据集共同选中
# =========================
shared_expert_per_layer = (count_matrix >= 2).sum(axis=0)
shared_by_all4_per_layer = (count_matrix == 4).sum(axis=0)

# =========================
# 6. 绘图风格
# =========================
mpl.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 8,
    "legend.fontsize": 9,
    "axes.linewidth": 0.8,
})

fig = plt.figure(figsize=(7.0, 4.8))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 4.0], hspace=0.08)

# -------------------------
# 上图：每层共享专家数量
# -------------------------
ax_top = fig.add_subplot(gs[0, 0])
x = np.arange(num_layers)

ax_top.plot(
    x, shared_expert_per_layer,
    marker="o", linewidth=1.8, markersize=4,
    label="Shared by >=2 datasets"
)
ax_top.plot(
    x, shared_by_all4_per_layer,
    marker="s", linewidth=1.4, markersize=3.5,
    label="Shared by all 4 datasets"
)

ax_top.set_xlim(-0.5, num_layers - 0.5)
ax_top.set_ylabel("#Shared\nExperts")
ax_top.grid(axis="y", linestyle="--", alpha=0.3)
ax_top.spines["top"].set_visible(False)
ax_top.spines["right"].set_visible(False)
ax_top.set_xticks([])
ax_top.legend(frameon=False, loc="upper right")

# -------------------------
# 下图：共享专家热力图
# -------------------------
ax = fig.add_subplot(gs[1, 0])

# 离散颜色：0,1,2,3,4
cmap = ListedColormap([
    "#FFFFFF",  # 0
    "#D9D9D9",  # 1
    "#9ECAE1",  # 2
    "#3182BD",  # 3
    "#08519C",  # 4
])
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)

im = ax.imshow(
    plot_matrix,
    aspect="auto",
    interpolation="nearest",
    cmap=cmap,
    norm=norm,
    origin="upper"
)

ax.set_xlabel("Layer")
ax.set_ylabel("Expert ID")

ax.set_xticks(np.arange(num_layers))
ax.set_xticklabels([str(i) for i in range(num_layers)])

# y 轴标签过多时做稀疏显示
if len(plot_experts) <= 30:
    ax.set_yticks(np.arange(len(plot_experts)))
    ax.set_yticklabels(plot_experts)
else:
    step = max(1, len(plot_experts) // 20)
    yticks = np.arange(0, len(plot_experts), step)
    ax.set_yticks(yticks)
    ax.set_yticklabels(plot_experts[yticks])

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label("#Datasets containing the expert in Top-6")
cbar.set_ticks([0, 1, 2, 3, 4])

plt.tight_layout()
# plt.savefig("shared_experts_across_datasets.pdf", bbox_inches="tight")
# plt.savefig("shared_experts_across_datasets.png", dpi=300, bbox_inches="tight")
plt.show()
