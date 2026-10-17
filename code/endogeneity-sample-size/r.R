BETA_X <- 2.0
GAMMA_Z <- 1.5
RHO <- 0.8
REPS <- 1000
SAMPLE_SIZES <- c(50, 500, 5000)
SEED <- 20261018

# Match Var(X) across the exogenous and endogenous cases.
X_SD <- sqrt(1 + RHO^2)

ols_slope <- function(x, y) {
  x_centered <- x - mean(x)
  sum(x_centered * (y - mean(y))) / sum(x_centered^2)
}

simulate_slope <- function(n, endogenous) {
  z <- rnorm(n)
  v <- rnorm(n)
  epsilon <- rnorm(n)

  if (endogenous) {
    x <- RHO * z + v
  } else {
    x <- X_SD * v
  }

  y <- 1 + BETA_X * x + GAMMA_Z * z + epsilon
  ols_slope(x, y)
}

set.seed(SEED)

theoretical_limit <- BETA_X + GAMMA_Z * RHO / (RHO^2 + 1)

cat(sprintf("Target beta_x in the data-generating process: %.4f\n", BETA_X))
cat(sprintf("Endogenous-case probability limit: %.4f\n\n", theoretical_limit))
cat(sprintf("%-12s %6s %9s %9s\n", "scenario", "n", "mean", "sd"))

for (n in SAMPLE_SIZES) {
  for (endogenous in c(FALSE, TRUE)) {
    estimates <- replicate(REPS, simulate_slope(n, endogenous))
    scenario <- if (endogenous) "endogenous" else "exogenous"

    cat(sprintf(
      "%-12s %6d %9.4f %9.4f\n",
      scenario,
      n,
      mean(estimates),
      sd(estimates)
    ))
  }
}
