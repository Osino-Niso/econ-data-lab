"""Generate two article figures, using the same simulation order as python.py.

Run: python code/endogeneity-sample-size/figures.py
Requires: numpy matplotlib pillow, and a Japanese sans-serif font.
"""
from pathlib import Path
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image
from python import BETA_X, GAMMA_Z, RHO, REPS, SAMPLE_SIZES, SEED, simulate_slope

OUT = Path(__file__).resolve().parents[2] / "images"
BLUE, ORANGE, NAVY = "#1479A8", "#DC6332", "#18344A"

def setup():
    names = {f.name for f in fm.fontManager.ttflist}
    font = next((f for f in ("Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic") if f in names), None)
    if font is None:
        raise RuntimeError("Japanese font required: install fonts-noto-cjk")
    plt.rcParams.update({"font.family": font, "axes.unicode_minus": False,
                         "text.color": NAVY, "axes.labelcolor": NAVY,
                         "xtick.color": NAVY, "ytick.color": NAVY, "font.size": 12,
                         "figure.facecolor": "white", "savefig.facecolor": "white"})
    OUT.mkdir(parents=True, exist_ok=True)
    print("Using font:", font)

def save(fig, filename):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=165, facecolor="white")
    buffer.seek(0)
    im = Image.open(buffer).convert("RGB")
    path = OUT / filename
    im.save(path, "WEBP", quality=87, method=6)
    print(path, im.size, path.stat().st_size, "bytes")
    plt.close(fig)

def kde(samples, grid):
    h = 1.06 * np.std(samples, ddof=1) * len(samples) ** (-1/5)
    u = (grid[:, None] - samples[None, :]) / h
    return np.exp(-.5*u*u).mean(axis=1) / (np.sqrt(2*np.pi)*h)

def distributions():
    rng = np.random.default_rng(SEED)
    target = BETA_X + GAMMA_Z*RHO/(RHO*RHO+1)
    grid = np.linspace(1.38, 3.42, 900)
    fig, axs = plt.subplots(3, 1, figsize=(8.3, 10.2), sharex=True,
                            gridspec_kw={"hspace": .47})
    fig.suptitle("標本数を増やすと、推定値はどこへ集まる？",
                 fontsize=20, fontweight="bold", y=.987)
    fig.text(.5,.948,"各条件1,000回・破線は理論的な収束先（青2／橙2.732）",
             ha="center",fontsize=12.0)
    for ax, n in zip(axs, SAMPLE_SIZES):
        # The ordering is intentionally identical to code/endogeneity-sample-size/python.py
        for endogenous, color, label in ((False,BLUE,"内生性なし"),
                                          (True,ORANGE,"内生性あり")):
            draws = np.array([simulate_slope(rng,n,endogenous) for _ in range(REPS)])
            print(n,label,f"{draws.mean():.4f}",f"{draws.std(ddof=1):.4f}")
            dens = kde(draws,grid)
            ax.fill_between(grid,dens,color=color,alpha=.18,lw=0)
            ax.plot(grid,dens,color=color,lw=2.65)
        for value, color in ((BETA_X,BLUE),(target,ORANGE)):
            ax.axvline(value,color=color,linestyle="--",lw=1.75,alpha=.94)
        ax.set_title(f"n = {n:,}",loc="left",fontweight="bold",fontsize=16,pad=8)
        ax.set_xlim(1.38,3.42)
        ax.set_xticks([1.5,2,2.5,3,3.4])
        ax.set_yticks([])
        ax.set_ylabel("密度",fontsize=11)
        ax.grid(axis="x",color="#DCE8EF",alpha=.85,lw=.9)
        ax.spines[["top","right","left"]].set_visible(False)
        ax.spines["bottom"].set_color("#B3C2CD")
        ax.tick_params(axis="x",labelbottom=True,labelsize=11)
    fig.legend(handles=[
        Line2D([],[],color=BLUE,lw=4,label="内生性なし"),
        Line2D([],[],color=ORANGE,lw=4,label="内生性あり")],
        loc="lower center",ncol=2,frameon=False,fontsize=12,
        bbox_to_anchor=(.5,.044))
    axs[-1].set_xlabel("推定された X の係数（傾き）",fontsize=13,labelpad=8)
    fig.subplots_adjust(left=.105,right=.96,top=.902,bottom=.168)
    save(fig,"endogeneity-sample-size-distributions.webp")
    assert abs(target-2.7317073170731705)<1e-12

def node(ax,x,y,w,h,label,face,edge,size=16):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,
        boxstyle="round,pad=0.022,rounding_size=.027",fc=face,ec=edge,lw=2))
    ax.text(x,y,label,ha="center",va="center",fontsize=size,
            color=NAVY,weight="bold")

def arrow(ax,a,b,color=NAVY,width=2.3,style="-|>",line="-"):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=18,
        lw=width,color=color,linestyle=line,connectionstyle="arc3,rad=0"))

def structure():
    fig=plt.figure(figsize=(8.3,9.5),facecolor="white")
    ax=fig.add_axes([.035,.02,.93,.94])
    ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis("off")
    ax.text(.5,.98,"Zを省略すると、何が起こる？",
            ha="center",va="top",fontsize=21,weight="bold")
    ax.text(.035,.917,"① データが生成される仕組み",
            ha="left",fontsize=15.5,weight="bold")
    ax.add_patch(FancyBboxPatch((.025,.502),.95,.387,
        boxstyle="round,pad=.01,rounding_size=.025",
        fc="#F5F9FB",ec="#D1DFE8",lw=1.1))
    node(ax,.225,.766,.25,.073,"Z（省略する変数）","#FFEDE4",ORANGE,13)
    node(ax,.67,.766,.18,.073,"X","#E8F5FA",BLUE,17)
    node(ax,.67,.605,.18,.073,"Y","#E9F1FA",NAVY,17)
    node(ax,.895,.766,.075,.065,"v","white","#A9BBC9",15)
    node(ax,.895,.605,.075,.065,"ε","white","#A9BBC9",15)
    arrow(ax,(.855,.766),(.77,.766),"#778C9A",1.75)
    arrow(ax,(.358,.766),(.559,.766),ORANGE)
    ax.text(.446,.790,"0.8",ha="center",fontsize=12,color=ORANGE)
    arrow(ax,(.67,.723),(.67,.647),BLUE)
    ax.text(.705,.693,"2",fontsize=12,color=BLUE)
    arrow(ax,(.297,.725),(.574,.63),ORANGE)
    ax.text(.41,.695,"1.5",fontsize=12,color=ORANGE)
    arrow(ax,(.854,.605),(.771,.605),"#778C9A",1.75)
    ax.text(.5,.535,"Y = 1 + 2X + 1.5Z + ε",ha="center",fontsize=14.5,
            bbox={"fc":"white","ec":"none","pad":6})
    ax.text(.035,.447,"② Zを落としたときに観察される関連",
            ha="left",fontsize=15.5,weight="bold")
    ax.add_patch(FancyBboxPatch((.025,.10),.95,.323,
        boxstyle="round,pad=.01,rounding_size=.025",
        fc="#FFF9F5",ec="#F2D7C8",lw=1.1))
    node(ax,.18,.305,.17,.077,"X","#E8F5FA",BLUE,18)
    node(ax,.77,.305,.17,.077,"Y","#E9F1FA",NAVY,18)
    node(ax,.48,.210,.30,.071,"u = 1.5Z + ε","#FFF0E5",ORANGE,15)
    # Lower panel depicts statistical association, NOT a causal X -> Y arrow.
    ax.add_patch(FancyArrowPatch((.275,.305),(.68,.305),
        arrowstyle="<->",mutation_scale=16,color=BLUE,lw=2.4,
        linestyle=(0,(4,3)),connectionstyle="arc3,rad=0"))
    ax.text(.50,.389,"XとYの単回帰：傾き ≈ 2.73",
            ha="center",fontsize=13.0,color=BLUE,weight="bold")
    # u enters the omitted-variable equation; do not draw a causal u -> Y arrow here.
    ax.add_patch(FancyArrowPatch((.225,.264),(.323,.219),
        arrowstyle="<->",mutation_scale=15,color="#8B4B70",lw=2.2,
        linestyle=(0,(3,3)),connectionstyle="arc3,rad=-.15"))
    ax.text(.095,.147,"Xとuは相関",color="#8B4B70",fontsize=12.4,ha="left")
    ax.text(.59,.121,"Zの寄与がuに入り、Xとuが相関する",
            ha="center",fontsize=12.3)
    ax.text(.5,.060,"上段の実線矢印＝仮定したデータ生成過程",
            ha="center",fontsize=12,color="#46606F")
    ax.text(.5,.035,"下段の点線両矢印＝統計的な関連（因果の矢印ではない）",
            ha="center",fontsize=11.5,color="#46606F")
    save(fig,"endogeneity-sample-size-structure.webp")

if __name__ == "__main__":
    setup()
    distributions()
    structure()
