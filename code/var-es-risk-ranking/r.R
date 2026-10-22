# Risk ranking example. Returns and losses are in percentage points.
target_mean <- 2

distros <- function() {
  p <- 0.04; q <- 0.08; r <- 0.88; middle <- -5
  quadratic <- function(x) {
    good <- -(p * x + q * middle) / r
    p * x^2 + q * middle^2 + r * good^2 - 100
  }
  bad <- uniroot(quadratic, interval = c(-100, -10), tol = 1e-12)$root
  good <- -(p * bad + q * middle) / r
  list(
    A = list(ret = c(-10, 10) + target_mean, prob = c(0.5, 0.5)),
    B = list(ret = c(bad, middle, good) + target_mean, prob = c(p, q, r))
  )
}

metrics <- function(ret, prob, alpha = 0.95) {
  stopifnot(abs(sum(prob) - 1) < 1e-10)
  mu <- sum(prob * ret)
  sd <- sqrt(sum(prob * (ret - mu)^2))
  loss <- -ret
  asc <- order(loss)
  var <- loss[asc][which(cumsum(prob[asc]) >= alpha - 1e-12)[1]]
  remaining <- 1 - alpha
  es_total <- 0
  for (i in order(loss, decreasing = TRUE)) {
    take <- min(prob[i], remaining)
    es_total <- es_total + take * loss[i]
    remaining <- remaining - take
    if (remaining < 1e-12) break
  }
  c(mean = mu, sd = sd, VaR95 = var, ES95 = es_total / (1 - alpha))
}

results <- lapply(distros(), function(d) metrics(d$ret, d$prob))
for (name in names(results)) {
  cat(sprintf("%s  %s\n", name,
              paste(sprintf("%.4f", results[[name]]), collapse = "  ")))
}
stopifnot(all(abs(results$A[1:2] - c(2, 10)) < 1e-6))
stopifnot(all(abs(results$B[1:2] - c(2, 10)) < 1e-6))
stopifnot(abs(results$A["VaR95"] - 8) < 1e-6)
stopifnot(abs(results$B["VaR95"] - 3) < 1e-6)
stopifnot(abs(results$B["ES95"] - 37.34538341093389) < 1e-5)
stopifnot(results$A["VaR95"] > results$B["VaR95"])
stopifnot(results$A["ES95"] < results$B["ES95"])
cat("Checks passed.\n")
