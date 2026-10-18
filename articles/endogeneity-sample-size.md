---
title: "標本数を増やせば内生性は解決する？ データを増やしてもOLSのズレが消えない理由"
emoji: "🎯"
type: "tech"
topics: ["econometrics", "statistics", "python", "r"]
published: false
---

計量経済学では、標本数が大きくなると推定が安定すると習います。

実際、標本数を増やせば、標本を取り直したときの推定値のばらつきは小さくなっていきます。

では、説明変数と誤差項が相関している、いわゆる**内生性**がある場合も、十分な量のデータを集めれば押し切れるのでしょうか。

結論から言うと、**押し切れません**。

内生性が残ったまま標本数だけを増やすと、推定値は「真値の周り」ではなく、**真値からずれた値の周りに、より狭く集まる**ことがあります。

この記事では、欠落変数によって内生性が生じる小さなモデルを使い、

- 標本数を増やすと何が改善するのか
- なぜ内生性によるズレは消えないのか
- 「ばらつきが小さい」と「真値に近い」はなぜ別なのか

を、数式とPython / Rのシミュレーションで確認します。

なお、この記事では単回帰に話を限定し、**説明変数 $X$ と誤差項 $u$ が相関する状態**を内生性と呼びます。

## 先に結論

ここでいう「真値2」は、後で設定する**元のデータ生成過程におけるXの係数**です。Zを省いた単回帰の母集団線形射影係数とは異なります。

また、標本数を増やしたときに推定量がある値へ確率的に近づくことを**確率収束**と呼び、$\hat\beta_n\xrightarrow{p}b$ と書きます。$\operatorname{plim}\hat\beta_n=b$ も同じ意味です。以下では前者に統一します。

## 先に結論

単回帰モデル

$$
Y=\beta_0+\beta_1X+u
$$

でOLSを使うと、傾きの推定量は

$$
\hat\beta_1
=
\beta_1
+
\frac{\sum_{i=1}^n (X_i-\bar X)u_i}
{\sum_{i=1}^n (X_i-\bar X)^2}
$$

と書けます。

分子・分母をそれぞれ $n$ で割ると、標本共分散と標本分散の比として読めます。独立同分布や有限のモーメントなど通常の大標本条件の下では、大数の法則によってこの比は

$$
\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}
$$

へ近づきます。

したがって、

$$
\operatorname{Cov}(X,u)\neq 0
$$

なら、

$$
\hat\beta_1\xrightarrow{p}
=
\beta_1
+
\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}
\neq \beta_1
$$

となります。

ここで重要なのは、標本数 $n$ を増やしても、

$$
\operatorname{Cov}(X,u)
$$

そのものが自動的に0になるわけではないことです。

データが増えるほど推定値の**ばらつき**は小さくなります。しかし、推定が向かう**中心**が間違っているなら、より大量のデータを使っても、その間違った中心の周りへ正確に集まっていきます。

## 1. 「標本数が増えると良くなる」の中身

まず、標本数が増えることの効果を分けて考えます。

同じ母集団から標本を何度も取り直してOLSを計算すると、毎回まったく同じ $\hat\beta_1$ が得られるわけではありません。

標本が違えば、推定値も少しずつ変わります。

標本数を増やすと、この**標本抽出による偶然のばらつき**は通常小さくなります。

これはとても重要な改善です。

しかし、ここから

> データを増やせば、どんな推定上の問題も解決する

とは言えません。

標本数を増やすことで主に減るのは、有限標本でのランダムな揺れです。

一方、説明変数と誤差項の間に系統的な関係が残っているなら、その関係は「データが少ないせいで偶然起きているもの」ではありません。

この違いを見るために、具体例を作ります。

## 2. 本当は $Z$ も効いているとする

本当のデータ生成過程が

$$
Y=1+2X+1.5Z+\varepsilon
$$

だったとします。

ここでは、$X$ の真の係数は

$$
\beta_X=2
$$

です。

ところが、分析者は $Z$ を観測できず、

$$
Y=\alpha+\beta X+u
$$

という単回帰だけを推定したとします。

このとき、単回帰の誤差項 $u$ には、落としてしまった $Z$ の影響が入ります。

$$
u=1.5Z+\varepsilon
$$

ここで、もし $X$ と $Z$ が無関係なら、$X$ と $u$ も相関しません。

しかし、$X$ と $Z$ が関連しているなら、$X$ は誤差項 $u$ とも関連してしまいます。

これが、欠落変数によって内生性が生じる基本的な形です。

以前の記事では、ゼロ条件付き平均

$$
E[u\mid X]=0
$$

の意味を扱いました。

https://zenn.dev/econ_data_lab/articles/zero-conditional-mean

今回の例では、$X$ と誤差項の間に系統的な関係を作ることで、OLSが真値へ収束しない状況を見ます。

## 3. 内生性がないケース

まずは比較用に、

$$
X=v
$$

とします。

$Z$, $v$, $\varepsilon$ は互いに独立で、すべて平均0、分散1の正規分布から生成するとします。

このとき、

$$
\operatorname{Cov}(X,Z)=0
$$

なので、

$$
\operatorname{Cov}(X,u)=0
$$

です。

したがって、大標本では

$$
\hat\beta\xrightarrow{p}2
$$

となります。

標本数を増やせば、推定値は真値2の周りへだんだん狭く集まるはずです。

## 4. 内生性があるケース

次に、$X$ を

$$
X=0.8Z+v
$$

として生成します。

すると、$X$ と $Z$ は正の相関を持ちます。

単回帰で $Z$ を落としたときの誤差項は

$$
u=1.5Z+\varepsilon
$$

なので、$X$ と $u$ も相関します。

実際、$Z$, $v$, $\varepsilon$ が互いに独立で分散1なら、

$$
\operatorname{Cov}(X,u)
=
\operatorname{Cov}(0.8Z+v,\ 1.5Z+\varepsilon)
=0.8\times1.5
=1.2
$$

です。

また、

$$
\operatorname{Var}(X)
=
0.8^2\operatorname{Var}(Z)+\operatorname{Var}(v)
=0.64+1
=1.64
$$

です。

したがって、OLSの傾きが大標本で向かう先は

$$
2+\frac{1.2}{1.64}
\approx 2.7317
$$

になります。

真値は2なのに、標本数をどれだけ増やしても、OLSは約2.73へ向かいます。

ここが今回の記事の中心です。

## 5. Pythonで1000回ずつ推定してみる

**図の読み方：** 横軸は推定された傾き、縦軸はその頻度です。真値2と、内生性がある場合の収束先約2.7317を縦線で示すと、標本数を増やしても後者の周りで分布が狭くなる様子が分かります。以下のコードを実行すれば、表だけでなくその図も生成できます。

$X$ の係数の真値を2に固定し、標本数を

- 50
- 500
- 5000

と増やします。

各標本数について1000回ずつデータを生成し、毎回 $Z$ を落とした単回帰を行います。

```python
import numpy as np

BETA_X = 2.0
GAMMA_Z = 1.5
RHO = 0.8
REPS = 1000
SAMPLE_SIZES = [50, 500, 5000]
SEED = 20261018


def ols_slope(x, y):
    x_centered = x - x.mean()
    return np.sum(x_centered * (y - y.mean())) / np.sum(x_centered**2)


def simulate_slope(rng, n, endogenous):
    z = rng.normal(size=n)
    v = rng.normal(size=n)
    epsilon = rng.normal(size=n)

    if endogenous:
        x = RHO * z + v
    else:
        x = v

    y = 1 + BETA_X * x + GAMMA_Z * z + epsilon
    return ols_slope(x, y)


rng = np.random.default_rng(SEED)

for n in SAMPLE_SIZES:
    for endogenous in [False, True]:
        estimates = np.array(
            [simulate_slope(rng, n, endogenous) for _ in range(REPS)]
        )

        scenario = "endogenous" if endogenous else "exogenous"
        print(
            scenario,
            n,
            estimates.mean(),
            estimates.std(ddof=1),
        )
```

実行すると、今回の乱数では次のようになりました。

| ケース | 標本数 $n$ | $\hat\beta$ の平均 | $\hat\beta$ の標準偏差 |
| --- | ---: | ---: | ---: |
| 内生性なし | 50 | 1.9932 | 0.2484 |
| 内生性あり | 50 | 2.7335 | 0.1757 |
| 内生性なし | 500 | 1.9985 | 0.0760 |
| 内生性あり | 500 | 2.7323 | 0.0523 |
| 内生性なし | 5000 | 2.0018 | 0.0254 |
| 内生性あり | 5000 | 2.7321 | 0.0165 |

この標準偏差は、推定量の標本分布の標準偏差（標準誤差）を1000回の反復で近似したものです。1回の回帰から計算する推定標準誤差とは区別してください。

見るべきなのは、**平均と標準偏差を分けること**です。

内生性なしでは、標本数を増やすと、

- 平均は真値2の近く
- 標準偏差は小さくなる

という動きになっています。

一方、内生性ありでは、

- 平均は約2.73のまま
- 標準偏差だけが小さくなる

という動きです。

つまり、標本数5000では推定値のばらつき自体はかなり小さくなっています。

しかし、その推定値は**間違った値の周りに非常に安定して集まっています**。


### 分布を描く

以下を上のPythonコードの末尾に追加してください。

```python
import matplotlib.pyplot as plt

rng_plot = np.random.default_rng(SEED)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=True)
for ax, n in zip(axes, SAMPLE_SIZES):
    estimates = [simulate_slope(rng_plot, n, True) for _ in range(REPS)]
    ax.hist(estimates, bins=35, density=True, alpha=0.65)
    ax.axvline(2, color="black", linestyle="--", label="True coefficient: 2")
    ax.axvline(2 + 1.2 / 1.64, color="red", linestyle=":", label="OLS limit: 2.7317")
    ax.set_xlim(1.5, 3.4)
    ax.set_title(f"n = {n}")
    ax.set_xlabel("Estimated slope")
axes[0].set_ylabel("Density")
axes[-1].legend(loc="upper left", fontsize=7)
fig.tight_layout()
plt.show()
```

図では、3つのパネルで**横軸の範囲を固定**しています。これにより、標本数が増えるほど分布が狭くなることを同じ尺度で比較できます。

## 6. Rでも同じことを確認する

:::details Rコードを開く

Rでも同じ実験ができます。

```r
BETA_X <- 2.0
GAMMA_Z <- 1.5
RHO <- 0.8
REPS <- 1000
SAMPLE_SIZES <- c(50, 500, 5000)
SEED <- 20261018

ols_slope <- function(x, y) {
  x_centered <- x - mean(x)
  sum(x_centered * (y - mean(y))) / sum(x_centered^2)
}

simulate_slope <- function(n, endogenous) {
  z <- rnorm(n)
  v <- rnorm(n)
  epsilon <- rnorm(n)

  if (endogenous) {
    x <- RHO * z + v
  } else {
    x <- v
  }

  y <- 1 + BETA_X * x + GAMMA_Z * z + epsilon
  ols_slope(x, y)
}

set.seed(SEED)

for (n in SAMPLE_SIZES) {
  for (endogenous in c(FALSE, TRUE)) {
    estimates <- replicate(REPS, simulate_slope(n, endogenous))
    scenario <- if (endogenous) "endogenous" else "exogenous"

    cat(sprintf(
      "%-12s %6d %9.4f %9.4f\n",
      scenario,
      n,
      mean(estimates),
      sd(estimates)
    ))
  }
}
```

RとPythonでは乱数生成器が違うため、有限回のシミュレーション結果は完全には一致しません。

それでも、標本数を増やすと

- 内生性なしでは2へ集中する
- 内生性ありでは約2.73へ集中する

という構造は同じです。

:::

## 7. 「ばらつきが小さい」と「一致している」は別

この例から分かるのは、推定値の評価には少なくとも2つの方向があるということです。

1つは、標本を取り直したときに推定値がどれくらい揺れるか。

もう1つは、推定値がそもそも真値を中心としているか、あるいは真値へ近づくかです。

今回の内生性ありのケースでは、標本数を増やすほど推定値の揺れは小さくなります。

しかし、真値2ではなく約2.73へ集まります。

したがって、

> 標準誤差が小さいから、推定値は正しい

とは言えません。

標準誤差が小さいことは、推定値が**精密**であることを示しても、その推定手続きが真値へ向かうことまで保証しません。

大量のデータによって、間違ったモデルから非常に安定した推定値が得られることもあります。

## 8. では、データを増やす意味はないのか

もちろん、そうではありません。

モデルの条件が適切で、OLSが一致する状況なら、標本数を増やすことには大きな意味があります。

今回言いたいのは、

> **標本数を増やすことと、内生性の原因を取り除くことは別の作業である**

ということです。

欠落変数が原因なら、適切な変数をモデルに入れられないか考える必要があります。

逆因果や同時決定など、単純に変数を追加するだけでは解決しない内生性もあります。その場合には、研究設計や操作変数法など、別の方法が必要になることがあります。

少なくとも、

> 「データが十分多いから、内生性は気にしなくてよい」

とは言えません。

## 9. よくある誤解

### 誤解1：標本数を増やせばバイアスも自動的に0になる

標本数を増やすだけでは、説明変数と誤差項の相関は消えません。

今回の例では、$n$ が大きくなるほど、OLSは約2.73へ安定していきます。

### 誤解2：推定値のばらつきが小さければ真値に近い

ばらつきの小ささと、真値へ向かうことは別です。

間違った中心の周りに狭く集まることもあります。

### 誤解3：大標本ならモデルの仮定を気にしなくてよい

大標本理論は、どんなモデルでも自動的に正しくしてくれる仕組みではありません。

むしろ、一致性を考えるときこそ、「推定量がどこへ収束するのか」を確認する必要があります。

## 10. 3問だけ確認

### Q1

説明変数と誤差項の相関が残っていても、標本数を無限に増やせばOLSは必ず真値へ収束する。

**○か×か。**

:::details 答え
×です。

今回の例では、真値2ではなく約2.73へ収束します。
:::

### Q2

真値が2で、標本数を増やすほど推定値が2.73付近へ狭く集まるようになったとします。

この結果から、「推定のばらつきは小さくなっている」と言えますか。また、「OLSは真値に一致している」と言えますか。

:::details 答え
ばらつきは小さくなっていると言えますが、真値2ではなく2.73付近へ集まっているので、一致しているとは言えません。
:::

### Q3

「標本数を増やすこと」と「内生性を解決すること」の違いを、自分の言葉で説明してみてください。

:::details 答えの例
標本数を増やすと標本抽出による偶然のばらつきは小さくなるが、説明変数と誤差項の系統的な相関は自動的には消えない。したがって、内生性がある場合は、その原因に応じてモデルや研究設計を見直す必要がある。
:::

## まとめ

今回のポイントは1つです。

> **データを増やすと推定は安定する。しかし、安定する先が真値とは限らない。**

内生性があり、

$$
\operatorname{Cov}(X,u)\neq0
$$

なら、OLSは

$$
\beta_1
+
\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}
$$

のような、真値とは異なる値へ向かうことがあります。

標本数を増やすほど、その間違った値の周りへのばらつきだけが小さくなることもあります。

「データが多い」と「推定方法が正しい」は別物です。

この区別ができると、一致性や内生性を学ぶ意味がかなり見えやすくなると思います。

## 再現コード

この記事のPython / RコードはGitHubにも置いています。

- Python: `code/endogeneity-sample-size/python.py`
- R: `code/endogeneity-sample-size/r.R`

## 参考資料

- 京都大学 環境マーケティング論分野「2SLS」  
  https://www.eeso.ges.kyoto-u.ac.jp/emm/materials/econometrics/2sls
- Jeffrey Grogger, *Economics 240B: Econometrics*（UC Berkeley, OLS problems with endogeneity）  
  https://www.ocf.berkeley.edu/~jeffreyg/240B.pdf
- MIT OpenCourseWare, *Lecture 21: Endogeneity and Instrument Variables*  
  https://ocw.mit.edu/courses/14-310x-data-analysis-for-social-scientists-spring-2023/resources/mit14_310x_s23_week10_lec21_pdf/
