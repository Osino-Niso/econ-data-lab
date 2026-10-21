# Aggregate votes cannot uniquely identify age-specific candidate shares.
# Small scenarios below are completely hypothetical.
# Official 2026 Yokohama figures are used only for the citywide share.
total_valid_ballots <- 1398358
yamamoto_votes <- 49377

young_valid_ballots <- 400
older_valid_ballots <- 600
candidate_ballots <- 100

cat(sprintf("Official citywide valid-vote share: %.4f%%\n",
            100 * yamamoto_votes / total_valid_ballots))
cat("Hypothetical example: 1,000 valid ballots, 100 for candidate A\n")
cat("18-39: 400 ballots; 40+: 600 ballots\n")

scenarios <- matrix(c(80, 20, 10, 90), ncol=2, byrow=TRUE)
rownames(scenarios) <- c("A (young: 80, older: 20)",
                         "B (young: 10, older: 90)")
stopifnot(all(rowSums(scenarios) == candidate_ballots))
stopifnot(all(scenarios[, 1] <= young_valid_ballots))
stopifnot(all(scenarios[, 2] <= older_valid_ballots))

for (i in seq_len(nrow(scenarios))) {
  cat(sprintf("%s: age 18-39 = %.2f%%, age 40+ = %.2f%%\n",
              rownames(scenarios)[i],
              100 * scenarios[i, 1] / young_valid_ballots,
              100 * scenarios[i, 2] / older_valid_ballots))
}

lo <- max(0, candidate_ballots - older_valid_ballots)
hi <- min(candidate_ballots, young_valid_ballots)
cat(sprintf("Feasible age 18-39 candidate votes: %d to %d\n", lo, hi))
cat(sprintf("Feasible age 18-39 valid-vote share: %.2f%% to %.2f%%\n",
            100 * lo / young_valid_ballots,
            100 * hi / young_valid_ballots))
stopifnot(lo == 0, hi == 100)
stopifnot(abs(100 * yamamoto_votes / total_valid_ballots - 3.5310) < 0.001)
