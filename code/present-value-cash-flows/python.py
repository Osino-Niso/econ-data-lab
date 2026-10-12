from math import isclose


def present_value(cash_flow: float, t: int, rate: float) -> float:
    """Return the present value of a cash flow received t periods later."""
    return cash_flow / (1 + rate) ** t


# Example 1: three 100-unit cash flows at years 1, 2, and 3.
rate = 0.05
cash_flows = [100.0, 100.0, 100.0]
pv_values = [
    present_value(cf, t, rate)
    for t, cf in enumerate(cash_flows, start=1)
]

print("Example 1: nominal total vs present value")
for t, (cf, pv) in enumerate(zip(cash_flows, pv_values), start=1):
    print(f"year {t}: CF={cf:.2f}, PV={pv:.2f}")

nominal_total = sum(cash_flows)
pv_total = sum(pv_values)
print(f"nominal total: {nominal_total:.2f}")
print(f"present value total: {pv_total:.2f}")

# Example 2: same nominal total, different timing.
rate = 0.10
project_a = present_value(70.0, 1, rate) + present_value(50.0, 2, rate)
project_b = present_value(50.0, 1, rate) + present_value(70.0, 2, rate)

print("\nExample 2: same nominal total, different timing")
print(f"project A PV: {project_a:.2f}")
print(f"project B PV: {project_b:.2f}")
print(f"difference: {project_a - project_b:.2f}")

# Example 3: NPV with an initial investment of 100 and two future inflows of 60.
npv = -100.0 + present_value(60.0, 1, rate) + present_value(60.0, 2, rate)
print("\nExample 3: NPV")
print(f"NPV: {npv:.2f}")

# Minimal reproducibility checks used by GitHub Actions.
assert isclose(nominal_total, 300.0, abs_tol=1e-12)
assert isclose(pv_total, 272.3248029370478, rel_tol=1e-12)
assert project_a > project_b
assert isclose(project_a, 104.9586776859504, rel_tol=1e-12)
assert isclose(project_b, 103.30578512396693, rel_tol=1e-12)
assert isclose(npv, 4.132231404958667, rel_tol=1e-12)
