"""World Bank WDI (via FRED) annual CPI inflation: Japan vs United States.
Only an observational comparison. Not an estimate of oil pass-through.
Series: FPCPITOTLZGJPN, FPCPITOTLZGUSA.
Both are annual all-items CPI inflation, not the BOJ speech's CPI excluding food and energy.
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
with (ROOT / "jp_us_headline_1970_1983.csv").open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
years = [int(row["year"]) for row in rows]
jp = [float(row["japan"]) for row in rows]
us = [float(row["united_states"]) for row in rows]
assert years == list(range(1970, 1984))
assert abs(jp[4] - 23.2222458076842) < 1e-8
assert abs(us[4] - 11.0548048048048) < 1e-8
assert abs(jp[10] - 7.77858176555718) < 1e-8
assert abs(us[10] - 13.5492019749684) < 1e-8

plt.rcParams["font.family"] = "Noto Sans CJK JP"
fig, ax = plt.subplots(figsize=(11.6, 5.65), dpi=170)
ax.plot(years, jp, marker="o", markersize=4, linewidth=2.7, label="日本")
ax.plot(years, us, marker="s", markersize=3.8, linewidth=2.5, label="米国")
for year in (1974, 1980):
    ax.axvspan(year - 0.4, year + 0.4, color="#eaeaea", zorder=0)
    j, u = jp[years.index(year)], us[years.index(year)]
    ax.annotate(f"{j:.1f}%", (year, j), xytext=(-4, 11),
                textcoords="offset points", ha="right", fontsize=11, weight="bold")
    ax.annotate(f"{u:.1f}%", (year, u), xytext=(7, -15),
                textcoords="offset points", ha="left", fontsize=11, weight="bold")
ax.set(xlim=(1969.6, 1983.4), ylim=(0, 26),
       ylabel="総合CPI上昇率（年平均、%）", xlabel="暦年",
       title="1970年代のインフレ：日本と米国で大小関係が逆転")
ax.set_xticks(range(1970, 1984, 2))
ax.grid(axis="y", alpha=.22)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper right", frameon=False)
fig.text(.125, .012,
         "出典：世界銀行 WDI（IMF IFS、FRED経由）。総合CPIの暦年上昇率。日銀講演の「食料・エネルギー除くCPI」とは別系列。因果分析ではない。",
         fontsize=7.8, alpha=.75)
fig.tight_layout(rect=[0, .03, 1, 1])
destination = ROOT.parent.parent / "images" / "boj-oil-us-japan-cpi-1970-1983.webp"
destination.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(destination, format="webp", dpi=170)
print(f"wrote {destination}")
print(f"1974: JP {jp[4]:.2f}, USA {us[4]:.2f}; 1980: JP {jp[10]:.2f}, USA {us[10]:.2f}")
