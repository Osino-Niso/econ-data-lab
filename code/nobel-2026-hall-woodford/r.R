sigma <- 1.0
expected_next_gap <- 0.0

# Expected real interest rate minus the natural rate of interest.
interest_gap <- c(-0.02, -0.01, 0.00, 0.01, 0.02)

# New Keynesian IS curve:
# x_t = E_t[x_{t+1}] - (1 / sigma) * interest_gap
current_output_gap <- expected_next_gap - interest_gap / sigma

result <- data.frame(
  real_interest_gap_pct = interest_gap * 100,
  current_output_gap_pct = current_output_gap * 100
)
print(result)

expected <- c(0.02, 0.01, 0.00, -0.01, -0.02)
stopifnot(isTRUE(all.equal(current_output_gap, expected)))
