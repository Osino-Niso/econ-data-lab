# Hypothetical CPI index paths only; not Japanese historical CPI observations.
paths <- list(
  A_one_step = c(100, 104, 104, 104),
  B_delayed = c(100, 102, 104, 104),
  C_persistent = c(100, 104, 108.16, 112.4864)
)

inflation_rates <- function(prices) {
  stopifnot(all(prices > 0))
  100 * (prices[-1] / prices[-length(prices)] - 1)
}

rates <- lapply(paths, inflation_rates)
for (name in names(rates)) {
  cat(name, paste(sprintf("%.4f%%", rates[[name]]), collapse = ", "), "\n")
}
stopifnot(isTRUE(all.equal(unname(rates$A_one_step), c(4, 0, 0), tolerance = 1e-10)))
stopifnot(isTRUE(all.equal(
  unname(rates$B_delayed), c(2, 100 * (104 / 102 - 1), 0),
  tolerance = 1e-10
)))
stopifnot(isTRUE(all.equal(unname(rates$C_persistent), c(4, 4, 4), tolerance = 1e-10)))
cat("All illustrative inflation calculations passed.\n")
