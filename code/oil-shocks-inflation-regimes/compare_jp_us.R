# World Bank WDI, via FRED. Annual headline CPI inflation; not oil-shock causal effects.
# Dataset: https://fred.stlouisfed.org/data/FPCPITOTLZGJPN
#          https://fred.stlouisfed.org/data/FPCPITOTLZGUSA
x <- read.csv("code/oil-shocks-inflation-regimes/jp_us_headline_1970_1983.csv")
stopifnot(identical(x$year, 1970:1983))
stopifnot(abs(x$japan[x$year == 1974] - 23.2222458076842) < 1e-8)
stopifnot(abs(x$united_states[x$year == 1980] - 13.5492019749684) < 1e-8)
mean_period <- function(from, to) {
  y <- x[x$year >= from & x$year <= to, ]
  c(Japan = mean(y$japan), US = mean(y$united_states))
}
a <- mean_period(1973, 1976)
b <- mean_period(1979, 1982)
stopifnot(a["Japan"] > a["US"], b["Japan"] < b["US"])
stopifnot(abs(a["Japan"] - 13.9840429731348) < 1e-8)
stopifnot(abs(b["US"] - 10.3174538612) < 1e-8)
print(rbind(`1973-1976` = a, `1979-1982` = b))
cat("Japan/US observational comparison validation passed.\n")
