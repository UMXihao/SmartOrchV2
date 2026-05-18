import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# =====================
# 1. 文件路径配置
# =====================

# 应用级别 top6 激活专家 ID
app_file = "top6_experts_per_layer_squad.csv"

# 单个应用内请求 top6 激活专家 ID
# 后面有更多请求文件时，继续在这里添加即可
request_files = {
    "app_1": "app-diff/top6_experts_per_layer_squad.csv",
    "app_2": "app-diff/top6_experts_per_layer_mtbench.csv",
}

# =====================
# 2. 读取应用级别结果
# =====================

df_app = pd.read_csv(app_file)

# =====================
# 3. 计算每个请求文件与应用级别的每层 top6 重合率
# =====================

all_results = []

for req_name, req_file in request_files.items():
    df_req = pd.read_csv(req_file)

    # 找两个表共有的 layer 列
    layers = [col for col in df_req.columns if col in df_app.columns]

    for layer in layers:
        req_ids = set(df_req[layer].dropna().astype(int))
        app_ids = set(df_app[layer].dropna().astype(int))

        common_ids = req_ids & app_ids

        overlap_count = len(common_ids)
        overlap_rate = overlap_count / 6

        all_results.append({
            "request": req_name,
            "layer": layer,
            "overlap_count": overlap_count,
            "overlap_rate": overlap_rate,
            "common_expert_ids": sorted(common_ids)
        })

result_df = pd.DataFrame(all_results)

print(result_df)

# 保存计算结果
result_df.to_csv("multi_request_top6_overlap.csv", index=False)

# =====================
# 4. 只绘制散点图
# =====================

plt.figure(figsize=(14, 5))

# layer 转成 x 轴位置
layers = sorted(result_df["layer"].unique(), key=lambda x: int(x.split("_")[-1]) if "_" in x else x)
x_pos = {layer: i for i, layer in enumerate(layers)}

request_names = list(request_files.keys())

# 多个请求文件时，给每个请求一点横向偏移，避免点完全重叠
offsets = np.linspace(-0.25, 0.25, len(request_names))

for offset, req_name in zip(offsets, request_names):
    sub_df = result_df[result_df["request"] == req_name]

    x_values = [x_pos[layer] + offset for layer in sub_df["layer"]]
    y_values = sub_df["overlap_rate"]

    plt.scatter(
        x_values,
        y_values,
        s=70,
        label=req_name,
        alpha=0.8
    )

plt.xticks(
    ticks=range(len(layers)),
    labels=layers,
    rotation=45
)

plt.ylim(0, 1.1)
plt.xlabel("Layer")
plt.ylabel("Top6 Overlap Rate")
plt.title("Top6 Activated Expert Similarity Between Request-level and App-level Results")

plt.grid(axis="y", linestyle="--", alpha=0.4)
# plt.legend()
plt.tight_layout()

# 保存图片
# plt.savefig("multi_request_top6_overlap_scatter.png", dpi=300)
plt.show()
