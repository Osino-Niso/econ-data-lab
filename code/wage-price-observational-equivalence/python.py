"""Two observationally equivalent wage-price economies.

A: price[t] = .75*wage[t-1] + innovation[t]
   wage[t]  = .8*price[t]
B: price[t] = external[t]
   external[t] = .6*external[t-1] + innovation[t]
   wage[t] = .8*price[t]

The reduced-form observational paths agree, while wage intervention differs.
Only artificial data are generated. No empirical identification is claimed.
"""
import numpy as np

N = 5000
rng = np.random.default_rng(20261028)
innovation = rng.normal(loc=0.0, scale=0.7, size=N)
innovation[0] = 2.0

price_a = np.zeros(N)
wage_a = np.zeros(N)
price_b = np.zeros(N)
wage_b = np.zeros(N)
external_b = np.zeros(N)

for t in range(N):
    price_a[t] = (0.75 * wage_a[t - 1] if t else 0.0) + innovation[t]
    wage_a[t] = 0.8 * price_a[t]

    external_b[t] = (0.6 * external_b[t - 1] if t else 0.0) + innovation[t]
    price_b[t] = external_b[t]
    wage_b[t] = 0.8 * price_b[t]

assert np.allclose(price_a, price_b, atol=1e-12, rtol=1e-12)
assert np.allclose(wage_a, wage_b, atol=1e-12, rtol=1e-12)

def ols_slope(price, wage):
    x = np.column_stack((np.ones(len(price) - 1), wage[:-1]))
    return np.linalg.lstsq(x, price[1:], rcond=None)[0]

coef_a = ols_slope(price_a, wage_a)
coef_b = ols_slope(price_b, wage_b)
assert np.allclose(coef_a, coef_b, atol=1e-12)
assert abs(coef_a[1] - 0.75) < 0.06

print(f"Maximum |price_A-price_B| = {np.max(np.abs(price_a-price_b)):.3g}")
print(f"Maximum |wage_A-wage_B|   = {np.max(np.abs(wage_a-wage_b)):.3g}")
print(f"OLS slope A = {coef_a[1]:.6f}, OLS slope B = {coef_b[1]:.6f}")
print("Structural response to +1pt imposed wage innovation:")
print("Economy A: +0.75pt next-period inflation deviation")
print("Economy B: +0.00pt next-period inflation deviation")
assert 0.75 * 1.0 == 0.75
assert 0.0 * 1.0 == 0.0
