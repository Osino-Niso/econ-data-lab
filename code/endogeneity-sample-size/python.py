import numpy as np

BETA_X = 2.0
GAMMA_Z = 1.5
RHO = 0.8
REPS = 1000
SAMPLE_SIZES = [50, 500, 5000]
SEED = 20261018


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
        x = v

    y = 1 + BETA_X * x + GAMMA_Z * z + epsilon
    return ols_slope(x, y)


def main():
    rng = np.random.default_rng(SEED)

    theoretical_limit = BETA_X + GAMMA_Z * RHO / (RHO**2 + 1)

    print(f"True beta_x: {BETA_X:.4f}")
    print(f"Endogenous-case probability limit: {theoretical_limit:.4f}")
    print()
    print(f"{'scenario':<12} {'n':>6} {'mean':>9} {'sd':>9}")

    for n in SAMPLE_SIZES:
        for endogenous in [False, True]:
            estimates = np.array(
                [simulate_slope(rng, n, endogenous) for _ in range(REPS)]
            )

            scenario = "endogenous" if endogenous else "exogenous"
            print(
                f"{scenario:<12} {n:>6} "
                f"{estimates.mean():>9.4f} "
                f"{estimates.std(ddof=1):>9.4f}"
            )


if __name__ == "__main__":
    main()
