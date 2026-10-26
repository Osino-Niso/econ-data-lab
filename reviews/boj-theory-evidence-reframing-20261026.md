# 2026-10-26 — 導入・研究上の位置づけの再設計

## 問題提起（ユーザーの校閲）

- 「2005Q3より2022Q1のCPI前年比が低い」という話が、導入でいきなり専門的かつ突飛。
- 図表の順位逆転自体を「意外な発見」とするより、植田総裁の説明が現代の主流的な経済学と整合するか、妥当性をどう検証するかを問う方が読者価値が高い。

## 編集判断と比較

| 方針 | 読者価値 | 正確性 | 負担・コスト | 判断 |
| --- | --- | --- | --- | --- |
| 四半期順位逆転をさらに補強 | 特殊な読図としては価値あり、しかし主題から逸れやすい | 時点を揃えてもショックが同質でない | 指標定義・図表の読みが先に必要 | 不採用 |
| 日銀の歴史解釈を無批判に整理 | 読みやすいが、原文以上の価値が乏しい | 根拠の強さを誤認しやすい | 低 | 不採用 |
| 4局面→波及の仕組み→既存実証と限界→検証方法 | 現代の研究へ接続でき、具体的な問いになる | 理論適合・実証示唆・個別因果識別を区別できる | 文献精査は必要 | 採用 |

## 本文の主な変更

- 導入の「2005Q3対2022Q1」段落を削除。一般読者が理解できる歴史的な問いと、研究上の妥当性への問いを提示。
- 旧3章の四半期比較を削除。旧4章のMermaid図を3章へ移し、一次的転嫁と二次的波及の区別を先に説明。
- 新4章に3本の研究と2026年4月日銀展望レポートBOX2を追加。研究の対象・仮定・限界を明示。
- Q3を、歴史的事実・因果関係・必要データを区別する応用課題へ変更。Q1水準、Q2転嫁・二次波及、Q3実証検証の役割分担。
- まとめを「初期のCPI値の逆転」から「説明がどこまで支えられ、何が未検証か」へ変更。
- 元の図表2～5と架空A/B/C、Python/Rの数値計算は維持。新たな独自実測値や因果推定は追加していない。

## 使用資料と確認範囲

- 植田和男（2026）日銀開会挨拶の本文・図表：https://www.boj.or.jp/about/press/koen_2026/data/ko260527a1.pdf
- Baba and Lee（2022）IMF WP 2022/173：欧州の原油ショックの波及とインフレ率・賃金設定制度・政策信認の関係。https://www.imf.org/en/publications/wp/issues/2022/09/06/second-round-effects-of-oil-price-shocks-implications-for-europes-inflation-outlook-523201
- 安達・加藤（2025）：日本/欧州DSGE分析で原材料価格一次転嫁が主因、賃金経由の二次的波及は持続性に寄与した可能性。https://www.boj.or.jp/research/wps_rev/wps_2025/wp25j05.htm
- Alvarez et al.（2022）IMF WP 2022/221：賃金・物価がともに加速しても、持続的なスパイラルが必然ではない。https://www.imf.org/en/publications/wp/issues/2022/11/11/wage-price-spirals-what-is-the-historical-evidence-525073
- 日本銀行『展望レポート』（2026年4月）BOX2：エネルギー原単位や産業構造の違いを組み込む一次的波及の試算。https://www.boj.or.jp/mopo/outlook/gor2604b.pdf

## 重要な非結論

- 「主流的な理論と整合する」は、すべてのマクロ経済学者が同じ寄与分解に合意しているという意味ではない。
- IMFの欧州推計は1970年代の日本を直接推定していない。日銀の追加資料は独立機関による再現ではない。
- 4時期の同時変化から金融政策、為替、労使交渉、省エネなどの効果を分離できない。政策も内生的に決定される。
- 2022Q1は2021年頃からのコスト上昇開始前ではなく、異なる原油ショックを等価な処置とみなさない。

## 公開ゲート

- `published: false` 維持。一般公開操作なし。
- 原文・研究の要約内容とZenn Markdownの静的検査を実施。引用図表の著作権条件、Zenn実表示・スマホでの視認性は未確認として扱う。
- このPRのPython/R/Interactive lab CI結果を確認後、非公開のままmainへ反映する。
## GitHubへの反映・確認（2026-10-26）

- PR #38（https://github.com/Osino-Niso/econ-data-lab/pull/38）をDraftで作成し、PR上のPython・R・Interactive lab 3ジョブ成功後にreadyへ移行してsquash merge。merge commit：89282579ed0f85eca521a5f383df124b9a4b8a1d。
- main上で articles/oil-shocks-inflation-regimes.md の published: false、追加研究章、応用型Q3、元図4点の参照を確認。
- マージ後のGitHub Actions Validate article code run 40270411957（https://github.com/Osino-Niso/econ-data-lab/actions/runs/40270411957）：Python・R・Interactive lab の3ジョブすべてsuccess。
- 静的確認は画像実表示・著作権の適否を保証しない。Zenn下書きの実表示と引用条件は未確認。
