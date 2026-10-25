"""Reproduce the illustrative price-level examples in the BOJ oil-shock explainer.

These paths are hypothetical. They are not Japanese CPI observations and not
forecasts implied by an oil-price model.
"""
PATHS = {
    "A_one_step": [100.0, 104.0, 104.0, 104.0],
    "B_delayed": [100.0, 102.0, 104.0, 104.0],
    "C_persistent": [100.0, 104.0, 108.16, 112.4864],
}


def inflation_rates(price_index):
    """Period-over-period percentage changes of a positive price index."""
    assert all(p > 0 for p in price_index)
    return [
        100.0 * (price_index[t] / price_index[t - 1] - 1.0)
        for t in range(1, len(price_index))
    ]


def main():
    out = {name: inflation_rates(path) for name, path in PATHS.items()}
    for name, rates in out.items():
        print(name, ", ".join(f"{x:.4f}%" for x in rates))
    assert all(abs(a - b) < 1e-10 for a, b in zip(out["A_one_step"], [4, 0, 0]))
    assert all(abs(a - b) < 1e-10 for a, b in zip(
        out["B_delayed"], [2, 100 * (104 / 102 - 1), 0]
    ))
    assert all(abs(a - b) < 1e-10 for a, b in zip(out["C_persistent"], [4, 4, 4]))
    print("All illustrative inflation calculations passed.")


if __name__ == "__main__":
    main()
