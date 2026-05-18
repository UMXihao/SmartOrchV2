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
    "request_0": "squad-request/top6_experts_request_0.csv",
    "request_1": "squad-request/top6_experts_request_1.csv",
    "request_2": "squad-request/top6_experts_request_2.csv",
    "request_3": "squad-request/top6_experts_request_3.csv",
    "request_4": "squad-request/top6_experts_request_4.csv",
    "request_5": "squad-request/top6_experts_request_5.csv",
    "request_6": "squad-request/top6_experts_request_6.csv",
    "request_7": "squad-request/top6_experts_request_7.csv",
    "request_8": "squad-request/top6_experts_request_8.csv",
    "request_9": "squad-request/top6_experts_request_9.csv",
    "request_10": "squad-request/top6_experts_request_10.csv",
    "request_11": "squad-request/top6_experts_request_11.csv",
    "request_12": "squad-request/top6_experts_request_12.csv",
    "request_13": "squad-request/top6_experts_request_13.csv",
    "request_14": "squad-request/top6_experts_request_14.csv",
    "request_15": "squad-request/top6_experts_request_15.csv",
    "request_16": "squad-request/top6_experts_request_16.csv",
    "request_17": "squad-request/top6_experts_request_17.csv",
    "request_18": "squad-request/top6_experts_request_18.csv",
    "request_19": "squad-request/top6_experts_request_19.csv",
    "request_20": "squad-request/top6_experts_request_20.csv",
    "request_21": "squad-request/top6_experts_request_21.csv",
    "request_22": "squad-request/top6_experts_request_22.csv",
    "request_23": "squad-request/top6_experts_request_23.csv",
    "request_24": "squad-request/top6_experts_request_24.csv",
    "request_25": "squad-request/top6_experts_request_25.csv",
    "request_26": "squad-request/top6_experts_request_26.csv",
    "request_27": "squad-request/top6_experts_request_27.csv",
    "request_28": "squad-request/top6_experts_request_28.csv",
    "request_29": "squad-request/top6_experts_request_29.csv",
    "request_30": "squad-request/top6_experts_request_30.csv",
    "request_31": "squad-request/top6_experts_request_31.csv",
    "request_32": "squad-request/top6_experts_request_32.csv",
    "request_33": "squad-request/top6_experts_request_33.csv",
    "request_34": "squad-request/top6_experts_request_34.csv",
    "request_35": "squad-request/top6_experts_request_35.csv",
    "request_36": "squad-request/top6_experts_request_36.csv",
    "request_37": "squad-request/top6_experts_request_37.csv",
    "request_38": "squad-request/top6_experts_request_38.csv",
    "request_39": "squad-request/top6_experts_request_39.csv",
    "request_40": "squad-request/top6_experts_request_40.csv",
    "request_41": "squad-request/top6_experts_request_41.csv",
    "request_42": "squad-request/top6_experts_request_42.csv",
    "request_43": "squad-request/top6_experts_request_43.csv",
    "request_44": "squad-request/top6_experts_request_44.csv",
    "request_45": "squad-request/top6_experts_request_45.csv",
    "request_46": "squad-request/top6_experts_request_46.csv",
    "request_47": "squad-request/top6_experts_request_47.csv",
    "request_48": "squad-request/top6_experts_request_48.csv",
    "request_49": "squad-request/top6_experts_request_49.csv",
    "request_50": "squad-request/top6_experts_request_50.csv",
    "request_51": "squad-request/top6_experts_request_51.csv",
    "request_52": "squad-request/top6_experts_request_52.csv",
    "request_53": "squad-request/top6_experts_request_53.csv",
    "request_54": "squad-request/top6_experts_request_54.csv",
    "request_55": "squad-request/top6_experts_request_55.csv",
    "request_56": "squad-request/top6_experts_request_56.csv",
    "request_57": "squad-request/top6_experts_request_57.csv",
    "request_58": "squad-request/top6_experts_request_58.csv",
    "request_59": "squad-request/top6_experts_request_59.csv",
    "request_60": "squad-request/top6_experts_request_60.csv",
    "request_61": "squad-request/top6_experts_request_61.csv",
    "request_62": "squad-request/top6_experts_request_62.csv",
    "request_63": "squad-request/top6_experts_request_63.csv",
    "request_64": "squad-request/top6_experts_request_64.csv",
    "request_65": "squad-request/top6_experts_request_65.csv",
    "request_66": "squad-request/top6_experts_request_66.csv",
    "request_67": "squad-request/top6_experts_request_67.csv",
    "request_68": "squad-request/top6_experts_request_68.csv",
    "request_69": "squad-request/top6_experts_request_69.csv",
    "request_70": "squad-request/top6_experts_request_70.csv",
    "request_71": "squad-request/top6_experts_request_71.csv",
    "request_72": "squad-request/top6_experts_request_72.csv",
    "request_73": "squad-request/top6_experts_request_73.csv",
    "request_74": "squad-request/top6_experts_request_74.csv",
    "request_75": "squad-request/top6_experts_request_75.csv",
    "request_76": "squad-request/top6_experts_request_76.csv",
    "request_77": "squad-request/top6_experts_request_77.csv",
    "request_78": "squad-request/top6_experts_request_78.csv",
    "request_79": "squad-request/top6_experts_request_79.csv",
    "request_80": "squad-request/top6_experts_request_80.csv",
    "request_81": "squad-request/top6_experts_request_81.csv",
    "request_82": "squad-request/top6_experts_request_82.csv",
    "request_83": "squad-request/top6_experts_request_83.csv",
    "request_84": "squad-request/top6_experts_request_84.csv",
    "request_85": "squad-request/top6_experts_request_85.csv",
    "request_86": "squad-request/top6_experts_request_86.csv",
    "request_87": "squad-request/top6_experts_request_87.csv",
    "request_88": "squad-request/top6_experts_request_88.csv",
    "request_89": "squad-request/top6_experts_request_89.csv",
    "request_90": "squad-request/top6_experts_request_90.csv",
    "request_91": "squad-request/top6_experts_request_91.csv",
    "request_92": "squad-request/top6_experts_request_92.csv",
    "request_93": "squad-request/top6_experts_request_93.csv",
    "request_94": "squad-request/top6_experts_request_94.csv",
    "request_95": "squad-request/top6_experts_request_95.csv",
    "request_96": "squad-request/top6_experts_request_96.csv",
    "request_97": "squad-request/top6_experts_request_97.csv",
    "request_98": "squad-request/top6_experts_request_98.csv",
    "request_99": "squad-request/top6_experts_request_99.csv",
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
