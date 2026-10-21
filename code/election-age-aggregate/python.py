"""Why aggregate vote counts do not identify age-specific vote shares.

All small-table allocations are hypothetical. Official Yokohama 2026 figures
are used only to check the citywide valid-vote share.
No external libraries or network access required.
"""
TOTAL_VALID_BALLOTS = 1_398_358
YAMAMOTO_VOTES = 49_377

YOUNG_VALID_BALLOTS = 400
OLDER_VALID_BALLOTS = 600
CANDIDATE_BALLOTS = 100

SCENARIOS = {
    "A (young: 80, older: 20)": (80, 20),
    "B (young: 10, older: 90)": (10, 90),
}


def feasible_young_bounds(young, older, votes):
    assert 0 <= votes <= young + older
    return max(0, votes - older), min(votes, young)


def main():
    assert TOTAL_VALID_BALLOTS == 1_398_358
    assert YAMAMOTO_VOTES == 49_377
    citywide = YAMAMOTO_VOTES / TOTAL_VALID_BALLOTS * 100
    print(f"Official citywide valid-vote share: {citywide:.4f}%")
    print("Hypothetical example: 1,000 valid ballots, 100 for candidate A")
    print("18-39: 400 ballots; 40+: 600 ballots")
    for label, (young_votes, older_votes) in SCENARIOS.items():
        assert young_votes + older_votes == CANDIDATE_BALLOTS
        assert 0 <= young_votes <= YOUNG_VALID_BALLOTS
        assert 0 <= older_votes <= OLDER_VALID_BALLOTS
        print(
            f"{label}: age 18-39 = "
            f"{young_votes / YOUNG_VALID_BALLOTS * 100:.2f}%, "
            f"age 40+ = {older_votes / OLDER_VALID_BALLOTS * 100:.2f}%"
        )

    lo, hi = feasible_young_bounds(
        YOUNG_VALID_BALLOTS, OLDER_VALID_BALLOTS, CANDIDATE_BALLOTS
    )
    print(f"Feasible age 18-39 candidate votes: {lo} to {hi}")
    print(
        f"Feasible age 18-39 valid-vote share: "
        f"{lo / YOUNG_VALID_BALLOTS * 100:.2f}% to "
        f"{hi / YOUNG_VALID_BALLOTS * 100:.2f}%"
    )
    assert (lo, hi) == (0, 100)
    assert abs(citywide - 3.5310) < 0.001


if __name__ == "__main__":
    main()
