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
    # CI: the two line series in the Zenn Mermaid figure must match the CSV.
    # This prevents editorial changes from quietly leaving the plot out of date.
    article = (ROOT.parent.parent / "articles" / "oil-shocks-inflation-regimes.md").read_text(encoding="utf-8")
    assert "published: false" in article and "published: true" not in article
    assert article.count("xychart-beta") == 1
    diagram = article.split("xychart-beta", 1)[1].split("```", 1)[0]
    # A named series requires Mermaid 11.17+ for the legend. In addition to
    # numeric agreement, check the labels so the two lines are identifiable.
    plotted = re.findall(r'^\s*line\s+"([^"]+)"\s*\[([^]]+)\]', diagram, flags=re.MULTILINE)
    assert [name for name, _ in plotted] == ["Manufacturing ULC", "All-items CPI"], (
        "Expect two clearly named Mermaid lines in ULC, CPI order"
    )
    parsed = [[float(v.strip()) for v in vals.split(",")] for _, vals in plotted]
    actual_years = list(range(1973, 1982))
    expected = [
        [oecd_ulc[y] for y in actual_years],
        [change(year[y]["japan_cpi_index_2015_100"],
                year[y-1]["japan_cpi_index_2015_100"]) for y in actual_years],
    ]
    for series, expected_series in zip(parsed, expected):
        assert len(series) == len(expected_series)
        assert all(abs(observed - reference) <= 0.0051
                   for observed, reference in zip(series, expected_series)), (
            "Mermaid series disagrees with source CSV rounded to 2 decimals"
        )
    assert "x-axis [1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981]" in diagram
    # CI also checks every row of the reader-facing Markdown table, not just the plot.
    rows = []
    expected_year_labels = {str(y) for y in actual_years}
    for line in article.splitlines():
        cells = [cell.strip() for cell in line.strip().split("|")]
        if len(cells) == 5 and cells[1] in expected_year_labels:
            rows.append((
                int(cells[1]),
                float(cells[2].removesuffix("％").replace("−", "-")),
                float(cells[3].removesuffix("％").replace("−", "-")),
            ))
    assert [year for year, _, _ in rows] == actual_years, (
        "Expected the complete 1973–1981 ULC/CPI Markdown table"
    )
    for (y, table_ulc, table_cpi), ref_ulc, ref_cpi in zip(rows, *expected):
        assert abs(table_ulc - ref_ulc) <= 0.0051, (
            f"ULC table for {y} disagrees with fixed CSV"
        )
        assert abs(table_cpi - ref_cpi) <= 0.0051, (
            f"CPI table for {y} disagrees with fixed CSV"
        )
    print("Zenn Markdown ULC/CPI table and Mermaid plot match source CSV.")
    print("Checks passed. These are descriptive comparisons, not causal estimates.")

if __name__ == "__main__":
    main()
