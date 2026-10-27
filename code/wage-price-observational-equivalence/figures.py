"""Generate reproducible Japanese-language charts for the Zenn draft.

All series and interventions are synthetic. The font comes from the CI runner's
system package (fonts-noto-cjk); the repository contains no font files.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.font_manager import findfont, FontProperties

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)
findfont(FontProperties(family="Noto Sans CJK JP"), fallback_to_default=False)
plt.rcParams.update({
    "font.family": "Noto Sans CJK JP", "font.size": 16,
    "axes.titlesize": 18, "axes.labelsize": 16, "legend.fontsize": 14,
    "xtick.labelsize": 14, "ytick.labelsize": 14,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})
BLUE, ORANGE = "#2665A8", "#BF6328"
shock = np.zeros(9)
shock[0] = 2.0
price_a = np.zeros(9); wage_a = np.zeros(9)
price_b = np.zeros(9); wage_b = np.zeros(9); s_b = np.zeros(9)
for t in range(9):
    price_a[t] = (0.75 * wage_a[t - 1] if t else 0.0) + shock[t]
    wage_a[t] = 0.8 * price_a[t]
    s_b[t] = (0.6 * s_b[t - 1] if t else 0.0) + shock[t]
    price_b[t] = s_b[t]
    wage_b[t] = 0.8 * price_b[t]
np.testing.assert_allclose(price_a, price_b, rtol=0, atol=1e-12)
np.testing.assert_allclose(wage_a, wage_b, rtol=0, atol=1e-12)
np.testing.assert_allclose(price_a[:4], [2, 1.2, 0.72, 0.432], rtol=0, atol=1e-12)

x = np.arange(len(shock))
fig, axes = plt.subplots(2, 1, figsize=(7.4, 9.2), sharex=True)
fig.suptitle("観測される2系列はどちらも完全一致", fontsize=19, weight="bold", y=0.984)
for ax, left, right, name in zip(
    axes, (price_a, wage_a), (price_b, wage_b),
    ("① 物価上昇率の追加分", "② 賃金上昇率の追加分")
):
    ax.plot(x, left, color=BLUE, linewidth=5.2, alpha=0.7,
            label="経済A：賃金・物価の循環", zorder=2)
    ax.plot(x, right, color=ORANGE, linestyle="None", marker="o",
            markersize=10, markerfacecolor="white", markeredgewidth=2.5,
            label="経済B：外部圧力が持続", zorder=3)
    ax.set_title(name, loc="left", pad=13)
    ax.set_ylabel("上昇率の上振れ（pt）")
    ax.set_ylim(-0.13, 2.24)
    ax.grid(axis="y", color="#e6e9ee", linewidth=0.9)
    ax.legend(loc="upper right", frameon=False, fontsize=12.8)
    ax.annotate("AとBが重なる", xy=(3, left[3]), xytext=(3.5, 1.03),
                fontsize=13, color="#314558",
                arrowprops={"arrowstyle": "->", "color": "#657789", "lw": 1.3})
axes[-1].set_xlabel("ショック発生からの期数")
axes[-1].set_xticks(x)
fig.tight_layout(rect=(0, 0.02, 1, 0.963), h_pad=2.6)
path1 = OUT / "wage-price-observational-path.png"
fig.savefig(path1, dpi=175)
plt.close(fig)

periods = np.arange(9)
response_a = np.zeros(9)
response_a[1:] = 0.75 * (0.6 ** np.arange(8))
response_b = np.zeros(9)
np.testing.assert_allclose(response_a[:4], [0, .75, .45, .27], rtol=0, atol=1e-12)
fig, ax = plt.subplots(figsize=(7.4, 6.4))
ax.plot(periods, response_a, color=BLUE, linewidth=3.5, marker="o",
        markersize=8, label="経済A：翌期から効果が残る")
ax.plot(periods, response_b, color=ORANGE, linewidth=2.8,
        linestyle="--", marker="s", markersize=7, label="経済B：効果なし")
ax.annotate("+0.75 pt", xy=(1, .75), xytext=(1.5, .88),
            color=BLUE, fontsize=15, weight="bold",
            arrowprops={"arrowstyle": "-", "lw": 1.2})
ax.annotate("+0.45 pt", xy=(2, .45), xytext=(2.65, .58),
            color=BLUE, fontsize=15, arrowprops={"arrowstyle": "-", "lw": 1.2})
ax.set_title("賃金だけを1ポイント増やしたら？",
             pad=15, fontsize=19, weight="bold")
ax.set_xlabel("介入時点からの期数")
ax.set_ylabel("介入による物価上昇率の差（pt）")
ax.set_xlim(-0.2, 8.3); ax.set_ylim(-0.12, 1.12)
ax.set_xticks(periods)
ax.grid(axis="y", color="#e6e9ee", linewidth=0.9)
ax.legend(loc="upper right", frameon=False, fontsize=12.8)
fig.tight_layout(pad=1.5)
path2 = OUT / "wage-price-wage-intervention.png"
fig.savefig(path2, dpi=175)
plt.close(fig)
for path in (path1, path2):
    assert path.exists() and 10000 < path.stat().st_size < 3_000_000
    print(f"Generated {path}: {path.stat().st_size:,} bytes")
