present_value <- function(cash_flow, t, rate) {
  cash_flow / (1 + rate)^t
}

# Example 1: three 100-unit cash flows at years 1, 2, and 3.
rate <- 0.05
cash_flows <- c(100, 100, 100)
times <- 1:3
pv_values <- mapply(
  present_value,
  cash_flows,
  times,
  MoreArgs = list(rate = rate)
)

cat("Example 1: nominal total vs present value\n")
for (i in seq_along(times)) {
  cat(sprintf("year %d: CF=%.2f, PV=%.2f\n", times[i], cash_flows[i], pv_values[i]))
}

nominal_total <- sum(cash_flows)
pv_total <- sum(pv_values)
cat(sprintf("nominal total: %.2f\n", nominal_total))
cat(sprintf("present value total: %.2f\n", pv_total))

# Example 2: same nominal total, different timing.
rate <- 0.10
project_a <- present_value(70, 1, rate) + present_value(50, 2, rate)
project_b <- present_value(50, 1, rate) + present_value(70, 2, rate)

cat("\nExample 2: same nominal total, different timing\n")
cat(sprintf("project A PV: %.2f\n", project_a))
cat(sprintf("project B PV: %.2f\n", project_b))
cat(sprintf("difference: %.2f\n", project_a - project_b))

# Example 3: NPV with an initial investment of 100 and two future inflows of 60.
npv <- -100 + present_value(60, 1, rate) + present_value(60, 2, rate)
cat("\nExample 3: NPV\n")
cat(sprintf("NPV: %.2f\n", npv))

# Minimal reproducibility checks used by GitHub Actions.
stopifnot(abs(nominal_total - 300) < 1e-12)
stopifnot(abs(pv_total - 272.3248029370478) < 1e-10)
stopifnot(project_a > project_b)
stopifnot(abs(project_a - 104.9586776859504) < 1e-10)
stopifnot(abs(project_b - 103.30578512396693) < 1e-10)
stopifnot(abs(npv - 4.132231404958667) < 1e-10)
