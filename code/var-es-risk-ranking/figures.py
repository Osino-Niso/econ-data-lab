"""Draw reproducible figures for the VaR/ES article (PNG, Zenn-ready)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from python import distributions, metrics

OUT = Path(__file__).resolve().parents[2] / "images"
OUT.mkdir(exist_ok=True)
D = distributions()
BLUE = "#3176b5"
ORANGE = "#e07a45"
RED = "#bd423e"

# Figure 1: discrete probability masses. The x positions are outcome
# categories, NOT a continuous return scale.
fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.9), sharey=True)
for a, (name, (returns, prob)) in zip(ax, D.items()):
    bars = a.bar(np.arange(len(prob)), 100 * prob,
                 color=BLUE if name == "A" else ORANGE, width=0.62)
    a.set_xticks(np.arange(len(prob)))
    a.set_xticklabels([f"{v:+.2f}%" for v in returns], fontsize=10)
    a.set_title(f"Investment {name}", fontsize=16, weight="bold")
    a.set_ylim(0, 105)
    a.set_ylabel("Probability (%)")
    a.set_xlabel("Return outcomes (categories)")
    a.spines[["top", "right"]].set_visible(False)
    for bar, p in zip(bars, prob):
        a.text(bar.get_x() + bar.get_width()/2, bar.get_height()+2,
               f"{p:.0%}", ha="center", fontsize=12, weight="bold")
    mean, sd, *_ = metrics(returns, prob)
    a.text(0.5, 0.96, f"Mean {mean:.0f}%   SD {sd:.0f}%",
           transform=a.transAxes, ha="center", va="top", fontsize=11)
fig.suptitle("Equal mean and SD, different probability distributions",
             fontsize=16, weight="bold", y=1.03)
fig.tight_layout()
fig.savefig(OUT / "var-es-risk-ranking-distributions.png",
            dpi=175, bbox_inches="tight")
plt.close(fig)

# Figure 2: represent exactly 5 percentage points of tail probability.
# Bar lengths are probability mass, not loss magnitude.
fig, ax = plt.subplots(figsize=(11.5, 4.7))
ax.barh("Investment A", 5, color=BLUE, height=0.43)
ax.barh("Investment B", 1, color=ORANGE, height=0.43)
ax.barh("Investment B", 4, left=1, color=RED, height=0.43)
ax.text(2.5, 0, "5% probability: 10% loss", ha="center", va="center",
        color="white", fontsize=11, weight="bold")
ax.text(0.5, 1, "1%", ha="center", va="center", fontsize=12, weight="bold")
ax.text(3, 1, "4% probability: 47.93% loss", ha="center", va="center",
        color="white", fontsize=11, weight="bold")
ax.set_xlim(0, 5)
ax.set_xlabel("Percentage points of the worst 5% outcomes")
ax.invert_yaxis()
ax.set_title("What is inside the worst 5% of losses?",
             fontsize=17, weight="bold", pad=20)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)
fig.text(0.5, 0.04,
         "A: VaR95 10%, ES95 10%     |     B: VaR95 5%, ES95 39.35%",
         ha="center", fontsize=13, weight="bold")
fig.text(0.5, 0.11, "B orange segment (1%): 5% loss",
         ha="center", fontsize=10)
fig.subplots_adjust(bottom=0.25, top=0.81, left=0.18, right=0.97)
fig.savefig(OUT / "var-es-risk-ranking-tail.png",
            dpi=175, bbox_inches="tight")
plt.close(fig)
print("Generated figures in", OUT)
