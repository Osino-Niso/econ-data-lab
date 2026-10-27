"""Generate two reproducible, artificial-model figures for the Zenn article.

No Japanese fonts required in GitHub Actions. Japanese explanations are in
the captions. Both models use the same numerical innovations and initial state.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.facecolor": "white",
})

N = 10
shock = np.zeros(N)
shock[0] = 2.0
pi_a = np.zeros(N)
w_a = np.zeros(N)
pi_b = np.zeros(N)
w_b = np.zeros(N)
s_b = np.zeros(N)

for t in range(N):
    pi_a[t] = (0.75 * w_a[t - 1] if t else 0.0) + shock[t]
    w_a[t] = 0.8 * pi_a[t]
    s_b[t] = (0.6 * s_b[t - 1] if t else 0.0) + shock[t]
    pi_b[t] = s_b[t]
    w_b[t] = 0.8 * pi_b[t]

np.testing.assert_allclose(pi_a, pi_b, atol=1e-12, rtol=0)
np.testing.assert_allclose(w_a, w_b, atol=1e-12, rtol=0)
np.testing.assert_allclose(pi_a[:4], [2.0, 1.2, 0.72, 0.432], atol=1e-12)
np.testing.assert_allclose(w_a[:4], [1.6, 0.96, 0.576, 0.3456], atol=1e-12)

x = np.arange(N)
blue, orange = "#2766AD", "#D47A2A"
fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8), sharex=True)
fig.suptitle("Same observations, different mechanisms", y=0.97, fontsize=17, weight="bold")
for ax, lhs, rhs, title in zip(axes, [pi_a, w_a], [pi_b, w_b], ["Price inflation", "Nominal wage growth"]):
    ax.plot(x, lhs, color=blue, linewidth=4.3, alpha=0.55, label="Economy A")
    ax.plot(x, rhs, color=orange, linewidth=1.9, linestyle="--",
            marker="o", markersize=5.6, markerfacecolor="white", markeredgewidth=1.6,
            label="Economy B")
    ax.set_title(title, pad=13)
    ax.set_xlabel("Periods after one-time shock")
    ax.set_ylabel("Extra growth rate (pp)")
    ax.set_xlim(-0.2, N - 0.8)
    ax.set_ylim(-0.10, 2.22)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.grid(axis="y", color="#E3E8EF", linewidth=0.85)
axes[1].legend(loc="upper right", fontsize=10, frameon=False)
fig.text(0.5, 0.012, "A and B overlap in both series; all quantities are simulated.",
         ha="center", fontsize=10, color="#52616F")
fig.tight_layout(rect=[0, 0.055, 1, 0.92], w_pad=2.4)
path1 = OUT / "wage-price-observational-path.png"
fig.savefig(path1, dpi=165)
plt.close(fig)

T = 9
time = np.arange(T)
response_a = np.zeros(T)
response_a[1:] = 0.75 * np.power(0.6, np.arange(T - 1))
response_b = np.zeros(T)
assert response_a[1] == 0.75 and np.isclose(response_a[2], 0.45)
assert np.all(response_b == 0)

fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.plot(time, response_a, color=blue, linewidth=2.7, marker="o",
        markersize=7, label="Economy A: wage feedback")
ax.plot(time, response_b, color=orange, linewidth=2.4, linestyle="--",
        marker="s", markersize=5.5, label="Economy B: external persistence")
ax.annotate("+0.75 pp", (1, 0.75), xytext=(1.3, 0.82),
            fontsize=11, color=blue, weight="bold")
ax.annotate("+0.45 pp", (2, 0.45), xytext=(2.3, 0.52),
            fontsize=11, color=blue)
ax.set(title="Intervention separates the two mechanisms",
       xlabel="Periods after one-time wage intervention",
       ylabel="Price-inflation response (pp)",
       xlim=(-0.2, T - 0.8), ylim=(-0.08, 1.03))
ax.set_xticks(time)
ax.grid(axis="y", color="#E3E8EF", linewidth=0.85)
ax.legend(loc="upper right", fontsize=10, frameon=False)
fig.tight_layout(pad=1.8)
path2 = OUT / "wage-price-wage-intervention.png"
fig.savefig(path2, dpi=165)
plt.close(fig)
for p in (path1, path2):
    assert p.exists() and 10000 < p.stat().st_size < 3_000_000, (p, p.stat().st_size)
    print(f"Generated {p} ({p.stat().st_size:,} bytes)")
