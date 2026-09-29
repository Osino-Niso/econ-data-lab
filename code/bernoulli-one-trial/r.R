p <- 0.3
x <- 0:1

# Probability mass of Bernoulli(p)
print(dbinom(x, size = 1, prob = p))

# One observation
set.seed(0)
single <- rbinom(
  n = 1,
  size = 1,
  prob = p
)
print(single)

# Many observations
set.seed(0)
sample <- rbinom(
  n = 10000,
  size = 1,
  prob = p
)
sample_mean <- mean(sample)

print(sample_mean)

# Minimal reproducibility checks
stopifnot(all(sample %in% c(0, 1)))
stopifnot(abs(sample_mean - p) < 0.03)
