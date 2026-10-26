"""Reproduce descriptive historical comparisons; NOT causal shock identification.

Raw data were manually transcribed; see README.md for series IDs and source URLs.
No network access or extra packages are needed.
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def change(new, old):
    return 100 * (float(new) / float(old) - 1)

def main():
    with (ROOT / "historical-japan-1972-1981.csv").open(encoding="utf-8", newline="") as f:
        year = {int(r["year"]): r for r in csv.DictReader(f)}
    with (ROOT / "opec-landed-us-1978-1980.csv").open(encoding="utf-8", newline="") as f:
        prices = defaultdict(list)
        for r in csv.DictReader(f):
            prices[int(r["year"])].append(float(r["us_landed_opec_cost_usd_per_bbl"]))
    assert list(year) == list(range(1972, 1982))
    assert all(len(v) == 12 for v in prices.values())
    means = {y: sum(v)/len(v) for y,v in prices.items()}
    print("Year | Japan CPI yoy (%) | Manufacturing ULC yoy (%) | Manufacturing output price yoy (%)")
    for y in range(1973, 1982):
        cpi = change(year[y]["japan_cpi_index_2015_100"],
                     year[y-1]["japan_cpi_index_2015_100"])
        r=year[y]
        print(f'{y} | {cpi:.2f} | {r["japan_manufacturing_ulc_yoy_pct"] or "NA"} | {r["japan_manufacturing_output_price_yoy_pct"] or "NA"}')
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
    assert year[1974]["japan_manufacturing_ulc_yoy_pct"] == "30"
    assert year[1979]["japan_manufacturing_ulc_yoy_pct"] == "-3"
    print("Checks passed. These are descriptive comparisons, not causal estimates.")

if __name__ == "__main__":
    main()
