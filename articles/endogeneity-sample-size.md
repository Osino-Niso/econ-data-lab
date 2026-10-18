---
title: "標本数を増やせば内生性は解決する？ データを増やしてもOLSのズレが消えない理由"
emoji: "🎯"
type: "tech"
topics: ["econometrics", "statistics", "python", "r"]
published: false
---

計量経済学では、標本数が大きくなると推定が安定すると習います。では、説明変数と誤差項が相関する**内生性**があっても、データを十分に集めれば問題を解決できるのでしょうか。

この記事では、欠落変数によって内生性が生じる小さなモデルを使い、

- 標本数を増やすと何が改善するのか
- なぜ内生性によるズレは消えないのか
- 「ばらつきが小さい」と「真値に近い」はなぜ別なのか

を、数式とPython / Rのシミュレーションで確認します。

想定読者は、単回帰OLSと分散・共分散を一度学んだ方です。数式は本文で順を追って確認します。

なお、この記事では単回帰に話を限定し、説明変数 $X$ と誤差項 $u$ が**相関する状態**を内生性と呼びます。

## 先に結論

**標本数を増やして減るのは、主に推定値の偶然のばらつきです。** 説明変数と誤差項の相関（内生性）は、データを増やすだけでは消えません。

この記事の「真値2」とは、後で設定する元のデータ生成過程における $X$ の**構造係数**です。一方、$Z$ を省いて単回帰したOLSが大標本で向かう値は、条件によって異なります。この2つを区別するのが目標です。

標本数 $n$ を増やすとOLSの推定量 $\hat\beta$ がある値 $b$ に確率的に近づくことを**確率収束**といい、$\hat\beta\xrightarrow{p}b$ と書きます。$\hat\beta$ は $n$ 個のデータから計算した傾きで、標本数によって変わります。

## 1. 「標本数が増えると良くなる」の中身

同じ母集団から標本を何度も取り直してOLSの傾きを計算すると、標本ごとに推定値は変わります。標本数を増やすと、この推定値の分布は通常狭くなります。

ただし、**分布の幅**と**分布が集まる位置**は別です。この2つを、変数を1つ省いた単回帰で比べます。

## 2. 本当は $Z$ も効いているとする

次のようなデータ生成過程を考えます。

$$
Y=1+2X+1.5Z+\varepsilon
$$

$Y$ は結果を表す変数、$X$ は係数を知りたい説明変数、$Z$ はもう1つの説明変数、$\varepsilon$ は残りのランダムな要因です。定数項は1です。

例えば、$X$ を教育年数、$Y$ を賃金、$Z$ を学習意欲だと考えてみてください。学習意欲が高い人ほど教育年数が長く、賃金にも学習意欲が関係するなら、$Z$ を省いた単回帰には教育年数だけでなく学習意欲との関連も混ざります。これは仕組みを想像するための例であり、実際の教育年数・賃金についてこの因果構造や数値が成り立つと主張するものではありません。

ここで知りたいのは、元の式における $X$ の**構造係数** $\beta_X=2$ です。この式を構造的な生成過程として仮定するなら、$Z$ と $\varepsilon$ を一定に保って $X$ を1増やしたとき、$Y$ は2増えます。

ところが、分析者は $Z$ を説明変数に入れず、$Y$ を $X$ だけに**切片つきOLS**で回帰するとします。OLSから得られる傾きを $\hat\beta$ と書きます。

省略した部分をまとめて、

$$
u=1.5Z+\varepsilon
$$

と置くと、元の式は $Y=1+2X+u$ になります。ここでの構造係数2と、$Z$ を省いたOLSで得る $\hat\beta$ は**同じとは限りません**。$X$ と $Z$ が関連すると、今回の設定では $X$ と $u$ が相関するからです。

なお、$u$ は省略した要因を含む**モデルの誤差項**であり、OLS推定後に計算する**残差** $\hat e_i=Y_i-\hat\alpha-\hat\beta X_i$ とは別物です（$\hat\alpha$ は推定された切片）。切片つきOLSでは残差と $X$ の標本共分散がゼロになりますが、それで $\operatorname{Cov}(X,u)=0$ になるわけではありません。

このように、関連する変数を落として誤差項に組み込むことで、内生性が生じる場合があります。

以前の記事では、ゼロ条件付き平均 $E[u\mid X]=0$ の意味を扱いました。

https://zenn.dev/econ_data_lab/articles/zero-conditional-mean

ここでは、$X$ と $u$ の相関がOLSの収束先にどう影響するかを計算します。

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

つまり今回は、$X$ と $u$ の共分散が1.2、$X$ の分散が1.64です。

これらの数値がなぜOLSのズレを決めるのでしょうか。次の節で、推定量の式から確認します。

## 5. なぜOLSは構造係数からずれるのか：式で確認

切片つき単回帰OLSの傾きは、

$$
\hat\beta
=\frac{\sum_{i=1}^n(X_i-\bar X)(Y_i-\bar Y)}
{\sum_{i=1}^n(X_i-\bar X)^2}
$$

です。$i$ は観測番号、$\bar X$ と $\bar Y$ は標本平均です。ここに $Y_i=1+2X_i+u_i$ を代入すると、定数項は差を取ると消えるので、

$$
\hat\beta
=2+\frac{\sum_{i=1}^n(X_i-\bar X)u_i}
{\sum_{i=1}^n(X_i-\bar X)^2}
$$

となります。$\sum_i(X_i-\bar X)=0$ なので、分子の $u_i$ は $(u_i-\bar u)$ に置き換えても同じです。分子・分母をともに $n$ で割ると、

$$
\hat\beta
=2+
\frac{\frac1n\sum_{i=1}^n(X_i-\bar X)(u_i-\bar u)}
{\frac1n\sum_{i=1}^n(X_i-\bar X)^2}
$$

です。右の分数は、$X$ と $u$ の**標本共分散**を $X$ の**標本分散**で割ったものです（いずれも分母を $n$ とする定義）。

観測が独立同分布で2次モーメントが有限、$\operatorname{Var}(X)>0$ などの条件が成り立てば、大数の法則から標本の共分散・分散は母集団の値へ近づきます。したがって、

$$
\hat\beta\xrightarrow{p}
2+\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}
$$

となります。$X$ と $u$ の共分散がゼロなら構造係数2へ、ゼロでなければ別の値へ向かいます。

今回の内生性ありの設定では、

$$
\hat\beta\xrightarrow{p}
2+\frac{1.2}{1.64}
\approx 2.7317
$$

です。これは、$Z$ を省いた単回帰が大標本で向かう値であって、元の生成過程の構造係数2ではありません。

第2節の教育年数（$X$）・賃金（$Y$）・学習意欲（$Z$）という仮想例では、教育年数と関連する学習意欲の寄与が、省略後の誤差項 $u$ を通して単回帰の傾きに混ざることに対応します。今回の式では $\operatorname{Cov}(X,u)=1.5\operatorname{Cov}(X,Z)$ であり、その混ざり方が右辺の $\operatorname{Cov}(X,u)/\operatorname{Var}(X)$ に表れています。これは仮定したモデルの説明であり、現実の教育・賃金の因果効果を示すものではありません。

### 約2.73は「意味のない数字」なのか

そうではありません。約2.73は、$X$ と $Y$ の**母集団での線形な関連**を表す傾きです。これを母集団線形射影係数と呼び、$\beta_{\mathrm{LP}}$ と書きます。

$$
\beta_{\mathrm{LP}}
=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}
=2+\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}
\approx2.7317
$$

**構造係数2を知りたいなら、このOLSは一致推定量ではありません。** 一方、線形な関連を記述・予測する目的なら、約2.73にも意味があります。

:::details 発展：なぜ母集団線形射影係数は「共分散 ÷ 分散」なのか

$Y$ を $a+bX$ という直線で予測するとします。ここで $a$ は切片、$b$ は傾きです。母集団での予測誤差の二乗平均

$$
E[(Y-a-bX)^2]
$$

を最小にします（$X,Y$ の2次モーメントは有限とします）。

**① まず切片を決める。** 傾き $b$ を固定し、$W=Y-bX$ と置くと、

$
E[(W-a)^2]
=\operatorname{Var}(W)+(E[W]-a)^2
$

です。右辺の第2項が0になる $a=E[W]=E[Y]-bE[X]$ が、最適な切片です。

**② 次に傾きを決める。** この切片を代入すると、最小化すべき値は

$
\begin{aligned}
\operatorname{Var}(Y-bX)
&=\operatorname{Var}(Y)-2b\operatorname{Cov}(X,Y)\\
&\quad+b^2\operatorname{Var}(X)
\end{aligned}
$

です。これを $b$ で微分して0と置くと、

$
-2\operatorname{Cov}(X,Y)+2b\operatorname{Var}(X)=0
$

なので、$\operatorname{Var}(X)>0$ のもとでは最小にする傾きが

$
b=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}
$

と求まります。今回の $Y=1+2X+u$ に当てはめた値が、本文の約2.73です。

:::

![欠落変数ZがXとYに影響し、省略後の誤差項uとXが相関する仕組み](/images/endogeneity-sample-size-structure.webp)
*図1：上段は $X=0.8Z+v$ と $Y=1+2X+1.5Z+\varepsilon$ という仮定した生成過程。下段の点線両矢印は統計的な関連であり、因果の矢印ではありません。2と約2.73の違いは、構造係数と単回帰の線形射影係数の違いです。*

最後に、これは標本数を増やしたときの**一致性**の議論です。有限標本において推定量の期待値が構造係数に等しいかという**不偏性**とは区別してください。

## 6. Pythonで1,000回ずつ推定してみる

ここでは、計算した理論値を**1,000回の繰り返し実験**で確かめます。後の図2では、横軸を推定された傾き、縦軸を推定した**確率密度**とし、2と約2.7317の位置を破線で示します。以下のPythonコードは**数値表を集計するためのもの**で、図版生成には別の再現コードを使います。

$X$ の係数の真値を2に固定し、標本数を $n=50, 500, 5000$ と増やします。

各標本数・各ケースで1,000回ずつデータを生成し、毎回 $Z$ を落とした単回帰を行います。

:::details Pythonコード（1,000回の実験）を開く

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

:::

実行すると、今回の乱数では次のようになりました。

| ケース | 標本数 $n$ | $\hat\beta$ の平均 | $\hat\beta$ の標準偏差 |
| --- | ---: | ---: | ---: |
| 内生性なし | 50 | 1.9932 | 0.2484 |
| 内生性あり | 50 | 2.7335 | 0.1757 |
| 内生性なし | 500 | 1.9985 | 0.0760 |
| 内生性あり | 500 | 2.7323 | 0.0523 |
| 内生性なし | 5000 | 2.0018 | 0.0254 |
| 内生性あり | 5000 | 2.7321 | 0.0165 |

この標準偏差は、推定量の標本分布の標準偏差（推定量の標準誤差）を1,000回の反復で近似したものです。1回の回帰から計算する推定標準誤差とは区別してください。

内生性ありの行を比べると、標本数を50から5,000に増やしたとき、**推定値の標準偏差は0.1757から0.0165へ、約10分の1**になりました。一方、OLSが理論上向かうのは**約2.7317**で、構造係数**2との差は約0.7317**のままです。ばらつきは小さくなっても、集まる位置は構造係数からずれています。

表の平均（2.7335や2.7321など）は、各条件1,000回の実験から得た値です。**理論上の確率収束先2.7317と、有限回の実験で求めた平均は別物**であり、完全に一致するとは限りません。内生性なしの行では、平均は2の近くにあり、標準偏差が小さくなっています。


### 分布を図で比較する

![標本数50・500・5000で内生性あり・なしのOLS推定量の分布を比較する図](/images/endogeneity-sample-size-distributions.webp)
*図2：各条件で1,000回推定した傾きから、カーネル密度推定で分布を滑らかに描いたもの。青は内生性なし、橙は内生性あり。縦の破線はそれぞれの理論的な確率収束先です。横軸の範囲は3段とも共通ですが、密度の縦軸尺度は段ごとに異なり、高さを直接比較する図ではありません。*

**上から下へ追うと、どちらの分布も狭くなります。** しかし、青は2に、橙は約2.73に集中します。なお、2つのケースでは $X$ 自体の分散も異なります。そのため、同じ標本数で青と橙の**分布の幅**を比べて内生性の効果とみなすのではなく、各色が標本数の増加とともに**どこへ集まるか**を比較してください。

### 分布図の再現

上の集計用Pythonコードと同じ乱数シード・生成順序を使用した図版生成コードをGitHubに置いています。

- [図版生成用Pythonコード（2枚の図を生成）](https://github.com/Osino-Niso/econ-data-lab/blob/main/code/endogeneity-sample-size/figures.py)

必要ライブラリ（NumPy / Matplotlib / Pillow）と日本語フォントを用意し、リポジトリ直下で次を実行してください。

```bash
python code/endogeneity-sample-size/figures.py
```

出力ファイルは `images/endogeneity-sample-size-distributions.webp` と `images/endogeneity-sample-size-structure.webp` です。

## 7. Rでも同じことを確認する

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

両方のコードで確認するのは、表の小数第4位までの一致ではなく、理論的な収束先（内生性なし：2、内生性あり：約2.7317）と整合するかです。

:::

## 8. では、データを増やす意味はないのか

意味はあります。一致性が成り立つ推定方法なら、標本数を増やすことで通常は推定値の偶然のばらつきが小さくなります。ただし、**標準誤差が小さいことは、構造係数を正しく推定できている証拠にはなりません。**

今回の欠落変数の例では、$Z$ を説明変数に適切に加えることが対処の一つです。一方、逆因果や同時決定などでは変数の追加だけで解決しないこともあり、研究設計や操作変数法など別の工夫が必要です。

## 9. よくある誤解

### 誤解1：内生性があると、OLSの傾きには何の意味もない

構造係数の推定としては一致しなくても、線形射影係数としての意味は残ります（第5節）。「何を推定したいのか」で評価は変わります。

### 誤解2：Zを1つ追加すれば、いつでも内生性が解決する

今回の設定では、$Z$ を適切に説明変数へ含めれば、$\varepsilon$ は $X$ と $Z$ から独立なので、構造係数2を推定できる条件が整います。しかし実際の研究では、観測できない交絡要因や逆因果などが残ることもあり、**変数を増やせば必ず解決するわけではありません。**

## 10. 3問で理解を確認

### Q1：推定値が安定すれば、それでよい？

**問題の設定**

ある母集団では $Y=1+2X+u$ という構造式が成り立ち、知りたい $X$ の構造係数は **2** です。$X$ と誤差項 $u$ の共分散はゼロではありません。各観測はこの母集団から独立に抽出され、必要な2次モーメントが有限で、$\operatorname{Var}(X)>0$ とします。分析者は $Y$ を $X$ に切片つきOLSで単回帰しました。

繰り返し標本を取り直す実験で、標本数を50から5,000へ増やすと、推定された傾きの分布は狭くなり、約2.73の近くに集中するようになりました。

**問い：** (1) このとき、推定値の「ばらつき」は改善していますか。(2) この結果から、構造係数2を一致推定できたと判断してよいですか。理由も説明してください。

:::details 解答・理由を開く

**(1) はい。** 分布が狭くなっているので、標本を取り直したときの推定値の偶然のばらつきは減っています。これは精密さの改善です。

**(2) いいえ。** 一致性は、標本数を増やしたときに**知りたい構造係数2へ確率収束するか**という性質です。この設定では $X$ と $u$ の共分散がゼロではなく、$\operatorname{Var}(X)>0$ とすると、大標本のOLSは $2+\operatorname{Cov}(X,u)/\operatorname{Var}(X)$ へ向かいます。これは2とは異なります。

問題文にある約2.73への集中も、構造係数2への収束を示してはいません。ただし、有限回の実験結果だけで確率収束を**証明**できるわけではなく、結論を理論的に支えるのは共分散についての仮定です。

:::

### Q2：$X$ と $Z$ が逆向きに動くと、OLSはどこへ向かう？

**問題の設定**

結果 $Y$ は次のデータ生成過程に従うとします。

$$
Y=1+2X+1.5Z+\varepsilon
$$

知りたいのは $X$ の**構造係数2**です。しかし分析者は $Z$ を説明変数に入れず、$Y$ を $X$ だけに切片つきOLSで単回帰します。

今回は説明変数 $X$ が、次の式で生成されるとします。

$$
X=-0.8Z+v
$$

各観測で $Z$、$v$、$\varepsilon$ を互いに独立な平均0・分散1の正規分布から生成し、観測間でも独立とします。$v$ と $\varepsilon$ はそれぞれの式に加わるランダムな要因です。

**問い：** $Z$ を省いたまま標本数を十分に増やすと、OLSで推定した $X$ の傾きは2へ近づくでしょうか。別の値なら、その数値を計算してください。

**計算の手がかり：** $Z$ を省いた誤差項を $u=1.5Z+\varepsilon$ と置くと、

$$
\text{確率収束先}
=2+\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}
$$

です。$\operatorname{Cov}$ は共分散、$\operatorname{Var}$ は分散です。分子と分母をそれぞれ求めてください。

:::details 解答・計算過程を開く

**① 共分散を求める**

$X=-0.8Z+v$、$u=1.5Z+\varepsilon$ なので、

$$
\begin{aligned}
\operatorname{Cov}(X,u)
&=\operatorname{Cov}(-0.8Z+v,\ 1.5Z+\varepsilon)\\
&=(-0.8)(1.5)\operatorname{Var}(Z)\\
&=-1.2
\end{aligned}
$$

となります。$Z$、$v$、$\varepsilon$ が互いに独立なので、それぞれ異なる乱数同士の共分散はゼロです。したがって、展開後には $Z$ と $Z$ の項だけが残ります。

**② 分散を求める**

$Z$ と $v$ は独立なので、

$$
\operatorname{Var}(X)=(-0.8)^2\operatorname{Var}(Z)+\operatorname{Var}(v)
=0.64+1=1.64
$$

です。

**③ 収束先を求めて解釈する**

$$
2+\frac{-1.2}{1.64}
\approx 1.2683
$$

**答え：約1.2683。** 構造係数2より約0.7317小さい値へ収束します。$Z$ を省いたままでは、標本数を増やしても構造係数2とのズレは消えません。

:::

### Q3：構造係数と単回帰係数は、何を表す？

**問題の設定**

$Y$ が次の生成過程に従うとします。

$$
Y=1+2X+1.5Z+\varepsilon,\qquad X=0.8Z+v
$$

各観測で $Z$、$v$、$\varepsilon$ を互いに独立な平均0・分散1の正規分布から生成し、観測間でも独立とします。元の式の $X$ の構造係数は **2** です。一方、$Z$ を省いて $Y$ を $X$ だけに切片つきOLSで回帰すると、その傾きは大標本で**約2.73**へ近づきます。

**問い：** (1) $Z$ と $\varepsilon$ を一定に保って $X$ を1増やしたとき、この構造式では $Y$ はいくつ増えますか。(2) 約2.73は何を表す係数ですか。これをそのまま「ほかの条件を一定に保ったときの $X$ の効果」と呼んでよいですか。

:::details 解答・理由を開く

**(1) 2増えます。** 式 $Y=1+2X+1.5Z+\varepsilon$ で $Z$ と $\varepsilon$ を固定すると、$X$ だけが1増えるときの $Y$ の増分は $2\times1=2$ です。これは与えられた生成過程の**構造係数2**が表す変化です。

**(2) 約2.73は、母集団における線形な関連を表す傾きです。** 具体的には母集団線形射影係数

$$
\beta_{\mathrm{LP}}
=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}
=2+\frac{1.2}{1.64}
\approx2.7317
$$

に一致します。$Z$ と $X$ が関連するため、省いた $Z$ の寄与が単回帰の傾きに混ざっています。

よって、約2.73を $Z$ などの条件を一定にした $X$ の効果として**読み替えることはできません**。ただし、約2.73にも線形な関連を表す係数としての意味はあります。また、構造係数2を現実の因果効果と呼べるかは、ここで仮定した生成過程を因果的に解釈できることが前提です。

:::

## まとめ

**データを増やすと、推定値のばらつきは通常小さくなります。しかし、どこに集中するかは別問題です。**

今回の例で $X$ と誤差項 $u$ の共分散がゼロでなければ、$Z$ を省いたOLSの収束先は

$$
\underbrace{\beta_X}_{\text{構造係数}}
+\underbrace{\frac{\operatorname{Cov}(X,u)}{\operatorname{Var}(X)}}_{\text{構造係数からのズレ}}
=\beta_{\mathrm{LP}}
$$

となります。標本数を増やすだけでは、このズレは解消しません。

**精密な推定と、知りたい係数を一致推定することは違う。** それを見分けるには、標本数だけでなく、推定対象とモデルの仮定を確認する必要があります。

## 再現コード

この記事のPython / Rコードと図版生成コードはGitHubにも置いています。

- [Pythonコード](https://github.com/Osino-Niso/econ-data-lab/blob/main/code/endogeneity-sample-size/python.py)
- [Rコード](https://github.com/Osino-Niso/econ-data-lab/blob/main/code/endogeneity-sample-size/r.R)
- [図版生成コード](https://github.com/Osino-Niso/econ-data-lab/blob/main/code/endogeneity-sample-size/figures.py)

## 参考資料

- 京都大学 環境マーケティング論分野「2SLS」  
  https://www.eeso.ges.kyoto-u.ac.jp/emm/materials/econometrics/2sls
- Jeffrey Greenbaum, *Economics 240B: Econometrics: Recitation Notes*（University of California, Berkeley）  
  https://www.ocf.berkeley.edu/~jeffreyg/240B.pdf
- MIT OpenCourseWare, *Lecture 21: Endogeneity and Instrument Variables*  
  https://ocw.mit.edu/courses/14-310x-data-analysis-for-social-scientists-spring-2023/resources/mit14_310x_s23_week10_lec21_pdf/
