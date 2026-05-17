import pandas as pd
import matplotlib.pyplot as plt


def plot_moe_heatmap(
    csv_path="moe_activation.csv",
    output_path="moe_activation_heatmap.png"
):
    # 读取 CSV
    df = pd.read_csv(csv_path)

    # 第一列是 expert_id，其余列是每一层的激活次数
    expert_ids = df["expert_id"]
    data = df.drop(columns=["expert_id"])

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 8.5,  # 全局默认字体
        "axes.labelsize": 9,  # 坐标轴标题
        "axes.titlesize": 9,  # 子图标题
        "xtick.labelsize": 7.5,  # x轴刻度
        "ytick.labelsize": 7.5,  # y轴刻度
        "legend.fontsize": 7.5,  # 图例
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    plt.figure(figsize=(14, 10))

    # 绘制热力图
    plt.imshow(data.values, aspect="auto", cmap="Reds")

    # 设置坐标轴
    plt.colorbar(label="Activation Count")
    plt.xlabel("Layer")
    plt.ylabel("Expert ID")
    plt.title("MoE Expert Activation Heatmap")

    plt.xticks(
        ticks=range(len(data.columns)),
        labels=data.columns,
        rotation=90
    )

    plt.yticks(
        ticks=range(len(expert_ids)),
        labels=expert_ids
    )

    plt.tight_layout()

    # 保存图片
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"热力图已保存到: {output_path}")


if __name__ == "__main__":
    plot_moe_heatmap(
        csv_path="moe_activation.csv",
        output_path="result/moe_activation_heatmap.pdf"
    )
