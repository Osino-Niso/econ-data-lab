from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BETA_X = 2.0
GAMMA_Z = 1.5
RHO = 0.8
REPS = 1000
SAMPLE_SIZES = [50, 500, 5000]
SEED = 20261018

# Match Var(X) across the exogenous and endogenous cases.
X_SD = np.sqrt(1 + RHO**2)


def ols_slope(x, y):
    x_centered = x - x.mean()
    return np.sum(x_centered * (y - y.mean())) / np.sum(x_centered**2)


def simulate_slope(rng, n, endogenous):
    z = rng.normal(size=n)
    v = rng.normal(size=n)
    epsilon = rng.normal(size=n)

    if endogenous:
        x = RHO * z + v
    else:
        x = X_SD * v

    y = 1 + BETA_X * x + GAMMA_Z * z + epsilon
    return ols_slope(x, y)


def main():
    rng = np.random.default_rng(SEED)
    theoretical_limit = BETA_X + GAMMA_Z * RHO / (RHO**2 + 1)

    estimates_by_case = {}

    print(f"Target beta_x in the data-generating process: {BETA_X:.4f}")
    print(f"Endogenous-case probability limit: {theoretical_limit:.4f}")
    print()
    print(f"{'scenario':<12} {'n':>6} {'mean':>9} {'sd':>9}")

    for n in SAMPLE_SIZES:
        for endogenous in [False, True]:
            estimates = np.array(
                [simulate_slope(rng, n, endogenous) for _ in range(REPS)]
            )
            estimates_by_case[(n, endogenous)] = estimates

            scenario = "endogenous" if endogenous else "exogenous"
            print(
                f"{scenario:<12} {n:>6} "
                f"{estimates.mean():>9.4f} "
                f"{estimates.std(ddof=1):>9.4f}"
            )

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    bins = np.linspace(1.7, 3.2, 121)

    for n in SAMPLE_SIZES:
        ax.hist(
            estimates_by_case[(n, True)],
            bins=bins,
            density=True,
            histtype="step",
            linewidth=1.4,
            label=f"n = {n}",
        )

    ax.axvline(
        BETA_X,
        linestyle="--",
        linewidth=1.2,
        label="target = 2.0",
    )
    ax.axvline(
        theoretical_limit,
        linestyle=":",
        linewidth=1.5,
        label=f"OLS limit ≈ {theoretical_limit:.2f}",
    )
    ax.set_xlabel("OLS slope estimate")
    ax.set_ylabel("density")
    ax.set_title(
        "Endogenous OLS: larger samples concentrate around the wrong target"
    )
    ax.legend()

    fig.tight_layout()

    output_path = Path("images/endogeneity-sample-size.webp")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    main()
