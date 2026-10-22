"""Analytic example for VaR/ES ranking reversal. Returns and losses are in percent."""
import numpy as np

TAIL = 0.05


def distributions():
    a = (np.array([-10.0, 10.0]), np.array([0.5, 0.5]))
    p, q, r = 0.04, 0.08, 0.88
    middle = -5.0
    # Let bad return x, good return z. Impose E[R] = 0 and Var(R) = 100.
    # z = -(p*x + q*middle)/r; solve variance as a quadratic in x.
    roots = np.roots([
        p + p**2 / r,
        2 * p * q * middle / r,
        q * middle**2 + (q * middle)**2 / r - 100.0,
    ])
    bad = float(min(roots))
    good = -(p * bad + q * middle) / r
    b = (np.array([bad, middle, good]), np.array([p, q, r]))
    return {"A": a, "B": b}


def metrics(returns, probs, alpha=0.95):
    assert np.isclose(probs.sum(), 1)
    mean = float(np.dot(returns, probs))
    sd = float(np.sqrt(np.dot(probs, (returns - mean) ** 2)))
    losses = -returns
    asc = np.argsort(losses)
    cdf = np.cumsum(probs[asc])
    var = float(losses[asc][np.searchsorted(cdf, alpha, side="left")])
    # Average the worst 1-alpha fraction. Trim atoms at the boundary.
    remain = 1 - alpha
    es_mass = 0.0
    for idx in np.argsort(losses)[::-1]:
        mass = min(float(probs[idx]), remain)
        es_mass += mass * float(losses[idx])
        remain -= mass
        if remain < 1e-12:
            break
    es = es_mass / (1 - alpha)
    return mean, sd, var, es


def main():
    print("Scenario   E[R]      SD       VaR95      ES95   (all %)")
    values = {}
    for name, (returns, probs) in distributions().items():
        values[name] = metrics(returns, probs)
        print(f"{name:>4}   " + "  ".join(f"{v:9.4f}" for v in values[name]))
        print("        returns:", [round(v, 6) for v in returns])
        print("        probs  :", probs.tolist())
    a, b = values["A"], values["B"]
    assert np.allclose(a[:2], [0.0, 10.0])
    assert np.allclose(b[:2], [0.0, 10.0], atol=1e-10)
    assert np.allclose(a[2:], [10.0, 10.0])
    assert np.isclose(b[2], 5.0)
    assert np.isclose(b[3], 39.34538341093389)
    assert a[2] > b[2] and a[3] < b[3]
    print("Checks passed: VaR and ES ranking reversal.")


if __name__ == "__main__":
    main()
