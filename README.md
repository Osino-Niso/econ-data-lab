# econ-data-lab

Zenn: **経済データ実験室**

統計・計量経済学で初学者がつまずきやすい論点を、数式だけで終わらせず、Python・R・実データを使って確認するためのリポジトリです。

授業や学習中に生じた「なぜ？」を出発点に、概念の整理、コードによる確認、再現可能な形での公開までを行います。

## 公開記事

### ベルヌーイ分布は「1回」なのに、なぜ確率分布なのか？

- Zenn: https://zenn.dev/econ_data_lab/articles/bernoulli-one-trial
- 原稿: [articles/bernoulli-one-trial.md](articles/bernoulli-one-trial.md)
- Python: [code/bernoulli-one-trial/python.py](code/bernoulli-one-trial/python.py)
- R: [code/bernoulli-one-trial/r.R](code/bernoulli-one-trial/r.R)

「1回の試行」と「確率分布」がなぜ両立するのかを、確率変数・実現値・分布の違いから整理し、PythonとRで実際に確認しています。

## 方針

- 初学者が混同しやすい論点を、疑問から順にほどく
- 必要最小限の数式と、小さな具体例を使う
- 可能な限りPythonとRの両方で同じ概念を確認する
- 記事中のコードは実行して出力を確認する
- 公開前に文章・数式・コードの整合性を確認する
- 将来的には日本の公的統計など、実データを使った検証にも広げる

## 再現性と検証

記事で使用するPython / Rコードは `code/` に分離して保存しています。

GitHub Actionsの `Validate article code` でコードを実行し、基本的な再現性チェックを行っています。

- Python 3.12
- R
- 実行結果のartifact保存
- 0/1値や標本平均など、記事内容に対応した最小限の自動検証

## リポジトリ構成

- `articles/`: Zenn掲載用Markdown
- `code/`: 記事中のPython / R再現コード
- `.github/workflows/`: コード検証用GitHub Actions

## 公開フロー

1. 記事とコードを作成
2. Pull Request上で内容を確認
3. GitHub ActionsでPython / Rコードを検証
4. `published: true` に切り替えて `main` へマージ
5. Zennへ反映

記事は、理解した内容を自分で検証しながら蓄積していくことを目的としています。
