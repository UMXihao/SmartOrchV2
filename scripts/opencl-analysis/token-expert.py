import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
# 假设你的 CSV 文件名为 data.csv
df = pd.read_csv('token.csv')

# 查看数据
print(df)

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(df['expert'], df['cumulative_assign'], color='skyblue')
plt.xlabel('Expert')
plt.ylabel('Cumulative Assign')
plt.title('Cumulative Assign per Expert')
plt.xticks(rotation=45)  # 如果 x 轴标签太密，可以旋转
plt.tight_layout()  # 自动调整布局，防止标签被遮挡

# 显示图形
plt.show()
