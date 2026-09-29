import numpy as np

p = 0.3

# Probability mass of Bernoulli(p)
values = np.array([0, 1])
probabilities = np.array([1 - p, p])

for value, probability in zip(values, probabilities):
    print(f"P(X={value}) = {probability}")

# One observation
rng = np.random.default_rng(0)
single = rng.binomial(n=1, p=p)
print("single draw =", single)

# Many observations
rng = np.random.default_rng(0)
sample = rng.binomial(n=1, p=p, size=10000)
sample_mean = sample.mean()

print("sample mean =", sample_mean)
print("share of 1s =", sample_mean)

# Minimal reproducibility checks
assert set(np.unique(sample)).issubset({0, 1})
assert abs(sample_mean - p) < 0.03
