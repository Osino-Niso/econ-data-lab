import numpy as np

p = 0.3

# Probability mass of Bernoulli(p)
values = np.array([0, 1])
probabilities = np.array([1 - p, p])

for value, probability in zip(values, probabilities):
    print(f"P(X={value}) = {probability}")

# Simulation
rng = np.random.default_rng(0)
x = rng.binomial(n=1, p=p, size=10000)

print("sample mean =", x.mean())
print("share of 1s =", x.mean())
