import numpy as np


def ols(x, y):
    x_centered = x - x.mean()
    slope = np.sum(x_centered * (y - y.mean())) / np.sum(x_centered**2)
    intercept = y.mean() - slope * x.mean()
    return intercept, slope


def grouped_error_means(x, u, groups=5):
    cuts = np.quantile(x, np.linspace(0, 1, groups + 1))
    group_id = np.digitize(x, cuts[1:-1])
    rows = []
    for i in range(groups):
        mask = group_id == i
        rows.append((i + 1, x[mask].mean(), u[mask].mean()))
    return rows


n = 100_000

# Case 1: X and u are generated independently.
rng = np.random.default_rng(42)
x_exo = rng.normal(size=n)
u_exo = rng.normal(size=n)
y_exo = 2 + 3 * x_exo + u_exo

_, slope_exo = ols(x_exo, y_exo)
exo_groups = grouped_error_means(x_exo, u_exo)

print(f"Exogenous OLS slope: {slope_exo:.4f}")
print(f"Exogenous overall mean(u): {u_exo.mean():.4f}")
for group, mean_x, mean_u in exo_groups:
    print(f"exo group {group}: mean(X)={mean_x:.4f}, mean(u)={mean_u:.4f}")

# Case 2: an omitted variable z affects both X and Y.
# True model: Y = 2 + 3X + 2Z + epsilon
# If Z is omitted, u = 2Z + epsilon and E[u|X] is not zero.
rng = np.random.default_rng(42)
z = rng.normal(size=n)
v = rng.normal(scale=0.5, size=n)
epsilon = rng.normal(size=n)

x_endo = z + v
u_endo = 2 * z + epsilon
y_endo = 2 + 3 * x_endo + u_endo

_, slope_endo = ols(x_endo, y_endo)
endo_groups = grouped_error_means(x_endo, u_endo)

print(f"Endogenous OLS slope: {slope_endo:.4f}")
print(f"Endogenous overall mean(u): {u_endo.mean():.4f}")
for group, mean_x, mean_u in endo_groups:
    print(f"endo group {group}: mean(X)={mean_x:.4f}, mean(u)={mean_u:.4f}")

# Minimal reproducibility checks.
assert abs(slope_exo - 3) < 0.03
assert abs(u_exo.mean()) < 0.02
assert max(abs(mean_u) for _, _, mean_u in exo_groups) < 0.03

assert 4.5 < slope_endo < 4.7
assert abs(u_endo.mean()) < 0.03
assert endo_groups[0][2] < -2.0
assert endo_groups[-1][2] > 2.0
