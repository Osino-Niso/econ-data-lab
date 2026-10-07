from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

quarters = np.array([
    "2023Q1", "2023Q2", "2023Q3", "2023Q4",
    "2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1",
])

sa_index = np.array([
    103.5, 104.8, 103.3, 104.4,
    99.0, 101.1, 101.4, 101.8, 101.5,
])

original_index = np.array([
    104.0, 102.4, 102.7, 106.5,
    99.9, 99.0, 100.9, 104.9, 100.9,
])

qoq = np.full(sa_index.shape, np.nan, dtype=float)
qoq[1:] = (sa_index[1:] / sa_index[:-1] - 1) * 100

yoy = np.full(original_index.shape, np.nan, dtype=float)
yoy[4:] = (original_index[4:] / original_index[:-4] - 1) * 100

mask = ~np.isnan(yoy)
view_quarters = quarters[mask]
view_qoq = qoq[mask]
view_yoy = yoy[mask]

print("quarter  qoq  yoy")
for quarter, qoq_value, yoy_value in zip(
    view_quarters,
    view_qoq,
    view_yoy,
):
    print(f"{quarter:>7} {qoq_value:5.1f} {yoy_value:5.1f}")

fig, ax = plt.subplots(figsize=(7.2, 4.2))

ax.plot(
    view_quarters,
    view_qoq,
    marker="o",
    linewidth=1.7,
    label="QoQ (seasonally adjusted)",
)
ax.plot(
    view_quarters,
    view_yoy,
    marker="o",
    linewidth=1.7,
    label="YoY (original series)",
)
ax.axhline(0, linestyle="--", linewidth=1.0)
ax.set_xlabel("Quarter")
ax.set_ylabel("Percent change (%)")
ax.set_title("Industrial Production: QoQ vs YoY", pad=12)
ax.set_ylim(-5.8, 2.8)
ax.grid(axis="y", alpha=0.25)
ax.legend(loc="lower right")

for target in ["2024Q2", "2025Q1"]:
    i = list(view_quarters).index(target)
    y = max(view_qoq[i], view_yoy[i])
    ax.annotate(
        f"QoQ {view_qoq[i]:+.1f}% / YoY {view_yoy[i]:+.1f}%",
        xy=(view_quarters[i], y),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=8,
    )

fig.tight_layout()

output_path = Path("images/qoq-vs-yoy-iip.webp")
output_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output_path, dpi=160)
plt.close(fig)

print(f"plot = {output_path}")
