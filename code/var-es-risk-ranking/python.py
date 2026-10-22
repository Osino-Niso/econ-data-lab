"""Reproduce the discrete return example used by the VaR/ES article.

Returns, standard deviations, VaR and ES are expressed in percent (not fractions).
Only NumPy is required.
"""
import numpy as np

EXPECTED_RETURN = 2.0
STANDARD_DEVIATION = 10.0
CONFIDENCE = 0.95


def distributions():
    a = (np.array([-8.0, 12.0]), np.array([0.50, 0.50]))
    p, q, r = 0.04, 0.08, 0.88
    # Work with excess returns relative to the targeted 2% mean.
    middle_c = -5.0
    roots = np.roots([
        p + p**2 / r,
        2 * p * q * middle_c / r,
        q * middle_c**2 + (q * middle_c)**2 / r - STANDARD_DEVIATION**2,
    ])
    bad_c = float(min(roots))
    good_c = -(p * bad_c + q * middle_c) / r
    b = (
        np.array([bad_c, middle_c, good_c]) + EXPECTED_RETURN,
        np.array([p, q, r]),
    )
    return {"A": a, "B": b}


def metrics(returns, probs, alpha=CONFIDENCE):
    returns, probs = np.asarray(returns), np.asarray(probs)
    assert len(returns) == len(probs)
    assert all(probs >= 0) and np.isclose(probs.sum(), 1)
    assert 0 < alpha < 1
    mean = float(np.dot(returns, probs))
    sd = float(np.sqrt(np.dot(probs, (returns - mean)**2)))
    losses = -returns
    order_asc = np.argsort(losses)
    var = float(losses[order_asc][np.searchsorted(
        np.cumsum(probs[order_asc]), alpha, side='left')])
    mass_to_select = 1 - alpha
    weighted_loss = 0.0
    for ix in np.argsort(losses)[::-1]:
        selected = min(float(probs[ix]), mass_to_select)
        weighted_loss += selected * float(losses[ix])
        mass_to_select -= selected
        if mass_to_select < 1e-12:
            break
    es = weighted_loss / (1 - alpha)
    return mean, sd, var, es


def main():
    result = {}
    print('Scenario, mean, sd, VaR95, ES95 (all values in %)')
    for label, (ret, prob) in distributions().items():
        result[label] = metrics(ret, prob)
        print(label, [round(x, 6) for x in result[label]])
        print('return outcomes:', [round(float(x), 6) for x in ret])
        print('probabilities:', prob.tolist())
    assert np.allclose(result['A'], [2, 10, 8, 8], atol=1e-10)
    assert np.allclose(result['B'], [2, 10, 3, 37.34538341093389], atol=1e-10)
    assert result['A'][2] > result['B'][2] and result['A'][3] < result['B'][3]
    # Translation invariance: shifting returns by +2 keeps SD and changes losses by -2.
    for label, (ret, prob) in distributions().items():
        zero_mean = metrics(ret - 2, prob)
        positive_mean = metrics(ret, prob)
        assert np.allclose(positive_mean, [zero_mean[0] + 2, zero_mean[1],
                                           zero_mean[2] - 2, zero_mean[3] - 2])
    print('All checks passed.')


if __name__ == '__main__':
    main()
