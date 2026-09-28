p <- 0.3
x <- 0:1

# Probability mass of Bernoulli(p)
print(dbinom(x, size = 1, prob = p))

# Simulation
set.seed(0)

sample <- rbinom(
  n = 10000,
  size = 1,
  prob = p
)

print(mean(sample))
