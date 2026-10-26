# Historical descriptive checks, NOT estimates of oil supply shocks or causal effects.
# Manually transcribed inputs and source provenance are in README.md.
script_arg <- grep("^--file=", commandArgs(), value = TRUE)
stopifnot(length(script_arg) == 1L)
root <- dirname(normalizePath(sub("^--file=", "", script_arg[1])))
japan <- read.csv(file.path(root, "historical-japan-1972-1981.csv"))
oecd_ulc <- read.csv(file.path(root, "oecd-manufacturing-ulc-1971-1981.csv"))
landed <- read.csv(file.path(root, "opec-landed-us-1978-1980.csv"))
pct <- function(new, old) 100 * (new / old - 1)
stopifnot(nrow(japan) == 10L, nrow(oecd_ulc) == 11L, all(table(landed$year) == 12L))
cpi_yoy <- pct(japan$japan_cpi_index_2015_100[-1],
               japan$japan_cpi_index_2015_100[-nrow(japan)])
print(data.frame(year = japan$year[-1],
                 cpi_yoy_pct = round(cpi_yoy, 4),
                 manuf_ulc_2014_vintage_yoy_pct = round(oecd_ulc$japan_manufacturing_ulc_oecd_benchmarked_yoy_pct[-1],4),
                 manuf_ulc_1981_vintage_yoy_pct = japan$japan_manufacturing_ulc_yoy_pct[-1]))
prices <- aggregate(us_landed_opec_cost_usd_per_bbl ~ year,
                    data = landed, FUN = mean)
price78 <- prices$us_landed_opec_cost_usd_per_bbl[prices$year == 1978]
price79 <- prices$us_landed_opec_cost_usd_per_bbl[prices$year == 1979]
supply <- function(y) japan$world_oil_supply_thousand_bpd[japan$year == y]
cat(sprintf("World supply 1973-74: %.2f%%; 1978-79: %.2f%%; landed crude 1978-79: %.2f%%\n",
            pct(supply(1974),supply(1973)), pct(supply(1979),supply(1978)),
            pct(price79,price78)))
stopifnot(abs(pct(supply(1974),supply(1973)) - 0.1534569983) < 1e-7,
          abs(pct(supply(1979),supply(1978)) - 4.2787076684) < 1e-7,
          abs(pct(price79,price78) - 48.8750654032) < 1e-7,
          abs(oecd_ulc$japan_manufacturing_ulc_oecd_benchmarked_yoy_pct[oecd_ulc$year == 1974] - 27.2525940505659) < 1e-8,
          abs(oecd_ulc$japan_manufacturing_ulc_oecd_benchmarked_yoy_pct[oecd_ulc$year == 1979] + 1.37702686777972) < 1e-8,
          abs(oecd_ulc$japan_manufacturing_ulc_oecd_benchmarked_yoy_pct[oecd_ulc$year == 1980] - 4.71712159349492) < 1e-8,
          japan$japan_manufacturing_ulc_yoy_pct[japan$year == 1974] == 30,
          japan$japan_manufacturing_ulc_yoy_pct[japan$year == 1979] == -3)
cat("Checks passed. These are descriptive comparisons, not causal estimates.\n")
