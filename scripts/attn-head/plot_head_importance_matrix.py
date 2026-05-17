import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    csv_path = Path("dist_csv/head_importance_mtbench.csv")

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
        columns="layer",
        index="head",
        values=value_col,
        aggfunc="mean"
    )

    matrix = matrix.sort_index(axis=0).sort_index(axis=1)

    # fig_width = max(8, matrix.shape[1] * 0.6)
    # fig_height = max(6, matrix.shape[0] * 0.35)
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8.5,  # 全局默认字体
        "axes.labelsize": 9,  # 坐标轴标题
        "axes.titlesize": 9,  # 子图标题
        "xtick.labelsize": 7.5,  # x轴刻度
        "ytick.labelsize": 7.5,  # y轴刻度
        "legend.fontsize": 7.5,  # 图例
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
    # 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Grays_r', 'Greens', 'Greens_r',
    # 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r',
    # 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r',
    # 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu',
    # 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r',
    # 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r',
    # 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'berlin', 'berlin_r',
    # 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r',
    # 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r',
    # 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_grey_r', 'gist_heat',
    # 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r',
    # 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gist_yerg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r',
    # 'gray', 'gray_r', 'grey', 'grey_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r',
    # 'magma', 'magma_r', 'managua', 'managua_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink',
    # 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring',
    # 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r',
    # 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r',
    # 'vanimo', 'vanimo_r', 'viridis', 'viridis_r', 'winter', 'winter_r'

    plt.figure(figsize=(6.9, 1.5))

    im = plt.imshow(
        matrix.values,
        aspect="auto",
        interpolation="nearest",
        # cmap=plt.get_cmap("PRGn_r"),
    )

    plt.colorbar(im, label=value_col)

    plt.xlabel("Layer ID")
    plt.ylabel("Head ID")

    plt.xticks(
        ticks=range(matrix.shape[1]),
        labels=matrix.columns.tolist()
    )

    plt.yticks(
        ticks=range(matrix.shape[0]),
        labels=matrix.index.tolist()
    )

    plt.tight_layout()
    plt.savefig("result/head_importance_matrix_mtbench.pdf", bbox_inches="tight")
    # plt.show()
    # plt.close()

if __name__ == "__main__":
    main()
