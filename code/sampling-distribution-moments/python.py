from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mu = 100.0
sigma = 20.0
repetitions = 10_000
sample_sizes = [25, 100]

rng = np.random.default_rng(42)

results = {}
sample_means_by_n = {}

for n in sample_sizes:
    samples = rng.normal(
        loc=mu,
        scale=sigma,
        size=(repetitions, n),
    )

    sample_means = samples.mean(axis=1)
    sample_means_by_n[n] = sample_means

    empirical_mean = sample_means.mean()
    empirical_variance = sample_means.var(ddof=1)
    empirical_sd = sample_means.std(ddof=1)
    theoretical_variance = sigma**2 / n
    theoretical_se = sigma / np.sqrt(n)

    results[n] = {
        "mean": empirical_mean,
        "variance": empirical_variance,
        "sd": empirical_sd,
        "theoretical_variance": theoretical_variance,
        "theoretical_se": theoretical_se,
    }

    print(f"n = {n}")
    print(f"mean of sample means = {empirical_mean:.4f}")
    print(f"variance of sample means = {empirical_variance:.4f}")
    print(f"sd of sample means = {empirical_sd:.4f}")
    print(f"theoretical SE = {theoretical_se:.4f}")
    print()

for n in sample_sizes:
    assert abs(results[n]["mean"] - mu) < 0.2
    assert abs(results[n]["variance"] - results[n]["theoretical_variance"]) < 0.5
    assert abs(results[n]["sd"] - results[n]["theoretical_se"]) < 0.1

assert results[100]["sd"] < results[25]["sd"]

fig, ax = plt.subplots(figsize=(6.4, 3.8))
bins = np.linspace(84, 116, 65)

for n in sample_sizes:
    ax.hist(
        sample_means_by_n[n],
        bins=bins,
        density=True,
        histtype="step",
        linewidth=1.3,
        label=f"n = {n}",
    )

ax.axvline(mu, linestyle="--", linewidth=1.0, label="population mean")
ax.set_xlabel("sample mean")
ax.set_ylabel("density")
ax.set_title("Sampling distributions of the sample mean")
ax.legend()
fig.tight_layout()

plot_path = Path("images/sampling-distribution-moments.webp")
plot_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(plot_path, dpi=100)
plt.close(fig)

assert plot_path.exists()
print(f"saved plot = {plot_path}")
