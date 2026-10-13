from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    nominal_rate: float
    expected_inflation: float
    natural_rate: float
    sigma: float = 1.0
    expected_next_gap: float = 0.0
    beta: float = 0.99
    kappa: float = 0.10


def evaluate(s: Scenario):
    expected_real_rate = s.nominal_rate - s.expected_inflation
    interest_gap = expected_real_rate - s.natural_rate
    output_gap = s.expected_next_gap - interest_gap / s.sigma
    inflation = s.beta * s.expected_inflation + s.kappa * output_gap
    stance = "tightening" if interest_gap > 1e-12 else "easing" if interest_gap < -1e-12 else "neutral"
    return expected_real_rate, interest_gap, output_gap, inflation, stance


scenarios = [
    Scenario("baseline", 0.03, 0.02, 0.01),
    Scenario("rate_hike", 0.04, 0.02, 0.01),
    Scenario("nominal_up_but_expectations_up_more", 0.04, 0.035, 0.01),
]

print("scenario                              real_rate  rate_gap  output_gap  inflation  stance")
for scenario in scenarios:
    real_rate, rate_gap, output_gap, inflation, stance = evaluate(scenario)
    print(
        f"{scenario.name:<37}"
        f"{real_rate * 100:>9.2f}%"
        f"{rate_gap * 100:>10.2f}%"
        f"{output_gap * 100:>12.2f}%"
        f"{inflation * 100:>11.2f}%  {stance}"
    )

# A one percentage-point nominal-rate increase with unchanged expected inflation
# raises the expected real rate and pushes the output gap down by one point
# when sigma = 1 and the expected future output gap is zero.
_, gap_base, x_base, _, _ = evaluate(scenarios[0])
_, gap_hike, x_hike, pi_hike, _ = evaluate(scenarios[1])
assert abs((gap_hike - gap_base) - 0.01) < 1e-12
assert abs((x_hike - x_base) + 0.01) < 1e-12

# A negative output gap is only downward pressure on inflation.
# Here inflation is still positive because expected future inflation is positive.
assert x_hike < 0
assert pi_hike > 0

# A higher nominal rate need not be tighter if expected inflation rises even more.
_, gap_expectations, x_expectations, _, stance_expectations = evaluate(scenarios[2])
assert gap_expectations < 0
assert x_expectations > 0
assert stance_expectations == "easing"
