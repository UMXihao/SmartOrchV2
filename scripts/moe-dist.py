import os
import numpy as np
import math
from typing import Tuple

# 读取一个文本文件中的数字（默认每行一个）
def read_numbers(path: str) -> np.ndarray:
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")
    nums = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s == '':
                continue
            try:
                nums.append(float(s))
            except ValueError:
                # 若一行有多个值（逗号/空格分隔），尝试逐个解析
                parts = s.replace(',', ' ').split()
                for p in parts:
                    try:
                        nums.append(float(p))
                    except ValueError:
                        pass
    return np.array(nums, dtype=float)

# 余弦相似度（可选均值中心化）
def cosine_similarity(x: np.ndarray, y: np.ndarray, center: bool = False) -> float:
    x = x.astype(float)
    y = y.astype(float)
    if center:
        x = x - x.mean()
        y = y - y.mean()
    denom = (np.linalg.norm(x) * np.linalg.norm(y))
    if denom == 0:
        return float('nan')
    return float(np.dot(x, y) / denom)

# Pearson 相关系数
def pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    if x.size != y.size:
        raise ValueError("Pearson相关系数需要两个数组长度一致。")
    x = x.astype(float)
    y = y.astype(float)
    xm = x - x.mean()
    ym = y - y.mean()
    denom = math.sqrt((xm**2).sum()) * math.sqrt((ym**2).sum())
    if denom == 0:
        return float('nan')
    return float((xm*ym).sum() / denom)

# Softmax 归一化为概率分布
def softmax(v: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    v = np.array(v, dtype=float) / float(temperature)
    m = np.max(v)
    e = np.exp(v - m)  # 数值稳定
    s = e.sum()
    if s == 0:
        return np.ones_like(v) / v.size
    return e / s

# Jensen–Shannon 距离（JS distance = sqrt(JS divergence)）
def jensen_shannon_distance(p: np.ndarray, q: np.ndarray) -> float:
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)
    p = p / p.sum() if p.sum() != 0 else np.ones_like(p) / p.size
    q = q / q.sum() if q.sum() != 0 else np.ones_like(q) / q.size
    m = 0.5 * (p + q)

    def kl(a, b):
        eps = 1e-12  # 防止 log(0)
        a2 = a + eps
        b2 = b + eps
        return float(np.sum(a2 * np.log(a2 / b2)))

    js_div = 0.5 * kl(p, m) + 0.5 * kl(q, m)
    return float(math.sqrt(max(js_div, 0.0)))

# 经验分布函数
def ecdf(x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    xs = np.sort(x.astype(float))
    n = xs.size
    cdf = np.arange(1, n+1) / n
    return xs, cdf

# 两样本 Kolmogorov–Smirnov 统计量 D
def ks_statistic(x: np.ndarray, y: np.ndarray) -> float:
    xs, cdf_x = ecdf(x)
    ys, cdf_y = ecdf(y)
    all_points = np.sort(np.unique(np.concatenate([xs, ys])))

    def cdf_at(arr_sorted, arr_cdf, t):
        idx = np.searchsorted(arr_sorted, t, side='right')
        if idx == 0:
            return 0.0
        return float(arr_cdf[idx-1])

    diffs = [abs(cdf_at(xs, cdf_x, t) - cdf_at(ys, cdf_y, t)) for t in all_points]
    return float(np.max(diffs))


for i in range(25):
    # === 修改为你的文件名 ===
    num = i + 1
    file_a = 'decode_ffn_moe_argsort-'+ num +'.txt'
    file_b = 'prefill_ffn_moe_argsort-'+ num +'.txt'

    # === 主流程 ===
    x = read_numbers(file_a)
    y = read_numbers(file_b)

    summary = {
        'len_x': int(x.size),
        'len_y': int(y.size),
        'mean_x': float(np.mean(x)) if x.size else float('nan'),
        'mean_y': float(np.mean(y)) if y.size else float('nan'),
        'std_x': float(np.std(x, ddof=1)) if x.size > 1 else float('nan'),
        'std_y': float(np.std(y, ddof=1)) if y.size > 1 else float('nan'),
        'min_x': float(np.min(x)) if x.size else float('nan'),
        'min_y': float(np.min(y)) if y.size else float('nan'),
        'max_x': float(np.max(x)) if x.size else float('nan'),
        'max_y': float(np.max(y)) if y.size else float('nan'),
    }

    cos_raw = cosine_similarity(x, y, center=False)
    cos_centered = cosine_similarity(x, y, center=True)
    pearson = pearson_r(x, y) if x.size == y.size else float('nan')

    p_x = softmax(x, temperature=1.0)
    p_y = softmax(y, temperature=1.0)
    js_dist = jensen_shannon_distance(p_x, p_y)

    ks_D = ks_statistic(x, y)

    results = {
        'summary': summary,
        'cosine_similarity_raw': cos_raw,
        'cosine_similarity_centered': cos_centered,
        'pearson_r': pearson,
        'jensen_shannon_distance_softmax': js_dist,
        'ks_statistic_D': ks_D,
    }

    print("数据概览:", summary)
    print("余弦相似度（原始）:", cos_raw)
    print("余弦相似度（中心化）:", cos_centered)
    print("Pearson 相关系数:", pearson)
    print("Jensen–Shannon 距离（softmax后）:", js_dist)
    print("KS 统计量 D:", ks_D)
