"""Age-composition scenarios for the 2026 Yokohama mayoral election.

The October 9 online poll (9% at 18-39; 7% at 40s) is NOT an
election-day exit poll. Rates here are counterfactual inputs, not
estimates of actual age-specific ballots.

Source of 2025 age-specific voter counts: Yokohama Election Commission,
"Survey of election awareness" (2025 mayoral election), appendix II-1-1.
Source of 2026 totals: Yokohama Election Commission election result PDF.
No third-party libraries or external data downloads required.
"""

VOTERS_2025_BY_AGE = {
    "18-19": 22_146,
    "20-24": 49_101,
    "25-29": 56_388,
    "30-34": 68_476,
    "35-39": 77_019,
    "40-44": 90_537,
    "45-49": 109_988,
}
ELIGIBLE_2025_YOUNG = (65_101 + 186_216 + 200_456 + 192_334 + 197_405)
TOTAL_VOTERS_2025 = 1_292_363

ELIGIBLE_2026 = 3_108_312
VOTERS_2026 = 1_416_233
VALID_2026 = 1_398_358
YAMAMOTO_VOTES_2026 = 49_377

# Values READ FROM a rounded age chart of a *pre-election online survey*,
# excluding undecided respondents. Subgroup sample sizes not available.
POLL_18_39 = 0.09
POLL_40_49 = 0.07


def reconstruction(age_mix_multiplier=1.0):
    young_2025 = sum(list(VOTERS_2025_BY_AGE.values())[:5])
    forties_2025 = sum(list(VOTERS_2025_BY_AGE.values())[5:])
    young_share = young_2025 / TOTAL_VOTERS_2025 * age_mix_multiplier
    forties_share = forties_2025 / TOTAL_VOTERS_2025 * age_mix_multiplier
    older_share = 1 - young_share - forties_share
    assert 0 < older_share < 1
    young_valid = VALID_2026 * young_share
    forties_valid = VALID_2026 * forties_share
    older_valid = VALID_2026 * older_share
    young_votes = young_valid * POLL_18_39
    forties_votes = forties_valid * POLL_40_49
    required_older_votes = YAMAMOTO_VOTES_2026 - young_votes - forties_votes
    required_older_rate = required_older_votes / older_valid
    return {
        "young_valid": young_valid,
        "forties_valid": forties_valid,
        "older_valid": older_valid,
        "young_votes": young_votes,
        "forties_votes": forties_votes,
        "required_older_votes": required_older_votes,
        "required_older_rate": required_older_rate,
        "is_compatible": 0 <= required_older_rate <= 1,
    }


def main():
    young_eligible_2025 = ELIGIBLE_2025_YOUNG
    young_voters_2025 = sum(list(VOTERS_2025_BY_AGE.values())[:5])
    forties_voters_2025 = sum(list(VOTERS_2025_BY_AGE.values())[5:])
    print("Data from 2025 election (NOT 2026 age turnout):")
    print("18-39 eligible:", young_eligible_2025)
    print("18-39 voters:", young_voters_2025)
    print("40-49 voters:", forties_voters_2025)
    print("2025 total voters:", TOTAL_VOTERS_2025)
    print()
    print("Naive 2025 eligible * pre-election 9%:", round(young_eligible_2025 * POLL_18_39))
    print("Actual Yamamoto votes in 2026:", YAMAMOTO_VOTES_2026)
    print("Actual citywide valid-ballot share: {:.4f}%".format(
        100 * YAMAMOTO_VOTES_2026 / VALID_2026
    ))
    print()
    print("Scenario: 2025 voter age composition also applies to 2026 valid ballots")
    for scale in (0.8, 1.0, 1.2):
        s = reconstruction(scale)
        print(
            f"Age-mix multiplier {scale:.1f}: "
            f"18-39 {s['young_votes']:,.0f} ballots; "
            f"40-49 {s['forties_votes']:,.0f} ballots; "
            f"50+ residual {s['required_older_votes']:,.0f} ballots; "
            f"required 50+ rate {100*s['required_older_rate']:.2f}%; "
            f"compatible={s['is_compatible']}"
        )
        total = (s["young_votes"] + s["forties_votes"] +
                 s["required_older_votes"])
        assert abs(total - YAMAMOTO_VOTES_2026) < 1e-8

    base = reconstruction()
    assert young_eligible_2025 == 841_512
    assert young_voters_2025 == 273_130
    assert forties_voters_2025 == 200_525
    assert round(base["young_votes"]) == 26_598
    assert round(base["forties_votes"]) == 15_188
    assert round(base["required_older_votes"]) == 7_591
    assert base["is_compatible"]
    assert not reconstruction(1.2)["is_compatible"]


if __name__ == "__main__":
    main()
