"""Generate two reader-friendly Japanese figures for the VaR/ES draft.
Run: python code/var-es-risk-ranking/figures.py from the repository root.
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'images'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(HERE))
from python import distributions, metrics  # noqa: E402

names=[p.name for p in font_manager.fontManager.ttflist]
if 'Noto Sans CJK JP' in names:
    plt.rcParams['font.family']='Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.size']=11

D=distributions()
colors={'A':'#215d9c','B':'#bc5726'}
fig, axes=plt.subplots(2,1,figsize=(10.9,7.8),sharex=True)
for ax,(name,(r,p)) in zip(axes,D.items()):
    x=r
    height=p*100
    ax.vlines(x,0,height,color=colors[name],linewidth=3,alpha=.9)
    ax.scatter(x,height,s=110,color=colors[name],zorder=3)
    for xi,yi in zip(x,height):
        ax.annotate(f'{yi:.0f}%',(xi,yi),xytext=(0,8),textcoords='offset points',ha='center',fontsize=11,weight='bold')
    mean,sd,*_=metrics(r,p)
    ax.set_title(f'投資{name} ｜ 期待リターン {mean:.0f}% ・ 標準偏差 {sd:.0f}%',fontsize=14,loc='left',pad=15)
    ax.set_ylim(0,108)
    ax.set_ylabel('発生確率（%）')
    ax.grid(axis='y',alpha=.16)
    ax.spines[['right','top']].set_visible(False)
    ax.set_yticks([0,25,50,75,100])
    for xi,yi in zip(x,height):
        ax.text(xi,30 if yi < 20 else 12,f'{xi:+.2f}%',ha='center',va='bottom',fontsize=10,color=colors[name])
axes[-1].set_xlim(-52,18)
axes[-1].set_xticks([-50,-40,-30,-20,-10,0,10])
axes[-1].set_xlabel('一期間のリターン（%）',labelpad=11)
fig.suptitle('平均と標準偏差が同じでも、分布の形は違う',fontsize=18,weight='bold',y=.995)
fig.subplots_adjust(hspace=.48,left=.10,right=.97,top=.89,bottom=.10)
fig.savefig(OUT/'var-es-risk-ranking-distributions.png',dpi=180)
plt.close(fig)

fig,ax=plt.subplots(figsize=(10.8,4.4))
ax.barh('投資A',5,height=.46,color='#215d9c')
ax.barh('投資B',1,height=.46,color='#e8a04c')
ax.barh('投資B',4,left=1,height=.46,color='#bc4935')
ax.invert_yaxis()
ax.set_xlim(0,5)
ax.set_xlabel('「最悪5%」に含める確率（パーセントポイント）')
ax.set_title('最悪5%の内訳を比べる',loc='left',fontsize=18,weight='bold',pad=22)
ax.text(2.5,0,'8%損失を5%分',ha='center',va='center',color='white',weight='bold',fontsize=12)
ax.text(.5,1,'3%損失\n1%分',ha='center',va='center',color='#202020',fontsize=10)
ax.text(3,1,'約45.93%損失を4%分',ha='center',va='center',color='white',weight='bold',fontsize=11)
ax.grid(axis='x',alpha=.16)
ax.set_axisbelow(True)
ax.spines[['top','right','left']].set_visible(False)
fig.text(.5,.085,'VaR（A 8% / B 3%）　　ES（A 8% / B 約37.35%）',ha='center',fontsize=12,weight='bold')
fig.subplots_adjust(top=.76,bottom=.29,left=.13,right=.96)
fig.savefig(OUT/'var-es-risk-ranking-tail.png',dpi=180)
plt.close(fig)
print('Created two figures in',OUT)
