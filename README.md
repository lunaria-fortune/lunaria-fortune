# LUNARIA｜AI占いサロン

## 概要
生年月日・星座・数秘術の情報と、利用者が選んだテーマをもとに、OpenAI APIを通じて生成AIが個別の占い文章を作成するWebアプリです。

## GitHubへのアップロード
ZIPを展開し、`app.py`、`requirements.txt`、`README.md`をGitHubリポジトリの直下にアップロードしてください。ZIPファイルそのものではなく、展開した中のファイルをアップロードします。

## Streamlit Community Cloudで公開
1. https://share.streamlit.io/ にGitHubアカウントでログインします。
2. GitHubアカウントへの接続を許可します。
3. Create appからRepository、Branch（通常はmain）、Main file path（`app.py`）を選択します。
4. Advanced settingsのSecretsに以下を入力します。

```toml
OPENAI_API_KEY = "あなたのOpenAI APIキー"
APP_ACCESS_CODE = "先生に伝えるアクセスコード"
```

5. Deployを押します。公開URLとアクセスコードを先生に伝えます。

## APIキーについて
OpenAI APIキーは https://platform.openai.com/api-keys から作成します。ChatGPTの月額プランとは別にAPI利用料金が発生する場合があります。APIキーをGitHubのファイルやメール本文に書かないでください。Streamlit CloudのSecretsにのみ保存してください。

## AIの仕組み
1. 利用者が入力した生年月日から、プログラムが星座とライフパスナンバーを算出します。
2. 選択された占いテーマ、気分、任意の相談内容を合わせてAIに送信します。
3. OpenAI Responses APIが入力内容に応じた鑑定文を生成します。
4. 結果を画面に表示し、同じセッション内の履歴に保存します。

## 提出時の説明例
本アプリは、生成AIを利用した占いWebアプリケーションである。利用者の生年月日から星座と数秘術の数値を算出し、占いテーマや気分などの入力情報と合わせて生成AIに送信する。AIは入力情報に応じて、運勢・メッセージ・ラッキーカラー・ラッキーアイテム・開運アクションを個別に生成する。固定の文章を表示するだけでなく、生成AIによって鑑定内容が変化する点が特徴である。

## 使用技術
- Python
- Streamlit
- OpenAI Python SDK
- OpenAI Responses API

## 注意
占いは娯楽目的です。将来や相手の気持ちを保証するものではありません。公開アプリではアクセスコードを設定し、API利用状況を定期的に確認してください。
