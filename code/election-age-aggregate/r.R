# Age-composition scenarios: the 9%/7% values are pre-election
# online survey display rates (excluding undecided), NOT exit-poll facts.
# Historical age-voter counts are for the 2025 Yokohama mayoral election.
voters_2025_by_age <- c(
  "18-19"=22146, "20-24"=49101, "25-29"=56388,
  "30-34"=68476, "35-39"=77019,
  "40-44"=90537, "45-49"=109988
)
eligible_2025_young <- sum(c(65101, 186216, 200456, 192334, 197405))
total_voters_2025 <- 1292363
eligible_2026 <- 3108312
voters_2026 <- 1416233
valid_2026 <- 1398358
yamamoto_votes_2026 <- 49377
poll_18_39 <- 0.09
poll_40_49 <- 0.07

young_2025 <- sum(voters_2025_by_age[1:5])
forties_2025 <- sum(voters_2025_by_age[6:7])

reconstruction <- function(multiplier=1.0) {
  young_share <- young_2025/total_voters_2025 * multiplier
  forties_share <- forties_2025/total_voters_2025 * multiplier
  older_share <- 1-young_share-forties_share
  stopifnot(older_share > 0, older_share < 1)
  young_valid <- valid_2026 * young_share
  forties_valid <- valid_2026 * forties_share
  older_valid <- valid_2026 * older_share
  young_votes <- young_valid * poll_18_39
  forties_votes <- forties_valid * poll_40_49
  older_votes <- yamamoto_votes_2026 - young_votes - forties_votes
  older_rate <- older_votes / older_valid
  list(
    young_votes=young_votes, forties_votes=forties_votes,
    older_votes=older_votes, older_rate=older_rate,
    compatible=(older_rate >= 0 && older_rate <= 1)
  )
}

cat("2025 18-39 eligible:",eligible_2025_young,"\n")
cat("2025 18-39 voters:",young_2025,"\n")
cat("2025 40-49 voters:",forties_2025,"\n")
cat(sprintf("Naive eligible * 9%%: %.0f\n",eligible_2025_young*poll_18_39))
cat(sprintf("2026 actual: %d votes (%.4f%% of valid)\n",
            yamamoto_votes_2026,100*yamamoto_votes_2026/valid_2026))

for (scale in c(0.8, 1.0, 1.2)) {
  s <- reconstruction(scale)
  cat(sprintf(paste0("Age mix multiplier %.1f: 18-39 %.0f; ",
                     "40-49 %.0f; 50+ residual %.0f; ",
                     "50+ rate %.2f%%; compatible=%s\n"),
              scale, s$young_votes, s$forties_votes, s$older_votes,
              100*s$older_rate, s$compatible))
  stopifnot(abs(s$young_votes + s$forties_votes + s$older_votes -
                yamamoto_votes_2026) < 1e-8)
}

base <- reconstruction(1.0)
stopifnot(young_2025 == 273130, forties_2025 == 200525)
stopifnot(round(base$young_votes) == 26598)
stopifnot(round(base$forties_votes) == 15188)
stopifnot(round(base$older_votes) == 7591)
stopifnot(base$compatible, !reconstruction(1.2)$compatible)
