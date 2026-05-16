import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    csv_path = Path("head_importance.csv")

    df = pd.read_csv(csv_path)
    value_col = "importance"
    required_cols = {"layer", "head", value_col}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    df["layer"] = df["layer"].astype(int)
    df["head"] = df["head"].astype(int)

    # 如果同一个 layer-head 有多条记录，则取平均
    matrix = df.pivot_table(
        index="layer",
        columns="head",
        values=value_col,
        aggfunc="mean"
    )

    matrix = matrix.sort_index(axis=0).sort_index(axis=1)

    fig_width = max(8, matrix.shape[1] * 0.6)
    fig_height = max(6, matrix.shape[0] * 0.35)

    plt.figure(figsize=(fig_width, fig_height))

    im = plt.imshow(
        matrix.values,
        aspect="auto",
        interpolation="nearest"
    )

    plt.colorbar(im, label=value_col)

    plt.xlabel("Attention Head")
    plt.ylabel("Layer")

    plt.xticks(
        ticks=range(matrix.shape[1]),
        labels=matrix.columns.tolist()
    )

    plt.yticks(
        ticks=range(matrix.shape[0]),
        labels=matrix.index.tolist()
    )

    # if annotate:
    #     for i in range(matrix.shape[0]):
    #         for j in range(matrix.shape[1]):
    #             value = matrix.values[i, j]
    #             if pd.notna(value):
    #                 plt.text(
    #                     j,
    #                     i,
    #                     f"{value:.3f}",
    #                     ha="center",
    #                     va="center",
    #                     fontsize=7
    #                 )

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
