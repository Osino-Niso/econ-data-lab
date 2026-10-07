quarters <- c(
  "2023Q1", "2023Q2", "2023Q3", "2023Q4",
  "2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1"
)

sa_index <- c(
  103.5, 104.8, 103.3, 104.4,
  99.0, 101.1, 101.4, 101.8, 101.5
)

original_index <- c(
  104.0, 102.4, 102.7, 106.5,
  99.9, 99.0, 100.9, 104.9, 100.9
)

qoq <- c(
  NA,
  (sa_index[-1] / sa_index[-length(sa_index)] - 1) * 100
)

yoy <- c(
  rep(NA, 4),
  (original_index[5:length(original_index)] /
    original_index[1:(length(original_index) - 4)] - 1) * 100
)

result <- data.frame(
  quarter = quarters,
  qoq = qoq,
  yoy = yoy
)

view <- result[!is.na(result$yoy), ]
view$qoq <- round(view$qoq, 1)
view$yoy <- round(view$yoy, 1)

print(view, row.names = FALSE)
