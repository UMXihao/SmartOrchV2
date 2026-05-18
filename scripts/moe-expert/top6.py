import pandas as pd

# 读取 CSV
df = pd.read_csv("moe_activation_test.csv")

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

print(result)

# 保存结果
result.to_csv("top6_experts_per_layer_test.csv", index=False)
