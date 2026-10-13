---
title: "2026年ノーベル経済学賞を数式で追う：利上げはなぜインフレを抑えるのか"
emoji: "🏭"
type: "tech"
topics: ["economics", "macroeconomics", "python", "r"]
published: true
---

2026年の「ノーベル経済学賞」（正式には *Sveriges Riksbank Prize in Economic Sciences in Memory of Alfred Nobel*）は、Robert E. HallとMichael Woodfordに授与されました。

正式な受賞理由は、

> **“for microeconomic foundations of macroeconomic stabilisation”**

です。

前回の記事では、この受賞内容を理解するために、家計の異時点間最適化からEuler方程式、Hallの消費理論、期待実質金利、自然利子率、ニュー・ケインジアンIS曲線までを追いました。

https://zenn.dev/econ_data_lab/articles/nobel-2026-hall-woodford

そこで分かったのは、中央銀行の金利が需要へ効く経路です。

$$
\text{名目金利}
\rightarrow
\text{期待実質金利}
\rightarrow
\text{GDPギャップ}
$$

ただ、前回の記事にはまだ大きな穴がありました。

> **GDPギャップが動いたあと、なぜインフレ率が動くのか？**

さらに金融政策まで戻って考えるなら、疑問はこうなります。

> **中央銀行が利上げすると、なぜ企業の価格設定を通じてインフレを抑える方向に働くのか？**

今回は、私がこの疑問を理解するためにたどった

```mermaid
flowchart LR
    A[企業の価格設定] --> B[マークアップと限界費用]
    B --> C[価格の硬直性]
    C --> D[将来を見た価格設定]
    D --> E[ニュー・ケインジアン<br/>フィリップス曲線]
    E --> F[Taylor rule]
    F --> G[Taylor principle]
```

という流れを整理します。

後半では、IS曲線とニュー・ケインジアン・フィリップス曲線を横に並べた小さな教材も使います。金利や期待インフレ率を動かすと、左のGDPギャップの変化が右のインフレ率へそのまま伝わるようにしました。

前回と同じく、この順序そのものがノーベル委員会の受賞理由をそのまま並べたものではありません。Royal Swedish Academy of Sciencesの2026年解説は、Woodfordのニュー・ケインジアン・モデルを、家計・企業のミクロ的意思決定に基づく3つの式からなる政策分析の枠組みとして説明しています。この記事は、そのうち前回ほとんど触れなかった**企業の価格設定と金融政策ルール**を、私自身の理解順に追うものです。

## 先に結論

基本的なニュー・ケインジアン・モデルでは、需要・供給・金融政策を代表的に次の3本の式でまとめられます。

### 需要側：ニュー・ケインジアンIS曲線

$$
 x_t
 =
 E_t x_{t+1}
 -
 \frac{1}{\sigma}
 \left[
 (i_t-E_t\pi_{t+1})-r_t^n
 \right].
$$

### 供給側：ニュー・ケインジアン・フィリップス曲線

$$
\pi_t
=
\beta E_t\pi_{t+1}
+\kappa x_t.
$$

### 金融政策：単純化したTaylor rule

$$
 i_t
 =
 r_t^n+\pi^*
 +\phi_\pi(\pi_t-\pi^*)
 +\phi_x x_t.
$$

ここで新しく重要になるのは、2本目と3本目です。

GDPギャップ $x_t$ が正なら、企業の限界費用を押し上げ、価格を引き上げる圧力になります。逆に $x_t$ が負なら、インフレ率を下げる方向に働きます。

ただし、

$$
x_t<0
$$

だからといって、

$$
\pi_t<0
$$

になるとは限りません。

現在のインフレ率には

$$
\beta E_t\pi_{t+1}
$$

も入るからです。

そして中央銀行がインフレを抑えるときに重要なのは、単に名目金利 $i_t$ を上げたかではありません。

$$
i_t-E_t\pi_{t+1}
$$

という**期待実質金利**がどう動き、自然利子率との差がどう変わったかを見る必要があります。

この3点が、今回私が特に引っかかったところでした。

## 1. まず、企業が毎期自由に価格を決められる世界を考える

いきなり価格の硬直性を入れる前に、価格を自由に変更できる企業の最適価格を考えます。

企業 $i$ が、他社とは少し違う商品を売っているとします。

価格を $P_i$、その企業の商品への需要を $Y_i$ とすると、簡単な差別化財モデルでは需要を

$$
Y_i
=
\left(\frac{P_i}{P}\right)^{-\varepsilon}Y,
\qquad \varepsilon>1
$$

のように書けます。

$P$ は経済全体の物価水準、$Y$ は総需要、$\varepsilon$ は価格を上げたとき需要がどれくらい減るかに関係するパラメータです。

企業の利潤を、限界費用 $MC$ が一定だと単純化して

$$
\Pi_i
=
(P_i-MC)Y_i
$$

とします。

企業は「値段を高くすれば1個あたりの利益は増えるが、売れる量は減る」という関係の中で $P_i$ を選びます。

この利潤を $P_i$ で最大化すると、最適価格は

$$
\boxed{
P_i^*
=
\frac{\varepsilon}{\varepsilon-1}MC
}
$$

となります。

前の学習では、たとえば

$$
MC=100,\qquad \varepsilon=5
$$

なら、

$$
P_i^*
=
\frac{5}{4}\times100
=125
$$

と計算しました。

ここで

$$
\mu
=
\frac{\varepsilon}{\varepsilon-1}
$$

と置けば、

$$
P_i^*=\mu MC
$$

です。

つまり、柔軟価格の世界では、企業の最適価格をまず

> **限界費用 × マークアップ**

として考えられます。

これは「企業が好き勝手に価格を決める」という意味ではありません。価格を上げすぎると需要を失うので、需要の価格弾力性がマークアップを制約しています。

## 2. でも、これだけでは「インフレの遅さ」を説明できない

ここで私は一度、「限界費用が上がれば価格も上がるなら、もうインフレの説明になっているのでは」と思いました。

ただ、この式だけなら、限界費用が変わった瞬間に企業は最適価格へ変更できます。

$$
MC\uparrow
\quad\Rightarrow\quad
P_i^*\uparrow
$$

です。

現実には、すべての価格があらゆる情報に対して同時に瞬時に変更されるわけではありません。

Royal Swedish Academy of Sciencesの2026年解説も、Woodfordのモデルでは企業が需要や生産費の変化のたびに価格を変えるのは高くつくため、価格が粘着的になると説明しています。

ニュー・ケインジアン・モデルでは、この**価格の硬直性**を入れることで、需要の変化が価格だけでなく生産量にも影響する余地が生まれます。

## 3. Calvo pricing：今価格を変えられる企業と、変えられない企業を分ける

価格硬直性を扱う代表的な方法が **Calvo pricing** です。

Calvo (1983) の価格設定では、各期に企業が価格を最適化し直せる確率を

$$
1-\theta
$$

とし、残りの

$$
\theta
$$

の企業はその期には価格を最適化し直せない、と考えます。

これは「現実の企業が本当に毎期くじを引いている」という主張ではありません。

さまざまな価格変更の摩擦を、分析しやすい形で表現するモデル化です。

重要なのは、価格を変更できる企業にとっても、今日だけを見て価格を決めればよいわけではないことです。

今日設定した価格を、次の期にも、その次の期にも使わなければならない可能性があります。

すると企業は、

- 将来の限界費用は上がりそうか
- 他社の価格は上がりそうか
- 自分の価格を次にいつ変更できるか分からない

といった将来まで考えて、今日の価格を決めます。

ここで、企業側にも**期待**が入ってきます。

前回の記事では家計が将来を見て消費を決めました。

今回は企業が将来を見て価格を決めます。

2026年のRoyal Swedish Academy of Sciencesの解説が、家計だけでなく企業の意思決定もforward lookingだと強調しているのは、この部分です。

## 4. 限界費用からインフレ率へ：まずはNKPCの「限界費用版」

Calvo型の価格設定を集計すると、単純化されたニュー・ケインジアン・フィリップス曲線は、まず実質限界費用を使って

$$
\pi_t
=
\beta E_t\pi_{t+1}
+\lambda\widehat{mc}_t
$$

のように書けます。

$\widehat{mc}_t$ は、実質限界費用の定常状態からの乖離です。

この式は、いきなり暗記するより2つに分けると分かりやすかったです。

### 将来のインフレ期待

$$
\beta E_t\pi_{t+1}
$$

企業は、今日決めた価格をしばらく使う可能性があります。

将来、他社の価格や自社の費用が高くなると考えているなら、価格を変更できる今日の時点で、より高い価格を設定する誘因があります。

そのため、**将来のインフレについての期待が現在のインフレ率にも入る**ことになります。

### 現在の限界費用

$$
\lambda\widehat{mc}_t
$$

生産を1単位増やす費用が高くなれば、企業が設定したい価格も高くなります。

San Francisco Fedも、基本NKPCを「期待将来インフレと実質限界費用が現在のインフレに関係する式」と説明しています。

## 5. なぜGDPギャップが限界費用につながるのか

次に、限界費用をGDPギャップへつなぎます。

ここは、私が最初に

> GDPギャップが増えたら、なぜ企業の限界費用が上がるのか

と引っかかったところです。

基本的なモデルでは、実際の産出が自然産出量を上回ると、企業は通常より多く生産しようとします。

そのため、

```text
GDPギャップが正
  ↓
生産を増やす
  ↓
労働需要などが強まる
  ↓
実質限界費用が上がる方向
  ↓
企業が設定したい価格が上がる
```

という経路を考えます。

もちろん、現実の限界費用は賃金、原材料価格、生産性、エネルギー価格などにも左右されます。

ここで言っているのは、基本的なニュー・ケインジアン・モデルで、実質限界費用の変動をGDPギャップと結び付ける部分です。

単純化して

$$
\widehat{mc}_t
\propto
x_t
$$

と書けば、先ほどの式は

$$
\boxed{
\pi_t
=
\beta E_t\pi_{t+1}
+\kappa x_t
}
$$

となります。

これが、今回使う**ニュー・ケインジアン・フィリップス曲線（NKPC）**です。

## 6. 私が間違えた点：$x_t<0$ でも、インフレ率が負とは限らない

私は最初、

$$
x_t<0
$$

なら

$$
\pi_t<0
$$

だと読みかけました。

しかし、NKPCは

$$
\pi_t
=
\beta E_t\pi_{t+1}
+\kappa x_t
$$

です。

$x_t$ が負であることが直接意味するのは、

$$
\kappa x_t<0
$$

ということだけです。

つまり、GDPギャップは**現在のインフレ率への下押し圧力**になります。

期待インフレ率の項が正なら、現在のインフレ率そのものは正のままでもかまいません。

たとえば、

$$
\beta=0.99,
\qquad
E_t\pi_{t+1}=2\%,
\qquad
\kappa=0.1,
\qquad
x_t=-1\%
$$

とします。

率を小数で代入すると、

$$
\pi_t
=0.99\times0.02
+0.1\times(-0.01)
$$

なので、

$$
\pi_t
=0.0188
=1.88\%
$$

です。

GDPギャップは負ですが、インフレ率は正です。

比較したいのは、GDPギャップが0だった場合の

$$
1.98\%
$$

よりも、現在のインフレ率が低くなっていることです。

Royal Swedish Academy of Sciencesの2026年解説も、負のGDPギャップについて「物価が押し下げられ、インフレが通常より低くなる」という形で説明しています。

> **負のGDPギャップ = デフレ**

ではなく、

> **負のGDPギャップ = インフレ率への下押し圧力**

と読む方が正確です。

## 7. 前回の需要側を1本だけ戻す

ここで、前回の記事の式を1本だけ戻します。

$$
 x_t
 =
 E_t x_{t+1}
 -
 \frac{1}{\sigma}
 \left[
 (i_t-E_t\pi_{t+1})-r_t^n
 \right].
$$

この式の導出は前回の記事で扱ったので、今回は繰り返しません。

見るのは括弧の中だけです。

$$
\underbrace{i_t-E_t\pi_{t+1}}_{\text{期待実質金利}}
-
\underbrace{r_t^n}_{\text{自然利子率}}
$$

期待実質金利が自然利子率より高ければ、GDPギャップを押し下げる方向に働きます。

そして今回分かったNKPCによって、

$$
x_t\downarrow
\quad\Rightarrow\quad
\pi_t\text{への下押し圧力}
$$

までつながります。

つまり、単純化すれば、

```mermaid
flowchart LR
    A[名目金利 i] --> B[期待実質金利<br/>i - Eπ]
    B --> C[自然利子率との比較]
    C --> D[GDPギャップ x]
    D --> E[限界費用]
    E --> F[企業の価格設定]
    F --> G[インフレ率 π]
```

です。

ここでようやく、前回の「金利はなぜGDPを動かすのか」から、今回の「なぜ利上げがインフレを抑える方向に働くのか」までつながりました。

## 8. ただし「名目金利を上げた」だけでは、引き締めとは限らない

ここも、私は一度符号を間違えました。

たとえば、名目金利が

$$
3\%\rightarrow4\%
$$

へ上がったとします。

これだけを見れば「利上げだから引き締め」と言いたくなります。

しかし、期待インフレ率が同時に

$$
2\%\rightarrow3.5\%
$$

へ上がったなら、期待実質金利は

$$
3\%-2\%=1\%
$$

から

$$
4\%-3.5\%=0.5\%
$$

へ**下がっています**。

自然利子率が1%のままなら、最初は中立的だった期待実質金利が、自然利子率を下回ります。

すると需要には、むしろ緩和方向の力がかかります。

したがって、金融政策の方向を見るときには、

> 名目金利を上げたか

だけではなく、

> **期待実質金利が自然利子率に対してどう動いたか**

を見る必要があります。

## 9. 中央銀行は金利をどう反応させるのか：Taylor rule

ここまでの2本の式だけでは、名目金利 $i_t$ が外から与えられたままです。

そこで、中央銀行がインフレ率やGDPギャップを見て金利を決める式を加えます。

単純化したTaylor ruleを

$$
\boxed{
 i_t
 =
 r_t^n+\pi^*
 +\phi_\pi(\pi_t-\pi^*)
 +\phi_x x_t
}
$$

とします。

ここで、

- $\pi^*$：インフレ目標
- $r_t^n+\pi^*$：GDPギャップが0でインフレ率が目標どおりのときの中立的な名目金利の基準
- $\phi_\pi$：インフレ率が目標からずれたとき、金利をどれだけ反応させるか
- $\phi_x$：GDPギャップへどれだけ反応するか

です。

John Taylorが1993年に示した代表的な式では、インフレが1%ポイント上がると、名目政策金利は合計で1.5%ポイント上がる形になっています。

ここで大事なのは、「中央銀行はこの式を機械的に守る」ということではありません。

Federal Reserveも、Taylor ruleを政策の原則を考える単純な基準として説明しつつ、現実の政策判断では金融環境や期待、海外経済など多くの情報が必要だとしています。

## 10. Taylor principle：なぜ「1対1より強く」が重要なのか

上の書き方では、Taylor principleは代表的に

$$
\boxed{\phi_\pi>1}
$$

と表せます。

直感を見るため、GDPギャップの項をいったん0とします。

インフレ率が目標から1%ポイント上がり、期待インフレ率もおおむね1%ポイント上がったと考えます。

### $\phi_\pi=0.5$ なら

名目金利は0.5%ポイントしか上がりません。

一方、期待インフレ率が1%ポイント上がるなら、

$$
i_t-E_t\pi_{t+1}
$$

は0.5%ポイント下がる方向です。

つまり、インフレが上がったのに期待実質金利が下がり、需要を刺激してしまう可能性があります。

### $\phi_\pi=1.5$ なら

名目金利は1.5%ポイント上がります。

期待インフレ率が1%ポイント上がっても、期待実質金利は0.5%ポイント上がる方向です。

すると、

$$
\text{期待実質金利}\uparrow
\rightarrow
x_t\downarrow
\rightarrow
\pi_t\text{への下押し圧力}
$$

という安定化方向のフィードバックが働きます。

MIT OpenCourseWareのニュー・ケインジアン・モデルの講義でも、$\phi_\pi>1$ のとき名目金利がインフレより1対1以上に反応し、実質金利が上がることをTaylor principleの中心として説明しています。

ただし、これは動学的なモデルの中で期待と政策反応が結び付く話です。

> **$\phi_\pi>1$ なら、どんな状況でも必ずインフレが下がる**

という機械的な法則ではありません。

## 11. 3本の式を並べると、モデルが閉じる

ここまで来ると、前回から追ってきた需要側、今回の供給側、中央銀行の行動を並べられます。

### 1. 需要

$$
 x_t
 =
 E_t x_{t+1}
 -
 \frac{1}{\sigma}
 \left[
 (i_t-E_t\pi_{t+1})-r_t^n
 \right]
$$

### 2. 供給

$$
\pi_t
=
\beta E_t\pi_{t+1}
+\kappa x_t
$$

### 3. 金融政策

$$
 i_t
 =
 r_t^n+\pi^*
 +\phi_\pi(\pi_t-\pi^*)
 +\phi_x x_t
$$

```mermaid
flowchart TD
    A[中央銀行の名目金利 i] --> B[期待実質金利 i - Eπ]
    B --> C[自然利子率との差]
    C --> D[GDPギャップ x]
    D --> E[限界費用への圧力]
    E --> F[企業の価格設定]
    F --> G[インフレ率 π]
    G --> A
    H[期待 Eπ, Ex] --> B
    H --> F
```

中央銀行が金利を決め、その金利が需要へ影響し、GDPギャップが企業の価格設定を通じてインフレ率へ影響し、インフレ率を見た中央銀行がまた金利を決めます。

Royal Swedish Academy of SciencesがWoodfordのモデルを「3つの式からなる政策の実験室」と説明している意味が、私にはここでようやく具体的になりました。

前回の記事では1本目だけをかなり長く追いました。

今回2本目と3本目まで入れたことで、

$$
\text{Hall}
\rightarrow
\text{家計の前向きな意思決定}
\rightarrow
\text{Woodford型の需要}
\rightarrow
\text{企業の前向きな価格設定}
\rightarrow
\text{金融政策による安定化}
$$

という流れが一応閉じます。

## 12. 2つの動くグラフで、金利からインフレまでつなぐ

ここまでの式は、1本ずつなら追えても、3本を頭の中だけで同時に動かすと急に分かりにくくなりました。

そこで、今回の基本モデルを**2つの連動するグラフ**として動かせる教材にしました。

左はニュー・ケインジアンIS曲線です。

$$
 x_t
 =
 E_t x_{t+1}
 -
 \frac{1}{\sigma}
 \left[
 (i_t-E_t\pi_{t+1})-r_t^n
 \right]
$$

名目金利や期待インフレ率を動かすと、期待実質金利が変わり、左のグラフ上でGDPギャップ $x_t$ が動きます。

右はNKPCです。

$$
\pi_t
=
\beta E_t\pi_{t+1}
+\kappa x_t
$$

左で決まった**同じGDPギャップ**をそのまま右へ渡し、現在のインフレ率がどこに来るかを表示します。

つまり画面上で、

$$
\text{名目金利}
\rightarrow
\text{期待実質金利}
\rightarrow
\text{GDPギャップ}
\rightarrow
\text{インフレ率}
$$

を一度に追えます。

灰色の破線・点は基準ケースで、色の付いた線・点が現在の設定です。スライダーを動かすと、グラフだけでなく中央の因果チェーンと説明文も同時に変わります。

まずは、次の3つを試すと今回の要点が見えやすいです。

### 1. 期待インフレ率を固定したまま利上げする

たとえば期待インフレ率を2%、自然利子率を1%にしたまま、名目金利を3%から4%へ上げます。

期待実質金利は1%から2%へ上がり、自然利子率を上回ります。その結果、左でGDPギャップが負方向へ動き、右ではインフレ率に下押し圧力がかかります。

### 2. 名目金利を上げても、期待インフレ率をそれ以上に上げる

次に名目金利を4%にしたまま、期待インフレ率を3.5%まで上げます。

期待実質金利は

$$
4\%-3.5\%=0.5\%
$$

となり、自然利子率1%を下回ります。

**名目金利は高いのに、需要には緩和方向の力がかかる**ケースを、左のグラフで確認できます。

これは「利上げしたか」だけでは金融環境を判定できない、という第8節の話そのものです。

### 3. GDPギャップを負にしても、インフレ率が正のままかを見る

期待インフレ率を正に保ったまま、GDPギャップが負になる設定を作ります。

右のNKPCでは点が左へ動き、インフレ率は下がりますが、必ずしも0%を下回りません。

ここで、

> **$x_t<0$ はデフレそのものではなく、インフレ率への下押し圧力**

という第6節の読み方を図でも確認できます。

### Taylor principleもグラフで見る

教材の下半分では、$\phi_\pi$ を動かせます。

$\phi_\pi<1$ と $\phi_\pi>1$ を切り替えると、インフレギャップが拡大したときの実質金利ギャップの傾きがどう変わるかを確認できます。

特に、

$$
\phi_\pi=0.5
$$

と

$$
\phi_\pi=1.5
$$

を比べると、Taylor principleの意味が見えやすいと思います。

以下から通常のWebページとして開けます。GitHub Pages上の静的なHTML / JavaScriptなので、読者側で追加の環境構築は必要ありません。

@[card](https://osino-niso.github.io/econ-data-lab/nobel-2026-pricing-inflation/)

この教材はパラメータの実証的な推定値を示すものではなく、**式の符号と金融政策の伝播経路を動かして確認するための教材**です。

同じ計算をコードでも確認できるよう、次にPython / R版を残しておきます。

## 13. Python / Rで3つのケースを比較する

ここでは、同じ単純化したIS曲線とNKPCを使って3ケースだけ比べます。

1. 期待実質金利 = 自然利子率で中立
2. 期待インフレ率が変わらないまま名目金利を1%ポイント上げる
3. 名目金利は上がるが、期待インフレ率がそれ以上に上がる

### Python

```python
from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    nominal_rate: float
    expected_inflation: float


natural_rate = 0.01
expected_next_gap = 0.0
sigma = 1.0
beta = 0.99
kappa = 0.10

scenarios = [
    Scenario("neutral", 0.03, 0.02),
    Scenario("nominal_hike", 0.04, 0.02),
    Scenario("hike_but_expectations_rise_more", 0.04, 0.035),
]

for s in scenarios:
    expected_real_rate = s.nominal_rate - s.expected_inflation
    interest_gap = expected_real_rate - natural_rate
    output_gap = expected_next_gap - interest_gap / sigma
    inflation = beta * s.expected_inflation + kappa * output_gap

    print(
        s.name,
        f"real={expected_real_rate * 100:.2f}%",
        f"interest_gap={interest_gap * 100:.2f}%pt",
        f"output_gap={output_gap * 100:.2f}%",
        f"inflation={inflation * 100:.2f}%",
    )
```

### R

```r
natural_rate <- 0.01
expected_next_gap <- 0.0
sigma <- 1.0
beta <- 0.99
kappa <- 0.10

scenarios <- data.frame(
  name = c(
    "neutral",
    "nominal_hike",
    "hike_but_expectations_rise_more"
  ),
  nominal_rate = c(0.03, 0.04, 0.04),
  expected_inflation = c(0.02, 0.02, 0.035)
)

scenarios$expected_real_rate <-
  scenarios$nominal_rate - scenarios$expected_inflation

scenarios$interest_gap <-
  scenarios$expected_real_rate - natural_rate

scenarios$output_gap <-
  expected_next_gap - scenarios$interest_gap / sigma

scenarios$inflation <-
  beta * scenarios$expected_inflation +
  kappa * scenarios$output_gap

print(transform(
  scenarios,
  expected_real_rate = expected_real_rate * 100,
  interest_gap = interest_gap * 100,
  output_gap = output_gap * 100,
  inflation = inflation * 100
))
```

見るべきなのは数値そのものではなく、

```text
期待実質金利 − 自然利子率
        ↓
GDPギャップ
        ↓
インフレ率への圧力
```

という符号です。

## 14. この3本の式は、現実のインフレを全部説明するわけではない

ここまで扱ったNKPCは、基本モデルを理解するためのかなり単純化された形です。

$$
\pi_t
=
\beta E_t\pi_{t+1}
+\kappa x_t
$$

だけを見れば、インフレ率は期待インフレ率とGDPギャップだけで決まるように見えます。

しかし現実には、原油価格、輸入価格、為替、生産性、賃金設定、インフレの慣性なども重要です。

そのため、実際の分析では供給ショックの項を加えたり、過去のインフレ率を含むハイブリッド型NKPCを考えたりします。

San Francisco Fedも、基本NKPCは理論上重要なベンチマークである一方、現実のインフレの持続性を説明するうえで課題があると指摘しています。

この記事で確認したいのは、現実のインフレをこの3本だけで予測することではありません。

> **家計の需要、企業の価格設定、中央銀行の金利決定を、ミクロ的な行動から一つのモデルにまとめられる**

というWoodford型の枠組みの骨格です。

## まとめ

第6記事と今回の記事を合わせると、私の中では次の流れになりました。

1. 家計は将来を見ながら今期と将来の消費を選ぶ。
2. 期待実質金利が自然利子率を上回ると、需要とGDPギャップを抑える方向に働く。
3. 企業は差別化された商品を売り、柔軟価格なら限界費用にマークアップを乗せた価格を設定する。
4. 価格が硬直的なら、企業は将来の限界費用や他社価格まで考えて今日の価格を決める。
5. その前向きな価格設定を集計すると、期待インフレ率とGDPギャップを含むNKPCにつながる。
6. 負のGDPギャップはインフレ率そのものを負にするのではなく、インフレ率への下押し圧力になる。
7. 金融政策では、名目金利ではなく期待実質金利と自然利子率の差を見る必要がある。
8. Taylor ruleを加えると、中央銀行の金利決定までモデル内に入る。
9. Taylor principleでは、インフレ上昇に対して名目金利を1対1より強く上げることが、期待実質金利を上げて需要を抑える方向のフィードバックにつながる。

2026年ノーベル経済学賞をきっかけに、第6記事では需要側、今回は供給側と中央銀行まで追いました。

細かい導出や、賃金硬直性、供給ショック、ゼロ金利制約、非伝統的金融政策などはまだ残っています。

それでも、

$$
\text{Hall}
\rightarrow
\text{Woodford}
\rightarrow
\text{ニュー・ケインジアン型のマクロ経済安定化政策}
$$

という大きな流れについては、少なくとも私自身が数式の符号を追える程度には具体的に見えるようになりました。

## 参考資料

- The Royal Swedish Academy of Sciences, “The Prize in Economic Sciences 2026”  
  https://www.kva.se/en/news/the-prize-in-economic-sciences-2026/
- The Royal Swedish Academy of Sciences, “Microfoundations deliver macro insights”  
  https://www.kva.se/en/prizes/prize-in-economic-sciences/microfoundations-deliver-macro-insights/
- Michael Woodford, *Interest and Prices: Foundations of a Theory of Monetary Policy*  
  https://blogs.cuit.columbia.edu/mw2230/interest-and-prices/
- Guillermo A. Calvo (1983), “Staggered prices in a utility-maximizing framework,” *Journal of Monetary Economics* 12(3), 383–398  
  https://www.sciencedirect.com/science/article/pii/0304393283900600
- MIT OpenCourseWare, *14.05 Intermediate Macroeconomics*, Lecture 19: Sticky Prices  
  https://ocw.mit.edu/courses/14-05-intermediate-macroeconomics-fall-2025/mit14_05_f25_lecture19.pdf
- MIT OpenCourseWare, *14.05 Intermediate Macroeconomics*, Lecture 20: The New Keynesian Model  
  https://ocw.mit.edu/courses/14-05-intermediate-macroeconomics-fall-2025/mit14_05_f25_lecture20.pdf
- Federal Reserve Bank of San Francisco, “Fixing the New Keynesian Phillips Curve”  
  https://www.frbsf.org/research-and-insights/publications/economic-letter/2007/11/new-keynesian-phillips-curve-nkpc/
- Board of Governors of the Federal Reserve System, “Principles for the Conduct of Monetary Policy”  
  https://www.federalreserve.gov/monetarypolicy/principles-for-the-conduct-of-monetary-policy.htm
- John B. Taylor (1993), “Discretion versus policy rules in practice”  
  https://web.stanford.edu/~johntayl/Papers/Discretion.PDF