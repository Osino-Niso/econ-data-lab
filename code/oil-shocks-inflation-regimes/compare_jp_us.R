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

# Hourly nominal compensation: BLS nonfarm business quarterly YoY series PRS85006101.
# Each annual observation below averages the four quarterly YoY values.
w <- read.csv("code/oil-shocks-inflation-regimes/usa_hourly_compensation_1972_1983.csv")
stopifnot(identical(w$year, 1972:1983))
cols <- c("q1_yoy", "q2_yoy", "q3_yoy", "q4_yoy")
w$annual <- rowMeans(w[cols])
stopifnot(abs(w$annual[w$year == 1975] - 10.45) < 1e-10)
stopifnot(abs(w$annual[w$year == 1980] - 10.725) < 1e-10)
first_mean <- mean(w$annual[w$year >= 1973 & w$year <= 1976])
second_mean <- mean(w$annual[w$year >= 1979 & w$year <= 1982])
first_accel <- w$annual[w$year == 1974] - w$annual[w$year == 1972]
second_accel <- w$annual[w$year == 1980] - w$annual[w$year == 1978]
stopifnot(abs(first_mean - 8.825) < 1e-10,
          abs(second_mean - 9.3125) < 1e-10,
          abs(first_accel - 2.95) < 1e-10,
          abs(second_accel - 2.175) < 1e-10)
cat(sprintf("US nominal hourly compensation: first %.3f%%, second %.3f%%; acceleration %.3fpp / %.3fpp\n",
            first_mean, second_mean, first_accel, second_accel))
