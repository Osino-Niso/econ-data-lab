import numpy as np

sigma = 1.0
expected_next_gap = 0.0

# Expected real interest rate minus the natural rate of interest.
interest_gap = np.array([-0.02, -0.01, 0.00, 0.01, 0.02])

# New Keynesian IS curve:
# x_t = E_t[x_{t+1}] - (1 / sigma) * interest_gap
current_output_gap = expected_next_gap - interest_gap / sigma

print("real_interest_gap_pct  current_output_gap_pct")
for gap, output_gap in zip(interest_gap, current_output_gap):
    print(f"{gap * 100:>21.1f}  {output_gap * 100:>22.1f}")

expected = np.array([0.02, 0.01, 0.00, -0.01, -0.02])
assert np.allclose(current_output_gap, expected)
