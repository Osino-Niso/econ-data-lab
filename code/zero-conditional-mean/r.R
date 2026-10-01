ols_slope <- function(x, y) {
  x_centered <- x - mean(x)
  sum(x_centered * (y - mean(y))) / sum(x_centered^2)
}

grouped_error_means <- function(x, u, groups = 5) {
  breaks <- quantile(x, probs = seq(0, 1, length.out = groups + 1))
  group_id <- cut(
    x,
    breaks = breaks,
    include.lowest = TRUE,
    labels = FALSE
  )

  data.frame(
    group = seq_len(groups),
    mean_x = as.numeric(tapply(x, group_id, mean)),
    mean_u = as.numeric(tapply(u, group_id, mean))
  )
}

n <- 100000

# Case 1: X and u are generated independently.
set.seed(42)
x_exo <- rnorm(n)
u_exo <- rnorm(n)
y_exo <- 2 + 3 * x_exo + u_exo

slope_exo <- ols_slope(x_exo, y_exo)
exo_groups <- grouped_error_means(x_exo, u_exo)

cat(sprintf("Exogenous OLS slope: %.4f\n", slope_exo))
cat(sprintf("Exogenous overall mean(u): %.4f\n", mean(u_exo)))
print(transform(exo_groups, mean_x = round(mean_x, 4), mean_u = round(mean_u, 4)))

# Case 2: an omitted variable z affects both X and Y.
# True model: Y = 2 + 3X + 2Z + epsilon
# If Z is omitted, u = 2Z + epsilon and E[u|X] is not zero.
set.seed(42)
z <- rnorm(n)
v <- rnorm(n, sd = 0.5)
epsilon <- rnorm(n)

x_endo <- z + v
u_endo <- 2 * z + epsilon
y_endo <- 2 + 3 * x_endo + u_endo

slope_endo <- ols_slope(x_endo, y_endo)
endo_groups <- grouped_error_means(x_endo, u_endo)

cat(sprintf("Endogenous OLS slope: %.4f\n", slope_endo))
cat(sprintf("Endogenous overall mean(u): %.4f\n", mean(u_endo)))
print(transform(endo_groups, mean_x = round(mean_x, 4), mean_u = round(mean_u, 4)))

# Minimal reproducibility checks.
stopifnot(abs(slope_exo - 3) < 0.03)
stopifnot(abs(mean(u_exo)) < 0.02)
stopifnot(max(abs(exo_groups$mean_u)) < 0.03)

stopifnot(slope_endo > 4.5, slope_endo < 4.7)
stopifnot(abs(mean(u_endo)) < 0.03)
stopifnot(endo_groups$mean_u[1] < -2.0)
stopifnot(endo_groups$mean_u[5] > 2.0)
