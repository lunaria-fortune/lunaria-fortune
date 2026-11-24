# LUNARIA｜AI占いサロン（API不要版）

Streamlitで動作する占いアプリです。OpenAI APIキーや外部APIへの接続は不要で、API利用料は発生しません。

## GitHubで更新する方法
1. ZIPを展開します。
2. GitHubの `lunaria-fortune` リポジトリを開きます。
3. `Add file` → `Upload files` を選びます。
4. 展開したフォルダ内の `app.py` と `requirements.txt` をアップロードします（READMEは任意）。
5. `Commit changes` を押します。
6. Streamlit Community Cloudが自動で再デプロイします。アプリ画面を再読み込みしてください。

## ローカル起動
```bash
pip install -r requirements.txt
streamlit run app.py
```

このアプリは星座・数秘術の簡易計算と、アプリ内に用意した占い文章を組み合わせて結果を表示します。生成AIがその場で文章を生成するものではありません。
