import os
from datetime import date
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LUNARIA｜AI占いサロン", page_icon="🌙", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap');
.stApp {background: radial-gradient(ellipse at top, #34264f 0%, #171329 42%, #10101d 100%); color:#f7f0ff;}
html, body, [class*="css"] {font-family:'Zen Kaku Gothic New',sans-serif;}
h1,h2,h3 {font-family:'Noto Serif JP',serif !important; color:#f4e8d2 !important;}
.hero {text-align:center;padding:2rem 1rem 1.4rem;border:1px solid #76618e;border-radius:22px;background:linear-gradient(135deg,rgba(89,65,119,.55),rgba(30,25,51,.75));margin-bottom:1.2rem;}
.hero .brand {font-family:'Noto Serif JP',serif;letter-spacing:.22em;font-size:2.5rem;color:#f4dfb4;}
.hero p {color:#d8cce8;letter-spacing:.08em;}
div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {border-color:#64527a !important;}
.stButton>button, .stFormSubmitButton>button {background:linear-gradient(90deg,#9a79b9,#c19b83);color:#171329;border:0;border-radius:12px;font-weight:700;min-height:3rem;width:100%;}
.stTextInput input,.stDateInput input,.stSelectbox div[data-baseweb="select"] {background:#211c35;color:#fff;border-color:#66547e;}
.result {background:rgba(45,35,66,.82);border:1px solid #8b739d;border-radius:18px;padding:1.3rem;margin:.8rem 0;}
.kicker {color:#d7b98c;letter-spacing:.18em;font-size:.78rem;}
.smallnote {color:#bdb1cc;font-size:.82rem;}
div[data-testid="stMarkdownContainer"] p {line-height:1.85;}
</style>
""", unsafe_allow_html=True)

# Public deployment protection: set APP_ACCESS_CODE in Streamlit Cloud Secrets.
try:
    app_access_code = st.secrets.get("APP_ACCESS_CODE", "")
except Exception:
    app_access_code = ""

if app_access_code:
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False
    if not st.session_state.access_granted:
        st.markdown('''<div class="hero"><div class="brand">LUNARIA</div><p>AI FORTUNE SALON</p><div>招待された方専用ページです。</div></div>''', unsafe_allow_html=True)
        with st.form("access_form"):
            entered_code = st.text_input("アクセスコード", type="password")
            unlock = st.form_submit_button("入室する")
        if unlock:
            if entered_code == app_access_code:
                st.session_state.access_granted = True
                st.rerun()
            else:
                st.error("アクセスコードが違います。")
        st.stop()
else:
    st.warning("管理者向け設定が未完了です。APP_ACCESS_CODEを設定すると、招待制で公開できます。")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("## 🌙 設定")
    st.caption("AI鑑定を利用するにはAPIキーが必要です。")
    api_key = st.text_input("OpenAI APIキー", type="password", help="入力したキーはこのアプリのセッション内でのみ使用します。コードには保存しません。")
    model = st.selectbox("使用モデル", ["gpt-5.5", "gpt-5.4", "gpt-4.1-mini"], index=0)
    st.markdown("---")
    st.markdown("**使い方**")
    st.caption("① 生年月日などを入力\n\n② 占いメニューを選択\n\n③「AIに占ってもらう」を押す")
    st.markdown("---")
    st.caption("このアプリの占いは娯楽を目的としたものです。")

def zodiac(d):
    signs = [
        ((1,20),"山羊座"),((2,19),"水瓶座"),((3,20),"魚座"),((4,20),"牡羊座"),
        ((5,21),"牡牛座"),((6,21),"双子座"),((7,22),"蟹座"),((8,23),"獅子座"),
        ((9,23),"乙女座"),((10,23),"天秤座"),((11,22),"蠍座"),((12,22),"射手座"),
        ((12,31),"山羊座")
    ]
    for (m,day), name in signs:
        if (d.month,d.day) <= (m,day):
            return name
    return "山羊座"

def life_path(d):
    n = sum(int(x) for x in d.strftime("%Y%m%d"))
    while n not in (11,22,33) and n > 9:
        n = sum(int(x) for x in str(n))
    return n

def ask_ai(prompt, key, model_name):
    client = OpenAI(api_key=key)
    response = client.responses.create(
        model=model_name,
        instructions=(
            "あなたはLUNARIAという上品で親しみやすい占いサロンの占い師AIです。"
            "日本語で、温かく具体的で、押しつけない鑑定をしてください。"
            "占いは娯楽・自己 reflection のためのものとして扱い、未来を断定しないでください。"
            "医療・法律・投資など重大な判断を占いで指示しないでください。"
            "以下の見出しを使って読みやすく回答してください："
            "【今日の運勢】【あなたへのメッセージ】【ラッキーカラー】【ラッキーアイテム】【開運アクション】。"
            "内容は入力情報に合わせ、定型文の繰り返しを避けてください。"
        ),
        input=prompt
    )
    return response.output_text

st.markdown("""
<div class="hero">
  <div style="font-size:2rem">☾ ✧ ☽</div>
  <div class="brand">LUNARIA</div>
  <p>AI FORTUNE SALON</p>
  <div style="color:#e9d9c4">星の導きから、あなたらしい一歩を。</div>
</div>
""", unsafe_allow_html=True)

menu = st.radio("占いメニュー", ["今日の運勢", "恋愛運", "仕事運", "金運", "総合運", "二人の相性"], horizontal=True)

with st.form("fortune_form"):
    st.subheader("あなたの情報")
    col1, col2 = st.columns(2)
    with col1:
        nickname = st.text_input("ニックネーム", placeholder="例：Karin")
        birthday = st.date_input("あなたの生年月日", value=date(2004,7,16), min_value=date(1900,1,1), max_value=date.today())
    with col2:
        mood = st.selectbox("今の気分", ["前向き", "少し疲れている", "新しいことを始めたい", "恋愛が気になる", "迷っている", "特に決まっていない"])
        focus = st.text_input("気になること（任意）", placeholder="例：新しい出会い、進路、人間関係")
    partner = None
    if menu == "二人の相性":
        st.markdown("---")
        st.subheader("お相手の情報")
        partner = st.date_input("お相手の生年月日", value=date(2003,1,1), min_value=date(1900,1,1), max_value=date.today(), key="partner")
    submitted = st.form_submit_button("✧ AIに占ってもらう ✧")

if submitted:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("AI鑑定の準備がまだ完了していません。管理者がStreamlit CloudのApp settings → SecretsにOPENAI_API_KEYを設定してください。")
    elif birthday >= date.today():
        st.error("生年月日は今日より前の日付を選択してください。")
    else:
        sign = zodiac(birthday)
        number = life_path(birthday)
        details = f"ニックネーム：{nickname or '利用者'}\n生年月日：{birthday}\n星座：{sign}\n数秘術のライフパスナンバー：{number}\n占いテーマ：{menu}\n今の気分：{mood}\n気になること：{focus or '特になし'}"
        if partner:
            details += f"\nお相手の生年月日：{partner}\nお相手の星座：{zodiac(partner)}\nお相手のライフパスナンバー：{life_path(partner)}"
        prompt = details + "\n\nこの情報を参考に、テーマに沿った個別鑑定をしてください。星座・数秘術は占い上の象徴として扱い、決めつけずに前向きなアドバイスを含めてください。"
        with st.spinner("星の配置を読み解いています…"):
            try:
                answer = ask_ai(prompt, api_key, model)
                st.session_state.history.insert(0, {"menu":menu, "nickname":nickname or "あなた", "answer":answer, "date":date.today().isoformat()})
                st.markdown('<div class="result"><div class="kicker">YOUR PERSONAL READING</div><h2>✧ 鑑定結果 ✧</h2></div>', unsafe_allow_html=True)
                st.markdown(answer)
                st.caption(f"鑑定データ：{sign} ／ ライフパスナンバー {number}")
            except Exception as e:
                st.error("AIとの接続でエラーが発生しました。APIキー・利用可能なモデル・API利用状況を確認してください。")
                st.caption(f"詳細：{str(e)[:300]}")

if st.session_state.history:
    st.markdown("---")
    st.subheader("✧ このセッションの鑑定履歴")
    for i, item in enumerate(st.session_state.history[:5], 1):
        with st.expander(f"{i}. {item['date']}｜{item['nickname']}｜{item['menu']}"):
            st.write(item["answer"])

st.markdown("---")
st.markdown('<p class="smallnote">※LUNARIAは生成AIを活用した娯楽向け占いアプリです。占い結果は将来や相手の気持ちを保証するものではありません。重要な決定は現実の情報をもとに判断してください。</p>', unsafe_allow_html=True)
