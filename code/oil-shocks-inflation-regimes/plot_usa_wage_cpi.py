"""BLS/FRED hourly nominal compensation growth vs WDI/FRED all-items CPI.
Income measure PRS85006101: Nonfarm Business Sector: Hourly Compensation
for All Workers; quarterly percent change from a year ago (not wage spiral).
Quarterly rates are arithmetically averaged to obtain each calendar-year entry.
CPI FPCPITOTLZGUSA is its publisher's annual all-items CPI inflation.
Observational only; not country-matched measures and not a causal analysis.
"""
import csv
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
with (ROOT / "usa_hourly_compensation_1972_1983.csv").open(encoding="utf-8") as file:
    wages = list(csv.DictReader(file))
with (ROOT / "jp_us_headline_1970_1983.csv").open(encoding="utf-8") as file:
    inflation = list(csv.DictReader(file))
wage_by_year = {int(r["year"]): mean(float(r[q]) for q in ("q1_yoy","q2_yoy","q3_yoy","q4_yoy")) for r in wages}
cpi_by_year = {int(r["year"]): float(r["united_states"]) for r in inflation}
years = sorted(wage_by_year)
assert years == list(range(1972, 1984))
# Compare pre-shock calendar years (not the immediate pre-shock quarters).
pre_first_cpi, pre_second_cpi = cpi_by_year[1972], cpi_by_year[1978]
pre_first_comp, pre_second_comp = wage_by_year[1972], wage_by_year[1978]
assert abs(pre_first_cpi-3.27227824655282) < 1e-9
assert abs(pre_second_cpi-7.63096383885605) < 1e-9
assert abs(pre_first_comp-6.475) < 1e-9
assert abs(pre_second_comp-8.55) < 1e-9
assert pre_second_cpi > pre_first_cpi and pre_second_comp > pre_first_comp
print(f"Pre-shock proxies: 1972 CPI {pre_first_cpi:.3f}% and compensation {pre_first_comp:.3f}%; "
      f"1978 CPI {pre_second_cpi:.3f}% and compensation {pre_second_comp:.3f}%")

assert abs(wage_by_year[1975] - 10.45) < 1e-9
assert abs(wage_by_year[1980] - 10.725) < 1e-9
for start,end in ((1973,1976),(1979,1982)):
    wc=mean(wage_by_year[y] for y in range(start,end+1))
    pc=mean(cpi_by_year[y] for y in range(start,end+1))
    print(f"{start}–{end} hourly nominal compensation: {wc:.4f}% | headline CPI: {pc:.4f}%")
assert abs(mean(wage_by_year[y] for y in range(1973,1977))-8.825) < 1e-9
assert abs(mean(wage_by_year[y] for y in range(1979,1983))-9.3125) < 1e-9
first_accel = wage_by_year[1975]-wage_by_year[1972]
second_accel = wage_by_year[1980]-wage_by_year[1978]
assert abs(first_accel-3.975)<1e-9 and abs(second_accel-2.175)<1e-9
print(f"1972→1975 wage-growth change: {first_accel:+.3f}pp; 1978→1980: {second_accel:+.3f}pp")

plt.rcParams["font.family"]="Noto Sans CJK JP"
fig, ax=plt.subplots(figsize=(11.5,5.8),dpi=180)
ax.plot(years,[cpi_by_year[y] for y in years],marker="o",linewidth=2.7,label="総合CPI上昇率")
ax.plot(years,[wage_by_year[y] for y in years],marker="s",linewidth=2.7,label="時間当たり名目報酬上昇率")
for y in (1974,1980):
    ax.axvspan(y-.33,y+.33,color="#ededed",zorder=0)
ax.set(xlim=(1971.7,1983.3),ylim=(0,16),xlabel="暦年",ylabel="前年比（%）",
       title="米国：石油ショック期の物価と時間当たり名目報酬")
ax.set_xticks(list(range(1972,1984,2)))
ax.grid(axis="y",alpha=.25)
ax.spines[["top","right"]].set_visible(False)
ax.legend(loc="upper right",frameon=False)
fig.text(.11,.014,"出所：世界銀行WDI・BLS（FRED経由）。報酬は四半期前年比の単純平均。系列定義は異なり、因果関係は示さない。",fontsize=8,alpha=.75)
fig.tight_layout(rect=[0,.035,1,1])
image_path=ROOT.parent.parent/"images"/"boj-us-wage-cpi-1972-1983.webp"
image_path.parent.mkdir(exist_ok=True,parents=True)
fig.savefig(image_path,format="webp",dpi=180)
print("saved",image_path)
