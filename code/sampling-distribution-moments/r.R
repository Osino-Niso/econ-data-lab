mu <- 100
sigma <- 20
repetitions <- 10000

set.seed(42)

results <- list()

for (n in c(25, 100)) {
  sample_means <- replicate(
    repetitions,
    mean(rnorm(n, mean = mu, sd = sigma))
  )

  empirical_mean <- mean(sample_means)
  empirical_variance <- var(sample_means)
  empirical_sd <- sd(sample_means)
  theoretical_se <- sigma / sqrt(n)

  results[[as.character(n)]] <- list(
    mean = empirical_mean,
    variance = empirical_variance,
    sd = empirical_sd,
    theoretical_se = theoretical_se
  )

  cat("n =", n, "\n")
  cat(sprintf("mean of sample means = %.4f\n", empirical_mean))
  cat(sprintf("variance of sample means = %.4f\n", empirical_variance))
  cat(sprintf("sd of sample means = %.4f\n", empirical_sd))
  cat(sprintf("theoretical SE = %.4f\n\n", theoretical_se))
}

stopifnot(abs(results[["25"]]$mean - mu) < 0.2)
stopifnot(abs(results[["25"]]$variance - sigma^2 / 25) < 0.5)
stopifnot(abs(results[["25"]]$sd - sigma / sqrt(25)) < 0.1)

stopifnot(abs(results[["100"]]$mean - mu) < 0.2)
stopifnot(abs(results[["100"]]$variance - sigma^2 / 100) < 0.5)
stopifnot(abs(results[["100"]]$sd - sigma / sqrt(100)) < 0.1)

stopifnot(results[["100"]]$sd < results[["25"]]$sd)
