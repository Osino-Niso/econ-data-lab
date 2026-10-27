# Artificial observationally equivalent wage-price models (A and B).
# This R run uses its own independent seeded random numbers.
set.seed(20261028)
n <- 5000
eps <- rnorm(n, mean = 0, sd = 0.7)
eps[1] <- 2
pa <- numeric(n); wa <- numeric(n)
pb <- numeric(n); wb <- numeric(n); sb <- numeric(n)
for (i in seq_len(n)) {
  lagwa <- if (i == 1) 0 else wa[i - 1]
  lag_sb <- if (i == 1) 0 else sb[i - 1]
  pa[i] <- 0.75 * lagwa + eps[i]
  wa[i] <- 0.8 * pa[i]
  sb[i] <- 0.6 * lag_sb + eps[i]
  pb[i] <- sb[i]
  wb[i] <- 0.8 * pb[i]
}
stopifnot(max(abs(pa - pb)) < 1e-10, max(abs(wa - wb)) < 1e-10)
slope_a <- unname(coef(lm(pa[-1] ~ wa[-n]))[2])
slope_b <- unname(coef(lm(pb[-1] ~ wb[-n]))[2])
stopifnot(abs(slope_a - slope_b) < 1e-10, abs(slope_a - 0.75) < 0.06)
cat(sprintf("Maximum price difference: %.3g\n", max(abs(pa - pb))))
cat(sprintf("OLS slope A = %.6f, B = %.6f\n", slope_a, slope_b))
cat("Counterfactual next-period price response for imposed wage +1pt:\n")
cat("Economy A: +0.75pt; Economy B: 0.00pt\n")

# Verify intervention impulse response with the same structural recursion.
h <- 9
resp_a <- numeric(h); resp_b <- numeric(h)
wresp_a <- numeric(h); wresp_b <- numeric(h); latent_b <- numeric(h)
wresp_a[1] <- 1; wresp_b[1] <- 1
for (i in 2:h) {
  resp_a[i] <- 0.75 * wresp_a[i - 1]
  wresp_a[i] <- 0.8 * resp_a[i]
  latent_b[i] <- 0.6 * latent_b[i - 1]
  resp_b[i] <- latent_b[i]
  wresp_b[i] <- 0.8 * resp_b[i]
}
expected <- c(0, 0.75 * (0.6 ^ (0:(h - 2))))
stopifnot(max(abs(resp_a - expected)) < 1e-12,
          max(abs(resp_b)) < 1e-12)
cat("Intervention response A:", paste(round(resp_a[1:5], 6), collapse=", "), "\n")
cat("Intervention response B:", paste(round(resp_b[1:5], 6), collapse=", "), "\n")
