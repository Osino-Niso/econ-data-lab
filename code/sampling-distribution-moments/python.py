import numpy as np

mu = 100.0
sigma = 20.0
repetitions = 10_000

rng = np.random.default_rng(42)

results = {}

for n in [25, 100]:
    samples = rng.normal(
        loc=mu,
        scale=sigma,
        size=(repetitions, n),
    )

    sample_means = samples.mean(axis=1)
    empirical_mean = sample_means.mean()
    empirical_variance = sample_means.var(ddof=0)
    empirical_sd = sample_means.std(ddof=0)
    theoretical_se = sigma / np.sqrt(n)

    results[n] = {
        "mean": empirical_mean,
        "variance": empirical_variance,
        "sd": empirical_sd,
        "theoretical_se": theoretical_se,
    }

    print(f"n = {n}")
    print(f"mean of sample means = {empirical_mean:.4f}")
    print(f"variance of sample means = {empirical_variance:.4f}")
    print(f"sd of sample means = {empirical_sd:.4f}")
    print(f"theoretical SE = {theoretical_se:.4f}")
    print()

assert abs(results[25]["mean"] - mu) < 0.2
assert abs(results[25]["variance"] - sigma**2 / 25) < 0.5
assert abs(results[25]["sd"] - sigma / np.sqrt(25)) < 0.1

assert abs(results[100]["mean"] - mu) < 0.2
assert abs(results[100]["variance"] - sigma**2 / 100) < 0.5
assert abs(results[100]["sd"] - sigma / np.sqrt(100)) < 0.1

assert results[100]["sd"] < results[25]["sd"]
