---
title: "標本分布の期待値・分散・標準偏差は何のため？ 標準誤差までつなげて考える"
emoji: "📊"
type: "tech"
topics: ["statistics", "econometrics", "python", "r"]
published: true
---

計量経済学の授業で、標本平均は確率変数なので標本分布を考えられる、と習いました。

そのあとに出てきたのが、

$$
E[\bar{Y}],\qquad Var(\bar{Y}),\qquad SD(\bar{Y})
$$

です。

式は追えるのですが、私はここで一度止まりました。

**標本分布の期待値・分散・標準偏差まで求めて、結局何につながるのでしょうか。**

整理してみると、これらは別々の公式ではなく、

> 標本平均という推定量が、どこを中心に、どれくらいぶれるのか

を見るための量でした。

この記事では標本平均に話を絞り、標準誤差、さらに信頼区間・仮説検定までのつながりを確認します。

## 先に結論

母平均を $\mu$、母分散を $\sigma^2$ とし、$Y_1,\ldots,Y_n$ が独立同一分布に従うとします。

標本平均

$$
\bar{Y}=\frac{1}{n}\sum_{i=1}^{n}Y_i
$$

について、

$$
E[\bar{Y}]=\mu
$$

$$
Var(\bar{Y})=\frac{\sigma^2}{n}
$$

$$
SD(\bar{Y})=\frac{\sigma}{\sqrt{n}}
$$

が成り立ちます。

それぞれの役割は次のように整理できます。

| 量 | 見ているもの |
| --- | --- |
| $E[\bar{Y}]$ | 標本分布の中心 |
| $Var(\bar{Y})$ | 標本平均のばらつき |
| $SD(\bar{Y})$ | そのばらつきを元の単位で表したもの |

そして、**推定量の標本分布の標準偏差**を標準誤差と呼びます。

したがって、母標準偏差 $\sigma$ が既知なら、

$$
SE(\bar{Y})=\frac{\sigma}{\sqrt{n}}
$$

です。

実際には $\sigma$ が未知であることが多いので、標本標準偏差 $s$ を使って

$$
\widehat{SE}(\bar{Y})=\frac{s}{\sqrt{n}}
$$

と推定します。

この区別は後でもう一度戻ります。

## 1. なぜ標本平均に分布があるのか

実際に標本を1回取ったあとなら、標本平均は

$$
\bar{y}=101.3
$$

のような1つの値です。

しかし、標本を取る前には、どの観測値が入るかはまだ決まっていません。

標本抽出前の

$$
Y_1,\ldots,Y_n
$$

は確率変数なので、

$$
\bar{Y}=\frac{Y_1+\cdots+Y_n}{n}
$$

も確率変数です。

同じ母集団から同じ大きさの標本を何度も取り直せば、

```text
1回目の標本平均  101.3
2回目の標本平均   98.7
3回目の標本平均  102.1
4回目の標本平均   99.5
...
```

のように、標本平均も毎回変わります。

この「標本平均がどの値をどの確率で取るか」を表したものが、標本平均の標本分布です。

1回の標本から得た値だけでなく、

- 標本平均は平均的にどこに現れるのか
- 標本を取り直すとどれくらい動くのか

を考えるために、標本分布の期待値や分散を見ます。

## 2. $E[\bar{Y}]=\mu$ は何を意味するのか

$Y_1,\ldots,Y_n$ が同じ母平均 $\mu$ を持つとします。

期待値の線形性から、

$$
E[\bar{Y}]
=
E\left[
\frac{1}{n}\sum_{i=1}^{n}Y_i
\right]
$$

$$
=
\frac{1}{n}\sum_{i=1}^{n}E[Y_i]
=
\frac{1}{n}\cdot n\mu
=
\mu
$$

です。

つまり、標本平均を何度も取り直したとき、標本分布の中心は母平均 $\mu$ にあります。

このように、推定量の期待値が推定したい母数に一致する性質を**不偏性**と呼びます。

標本平均は母平均の不偏推定量です。

ただし、

$$
E[\bar{Y}]=\mu
$$

だからといって、1回ごとの標本平均が必ず母平均と一致するわけではありません。

母平均が100でも、ある標本では97、別の標本では103になることがあります。

### ここは大数の法則とは別の話

復習していて、私が実際に混同したのがここでした。

$$
E[\bar{Y}_n]=\mu
$$

と、大数の法則

$$
\bar{Y}_n\xrightarrow{p}\mu
$$

は同じ主張ではありません。

前者は、**ある標本サイズ $n$ を固定したとき、標本平均の標本分布の中心がどこにあるか**という話です。

独立同一分布の標本なら、$n=5$ でも $n=100$ でも、

$$
E[\bar{Y}_n]=\mu
$$

です。

一方、大数の法則は、**$n$ を大きくしていったとき、標本平均が母平均の近くへ確率的に集中していく**という話です。

同じ $\mu$ が出てきますが、

- 不偏性：固定した $n$ での分布の中心
- 大数の法則：$n\to\infty$ での確率収束

と役割が違います。

## 3. 期待値だけではなぜ足りないのか

2つの推定量A、Bを考えます。

どちらも期待値が100だとしても、

- Aは99〜101あたりに集まりやすい
- Bは80〜120まで大きく動く

なら、同じ「中心が100」でも、標本を取り直したときの安定性は違います。

つまり、

$$
E[\bar{Y}]=\mu
$$

だけでは、標本平均がどれくらいぶれるかは分かりません。

そこで分散を見ます。

## 4. $Var(\bar{Y})=\sigma^2/n$ を導く

$Y_1,\ldots,Y_n$ が独立で、それぞれ分散 $\sigma^2$ を持つとします。

標本平均の分散は、

$$
Var(\bar{Y})
=
Var\left(
\frac{1}{n}\sum_{i=1}^{n}Y_i
\right)
$$

です。

定数 $1/n$ を外に出すと、

$$
Var(\bar{Y})
=
\frac{1}{n^2}
Var\left(
\sum_{i=1}^{n}Y_i
\right)
$$

となります。

独立なら共分散項が0なので、

$$
Var\left(
\sum_{i=1}^{n}Y_i
\right)
=
\sum_{i=1}^{n}Var(Y_i)
=
n\sigma^2
$$

です。

したがって、

$$
Var(\bar{Y})
=
\frac{1}{n^2}\cdot n\sigma^2
=
\frac{\sigma^2}{n}
$$

となります。

ここでは、分散を足し合わせるところで独立性を使っています。

## 5. 標本サイズを増やすと何が変わるか

母標準偏差を

$$
\sigma=20
$$

とします。

$n=25$ なら、

$$
Var(\bar{Y})=\frac{20^2}{25}=16
$$

なので、

$$
SD(\bar{Y})=4
$$

です。

$n=100$ なら、

$$
Var(\bar{Y})=\frac{20^2}{100}=4
$$

なので、

$$
SD(\bar{Y})=2
$$

です。

整理すると、

| $n$ | $E[\bar{Y}]$ | $Var(\bar{Y})$ | $SD(\bar{Y})$ |
| ---: | ---: | ---: | ---: |
| 25 | $\mu$ | 16 | 4 |
| 100 | $\mu$ | 4 | 2 |

$n$ を25から100へ4倍にしても、標本分布の中心は変わりません。

変わるのは広がりです。

また、標準偏差は

$$
\frac{1}{\sqrt{n}}
$$

に比例するので、標本サイズを4倍にすると半分になります。

## 6. 標本分布の標準偏差が標準誤差

標準誤差は、推定量の標本分布の標準偏差です。

標本平均なら、

$$
SE(\bar{Y})
=
SD(\bar{Y})
=
\frac{\sigma}{\sqrt{n}}
$$

です。

標準偏差と標準誤差は、見ている対象が違います。

| 量 | ばらつきを見ている対象 |
| --- | --- |
| 母標準偏差 $\sigma$ | 個々の観測値 $Y$ |
| 標準誤差 $SE(\bar{Y})$ | 推定量である標本平均 $\bar{Y}$ |

標準誤差を「推定値がどの程度信頼できるか」とだけ言うと、少し広すぎます。

標準誤差が直接表しているのは、

> 同じ標本抽出を繰り返したとき、推定量がどれくらいばらつくか

です。

標準誤差が小さいほど、**標本抽出によるばらつきが小さいという意味では**推定が安定しています。

一方で、標準誤差が小さくても、標本の取り方に偏りがある、モデルの仮定が崩れている、といった別の問題は残りえます。

## 7. Pythonで標本平均を10,000回作る

母平均100、母標準偏差20の正規分布から標本を取ります。

標本サイズ25と100について、それぞれ10,000回標本を作り、毎回の標本平均を計算します。

```python
import numpy as np

mu = 100.0
sigma = 20.0
repetitions = 10_000

rng = np.random.default_rng(42)

for n in [25, 100]:
    samples = rng.normal(
        loc=mu,
        scale=sigma,
        size=(repetitions, n),
    )

    sample_means = samples.mean(axis=1)

    print(f"n = {n}")
    print(f"mean of sample means = {sample_means.mean():.4f}")
    print(f"variance of sample means = {sample_means.var(ddof=1):.4f}")
    print(f"sd of sample means = {sample_means.std(ddof=1):.4f}")
    print(f"theoretical SE = {sigma / np.sqrt(n):.4f}")
```

GitHub Actions上での実行結果は、次のようになります。

```text
n = 25
mean of sample means = 100.0027
variance of sample means = 16.0495
sd of sample means = 4.0062
theoretical SE = 4.0000

n = 100
mean of sample means = 100.0194
variance of sample means = 3.8738
sd of sample means = 1.9682
theoretical SE = 2.0000
```

10,000個の標本平均の平均は100付近です。

また、その標準偏差は、

- $n=25$ では4付近
- $n=100$ では2付近

となり、理論上の

$$
\frac{\sigma}{\sqrt{n}}
$$

に近づいています。

このシミュレーションでは母集団を正規分布にしているため、標本平均も正規分布に従います。

ここで見たいのは中心極限定理そのものというより、**$n$ を増やすと標本分布の幅が狭くなること**です。

## 8. Pythonで標本分布を可視化する

同じ10,000個の標本平均をヒストグラムにすると、$n=100$ のほうが母平均100の近くへ強く集中していることを確認できます。

```python
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

mu = 100.0
sigma = 20.0
repetitions = 10_000
sample_sizes = [25, 100]

rng = np.random.default_rng(42)
sample_means_by_n = {}

for n in sample_sizes:
    samples = rng.normal(
        loc=mu,
        scale=sigma,
        size=(repetitions, n),
    )
    sample_means_by_n[n] = samples.mean(axis=1)

fig, ax = plt.subplots(figsize=(6.4, 3.8))

bins = np.linspace(84, 116, 65)

for n in sample_sizes:
    ax.hist(
        sample_means_by_n[n],
        bins=bins,
        density=True,
        histtype="step",
        linewidth=1.3,
        label=f"n = {n}",
    )

ax.axvline(mu, linestyle="--", linewidth=1.0, label="population mean")
ax.set_xlabel("sample mean")
ax.set_ylabel("density")
ax.set_title("Sampling distributions of the sample mean")
ax.legend()

fig.tight_layout()

output_path = Path("images/sampling-distribution-moments.webp")
output_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output_path, dpi=100)
plt.close(fig)
```

![n=25とn=100の標本平均の標本分布](/images/sampling-distribution-moments.webp)
*同じ母集団から標本を10,000回ずつ生成した結果。中心はどちらも100付近だが、n=100のほうが分布が狭い。*

数値で標準偏差が4から2へ小さくなることを確認するだけでなく、図にすると「中心はほぼ動かず、広がりだけが小さくなる」という違いが見えやすくなります。

GitHub Actionsでもこの可視化コードを実行し、記事で使うWebP画像をartifactとして保存するようにしています。

## 9. Rでも同じ実験をする

Rでは `replicate()` を使って、標本抽出と標本平均の計算を繰り返します。

```r
mu <- 100
sigma <- 20
repetitions <- 10000

set.seed(42)

for (n in c(25, 100)) {
  sample_means <- replicate(
    repetitions,
    mean(rnorm(n, mean = mu, sd = sigma))
  )

  cat("n =", n, "\n")
  cat(sprintf("mean of sample means = %.4f\n", mean(sample_means)))
  cat(sprintf("variance of sample means = %.4f\n", var(sample_means)))
  cat(sprintf("sd of sample means = %.4f\n", sd(sample_means)))
  cat(sprintf("theoretical SE = %.4f\n\n", sigma / sqrt(n)))
}
```

PythonとRでは乱数生成の仕組みが異なるため、実行結果の数値は完全には一致しません。

ただし、どちらでも

- 標本平均の平均は100付近
- $n=25$ の標本平均の標準偏差は4付近
- $n=100$ では2付近

になることを確認できます。

Rでも同様のヒストグラムを描けますが、同じ内容の図を2枚並べると重複が大きいため、本文ではPythonで生成した図だけを掲載しています。

## 10. 信頼区間・仮説検定へどうつながるか

ここまでで、標本平均の標本分布について

- 中心
- ばらつき

が分かりました。

さらに分布の形まで分かれば、確率計算ができます。

独立同一分布で分散が有限であるなど、中心極限定理の条件が満たされると、$n$ が十分大きいとき、

$$
\bar{Y}
\approx
\mathcal{N}\left(
\mu,
\frac{\sigma^2}{n}
\right)
$$

と近似できます。

同じことを標準化して書けば、

$$
\frac{\bar{Y}-\mu}{\sigma/\sqrt{n}}
\approx
\mathcal{N}(0,1)
$$

です。

分母に入っている

$$
\frac{\sigma}{\sqrt{n}}
$$

が標準誤差です。

これによって、観測された標本平均が仮定した母平均から「標準誤差何個分離れているか」を考えられます。

この発想が仮説検定へつながります。

また、母標準偏差 $\sigma$ が既知で、正規分布を使える単純な場合には、95%信頼区間を

$$
\bar{Y}
\pm
1.96\frac{\sigma}{\sqrt{n}}
$$

の形で作れます。

標本分布の期待値・分散・標準誤差を求めることは、ここで初めて「確率計算の材料」として効いてきます。

## 11. 母標準偏差 $\sigma$ が未知ならどうするか

実際には、母標準偏差 $\sigma$ は分からないことが多いです。

その場合、1回の標本から計算した標本標準偏差 $s$ を使って、

$$
\widehat{SE}(\bar{Y})
=
\frac{s}{\sqrt{n}}
$$

と標準誤差を推定します。

ここで $s$ は、通常、$n-1$ で割る標本分散の平方根として計算する標本標準偏差です。

ここで区別したいのは、

$$
SE(\bar{Y})
=
\frac{\sigma}{\sqrt{n}}
$$

は理論上の標準誤差そのものであり、

$$
\widehat{SE}(\bar{Y})
=
\frac{s}{\sqrt{n}}
$$

は、その未知の標準誤差を標本から推定した値だということです。

正規母集団で $\sigma$ が未知の小標本なら、母平均の推測では標準正規分布ではなく $t$ 分布を使います。

この記事では深入りしませんが、「$\sigma$ が未知なら何もできない」のではなく、$s$ を使って標準誤差を推定し、その不確かさも含めた方法へ進む、と考えるとつながります。

## 12. 混同しやすい概念を並べる

最後に、今回の式と定理を並べます。

| 内容 | 何を言っているか |
| --- | --- |
| $E[\bar{Y}_n]=\mu$ | 固定した $n$ で、標本分布の中心が母平均にある |
| 不偏性 | 推定量の期待値が推定対象の母数に一致する |
| $Var(\bar{Y}_n)=\sigma^2/n$ | 標本平均のばらつきが $n$ とともに小さくなる |
| $SE(\bar{Y}_n)=\sigma/\sqrt{n}$ | 標本平均の標本分布の標準偏差 |
| 大数の法則 | $n\to\infty$ で $\bar{Y}_n$ が $\mu$ へ確率収束する |
| 中心極限定理 | 標準化した標本平均の分布が正規分布へ近づく |

特に、

$$
E[\bar{Y}_n]=\mu
$$

と

$$
\bar{Y}_n\xrightarrow{p}\mu
$$

は、同じ「母平均 $\mu$」が出てきても別の話です。

前者は分布の中心、後者は標本サイズを増やしたときの収束を表しています。

## まとめ

最初の疑問は、

> 標本分布の期待値・分散・標準偏差を求めて、結局何につながるのか？

というものでした。

標本平均については、

$$
E[\bar{Y}]=\mu
$$

が標本分布の中心を、

$$
Var(\bar{Y})=\frac{\sigma^2}{n}
$$

がばらつきを、

$$
SE(\bar{Y})=\frac{\sigma}{\sqrt{n}}
$$

がそのばらつきを元の単位で表します。

そして、中心極限定理などによって標本分布の形まで扱えるようになると、標準誤差を使った確率計算から、信頼区間や仮説検定へ進めます。

授業で期待値・分散・標準偏差が並んだとき、私は最初、それぞれを計算する目的が見えていませんでした。

今は、

> 中心を見るのが期待値、ぶれを見るのが分散・標準誤差。その情報を使って統計的推測へ進む

と整理しています。

## 関連記事

- [ベルヌーイ分布は「1回」なのに、なぜ確率分布なのか？](https://zenn.dev/econ_data_lab/articles/bernoulli-one-trial)
- [E[u|X]=0って結局どういう意味？ 条件付き平均ゼロから外生性を考える](https://zenn.dev/econ_data_lab/articles/zero-conditional-mean)

## 参考資料

- [東北大学 石垣司「統計学入門 ～標本平均～」](https://www2.econ.tohoku.ac.jp/~isgk/lec_material/basic_stat/basic_stat_09.pdf)
- [龍谷大学 蛭川雅之「経済統計学講義ノート No.6」](https://www.econ.ryukoku.ac.jp/~hirukawa/econstat/ln06.pdf)
