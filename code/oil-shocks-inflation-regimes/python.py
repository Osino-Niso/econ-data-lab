"""Reproduce descriptive historical comparisons; NOT causal shock identification.

Raw data were manually transcribed; see README.md for series IDs and source URLs.
No network access or extra packages are needed.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def change(new, old):
    return 100 * (float(new) / float(old) - 1)

def main():
    with (ROOT / "historical-japan-1972-1981.csv").open(encoding="utf-8", newline="") as f:
        year = {int(r["year"]): r for r in csv.DictReader(f)}
    with (ROOT / "oecd-manufacturing-ulc-1971-1981.csv").open(encoding="utf-8", newline="") as f:
        oecd_ulc = {int(r["year"]): float(r["japan_manufacturing_ulc_oecd_benchmarked_yoy_pct"])
                    for r in csv.DictReader(f)}
    with (ROOT / "opec-landed-us-1978-1980.csv").open(encoding="utf-8", newline="") as f:
        prices = defaultdict(list)
        for r in csv.DictReader(f):
            prices[int(r["year"])].append(float(r["us_landed_opec_cost_usd_per_bbl"]))
    assert list(year) == list(range(1972, 1982))
    assert list(oecd_ulc) == list(range(1971, 1982))
    assert all(len(v) == 12 for v in prices.values())
    means = {y: sum(v)/len(v) for y,v in prices.items()}
    print("Year | CPI yoy (%) | OECD manuf ULC yoy (%) [2014 FRED] | manuf ULC yoy (%) [1981 Hansard] | manuf output price yoy (%)")
    for y in range(1973, 1982):
        cpi = change(year[y]["japan_cpi_index_2015_100"],
                     year[y-1]["japan_cpi_index_2015_100"])
        r=year[y]
        print(f'{y} | {cpi:.2f} | {oecd_ulc[y]:.2f} | {r["japan_manufacturing_ulc_yoy_pct"] or "NA"} | {r["japan_manufacturing_output_price_yoy_pct"] or "NA"}')
    supply_73_74 = change(year[1974]["world_oil_supply_thousand_bpd"], year[1973]["world_oil_supply_thousand_bpd"])
    supply_78_79 = change(year[1979]["world_oil_supply_thousand_bpd"], year[1978]["world_oil_supply_thousand_bpd"])
    landed_78_79 = change(means[1979], means[1978])
    print(f"World oil supply 1973-74: {supply_73_74:.2f}%, 1978-79: {supply_78_79:.2f}%")
    print(f"U.S. landed OPEC crude 1978: {means[1978]:.3f}, 1979: {means[1979]:.3f} USD/bbl, change: {landed_78_79:.2f}%")
    assert abs(supply_73_74 - 0.1534569983) < 1e-7
    assert abs(supply_78_79 - 4.2787076684) < 1e-7
    assert abs(landed_78_79 - 48.8750654032) < 1e-7
    assert abs(change(year[1974]["japan_cpi_index_2015_100"], year[1973]["japan_cpi_index_2015_100"]) - 23.0965113318) < 1e-7
    assert abs(change(year[1979]["japan_cpi_index_2015_100"], year[1978]["japan_cpi_index_2015_100"]) - 3.7531902117) < 1e-7
    assert abs(oecd_ulc[1974] - 27.2525940505659) < 1e-8
    assert abs(oecd_ulc[1979] - (-1.37702686777972)) < 1e-8
    assert abs(oecd_ulc[1980] - 4.71712159349492) < 1e-8
    assert year[1974]["japan_manufacturing_ulc_yoy_pct"] == "30"
    assert year[1979]["japan_manufacturing_ulc_yoy_pct"] == "-3"
    # The reader-facing article is now an introductory explanation. Technical
    # ULC/CPI year tables and Q-JEM are reserved for the later advanced article.
    # Keep verifying the historical data above for future reuse, but do not
    # require a chart or numerical table that is no longer in the intro.
    article = (ROOT.parent.parent / "articles" / "oil-shocks-inflation-regimes.md").read_text(encoding="utf-8")
    assert "published: false" in article and "published: true" not in article
    assert article.count("flowchart TD") == 1, "Expect exactly one educational feedback-flow diagram"
    assert "xychart-beta" not in article, "Technical ULC/CPI chart belongs in the advanced article"
    assert "| 年 | 製造業ULC前年比" not in article
    assert "Q-JEM" not in article
    assert article.count(":::details 解答と理由") == 3, "Expect three independent learning checks"
    assert article.count(":::details 説明例と確認ポイント") == 1, "Expect an optional 100-character mastery challenge"
    assert article.count(":::details") == 4, "Expect three exercises plus one foldable self-check"
    assert article.count("### Q1：110円のままなら、値上がり率はどうなる？") == 1
    assert article.count("### Q3：2000年代半ばと2021年以降、何が違った？") == 1
    assert "### 仕上げ：この記事の疑問を100～150字程度で説明してみよう" in article
    assert "なぜ原油高の図なのに「食料・エネルギーを除くCPI」を見るのでしょうか" in article
    assert "それ以外の商品やサービスの価格にまで上昇が広がっているか" in article
    assert "年号や数値の暗記は不要です" in article
    assert "その時期のどんな条件が連鎖の強さに関係したのか" in article
    assert "T−1" in article and "T＋1" in article and "右側の目盛り" in article
    assert all(
        f"/images/boj-ueda-2026-chart-{n}-quoted.webp" in article
        for n in range(2, 6)
    ), "All four BOJ lecture charts should remain in the introduction"
    assert "原油高で輸入費用が上昇" in article and "次の価格改定" in article
    assert all(f"**{y}" in article for y in ("1973年", "1979年"))
    assert "2000年代半ば" in article and "2021年以降" in article
    print("Intro Zenn article: diagram, 4 charts, 3 questions and a mastery challenge validated.")
    print("Checks passed. These are descriptive comparisons, not causal estimates.")

if __name__ == "__main__":
    main()
