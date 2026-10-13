evaluate <- function(name, nominal_rate, expected_inflation, natural_rate,
                     sigma = 1.0, expected_next_gap = 0.0,
                     beta = 0.99, kappa = 0.10) {
  expected_real_rate <- nominal_rate - expected_inflation
  interest_gap <- expected_real_rate - natural_rate
  output_gap <- expected_next_gap - interest_gap / sigma
  inflation <- beta * expected_inflation + kappa * output_gap

  stance <- if (interest_gap > 1e-12) {
    "tightening"
  } else if (interest_gap < -1e-12) {
    "easing"
  } else {
    "neutral"
  }

  data.frame(
    scenario = name,
    real_rate_pct = expected_real_rate * 100,
    rate_gap_pct = interest_gap * 100,
    output_gap_pct = output_gap * 100,
    inflation_pct = inflation * 100,
    stance = stance
  )
}

result <- rbind(
  evaluate("baseline", 0.03, 0.02, 0.01),
  evaluate("rate_hike", 0.04, 0.02, 0.01),
  evaluate("nominal_up_but_expectations_up_more", 0.04, 0.035, 0.01)
)

print(result, row.names = FALSE)

stopifnot(abs(result$rate_gap_pct[2] - result$rate_gap_pct[1] - 1.0) < 1e-10)
stopifnot(abs(result$output_gap_pct[2] - result$output_gap_pct[1] + 1.0) < 1e-10)
stopifnot(result$output_gap_pct[2] < 0)
stopifnot(result$inflation_pct[2] > 0)
stopifnot(result$rate_gap_pct[3] < 0)
stopifnot(result$output_gap_pct[3] > 0)
stopifnot(result$stance[3] == "easing")
