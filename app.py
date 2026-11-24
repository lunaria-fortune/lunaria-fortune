import random
import streamlit as st
from datetime import date

st.set_page_config(page_title="LUNARIA｜AI占いサロン", page_icon="🌙", layout="wide")

st.markdown("""
<style>
/* 全体：濃い背景に明るい文字 */
.stApp {background: linear-gradient(135deg,#171329 0%,#241936 55%,#34213e 100%); color:#fff7eb;}
.stApp, .stApp p, .stApp label, .stApp .stMarkdown, .stApp [data-testid="stMarkdownContainer"] {color:#fff7eb;}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {color:#f3d9ad;}
.stApp [data-testid="stCaptionContainer"], .stApp small {color:#e4d6ec !important;}
/* 入力欄は明るい面＋濃い文字にして視認性を確保 */
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] > div {background-color:#fffaf4 !important; color:#292033 !important; -webkit-text-fill-color:#292033 !important;}
.stApp input::placeholder, .stApp textarea::placeholder {color:#756b7b !important; -webkit-text-fill-color:#756b7b !important; opacity:1;}
.stApp [data-baseweb="select"] *, .stApp [role="radiogroup"] label, .stApp [role="checkbox"] label {color:#fff7eb !important;}
.stApp [data-baseweb="popover"] *, .stApp [role="listbox"] * {color:#292033 !important;}
.stApp button[kind="primary"] {color:#241936 !important;}
section[data-testid="stSidebar"] {background:#f7f5f2;}
section[data-testid="stSidebar"] * {color:#30263b !important;}
.hero {text-align:center; padding:28px 12px 20px; border:1px solid #a18ab4; border-radius:22px; background:rgba(255,255,255,.09); margin-bottom:22px;}
.hero h1 {color:#f3d9ad; letter-spacing:.12em; font-size:2.5rem; margin-bottom:4px;}
.hero p {color:#fff0dc; margin:0;}
.panel {border:1px solid #8d75a0; border-radius:16px; padding:20px; background:rgba(255,255,255,.09); margin:12px 0;}
.result {border-left:3px solid #e4c58f; padding:10px 16px; margin:12px 0; background:rgba(255,255,255,.10); border-radius:6px; color:#fff7eb;}
.result strong {color:#f3d9ad;}
.small {color:#f0e4f5 !important; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

ZODIAC = [
    ("山羊座", (12,22), (1,19)), ("水瓶座", (1,20), (2,18)), ("魚座", (2,19), (3,20)),
    ("牡羊座", (3,21), (4,19)), ("牡牛座", (4,20), (5,20)), ("双子座", (5,21), (6,21)),
    ("蟹座", (6,22), (7,22)), ("獅子座", (7,23), (8,22)), ("乙女座", (8,23), (9,22)),
    ("天秤座", (9,23), (10,23)), ("蠍座", (10,24), (11,22)), ("射手座", (11,23), (12,21)),
]

def zodiac(d):
    m, day = d.month, d.day
    for name, start, end in ZODIAC:
        if start[0] == 12:
            if (m == 12 and day >= start[1]) or (m == 1 and day <= end[1]): return name
        elif (m, day) >= start and (m, day) <= end:
            return name
    return "山羊座"

def life_path(d):
    n = sum(int(x) for x in d.strftime("%Y%m%d"))
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(x) for x in str(n))
    return n

READINGS = {
 "今日の運勢": [
  ("全体運", "小さな選択が、思いがけない良い流れにつながりそう。気になったことを一つだけ行動に移してみて。"),
  ("恋愛運", "相手の反応を急がず、自然体の会話を大切に。あなたらしい落ち着きが魅力として伝わります。"),
  ("仕事・学業運", "順番を決めて取り組むと集中力が高まりそう。最初の一歩を軽くすることが鍵。"),
  ("金運", "買う前に一呼吸置くと満足度の高い選択に。長く使えるものに目を向けて。"),
 ],
 "恋愛運": [
  ("出会い", "いつもの行動範囲から少しだけ外へ。新しい場所や会話に、次のきっかけがありそう。"),
  ("距離の縮め方", "駆け引きよりも、相手への興味を素直に示すこと。短い一言が印象に残ります。"),
  ("恋のヒント", "自分の気持ちを後回しにしないで。心地よい距離感を選ぶことが良い流れを呼びます。"),
 ],
 "仕事・学業運": [
  ("集中力", "最初に優先順位を三つまでに絞ると、迷いが減って進みやすくなります。"),
  ("対人運", "相手の得意なことを頼ってみると、協力関係が深まりそう。"),
  ("開運アクション", "机やスマートフォンの中を五分だけ整理。環境を整えると頭もすっきり。"),
 ],
 "金運": [
  ("お金の流れ", "使う目的をはっきりさせると、満足度の高いお金の使い方ができそう。"),
  ("買い物運", "比較してから選ぶのが吉。今すぐ必要かどうかを確認してみて。"),
  ("開運アクション", "今月の支出を一度見返して、無理なく続けられる小さな工夫を一つ決めて。"),
 ],
 "総合運": [
  ("今のテーマ", "焦らず、自分のペースを守ること。積み重ねてきたことが少しずつ形になりそう。"),
  ("人間関係", "相手に合わせすぎず、丁寧な言葉で自分の希望も伝えてみて。"),
  ("ラッキーアクション", "いつもより少し早く休むこと。余白をつくると新しい発想が生まれます。"),
 ],
 "二人の相性": [
  ("相性のヒント", "違いを面白がれる関係が育ちやすいとき。結論を急がず、お互いの考えを聞いてみて。"),
  ("会話の鍵", "共通の好きなことを話題にすると自然に距離が縮まりそう。"),
  ("関係を育てるコツ", "期待を一方的に重ねず、小さな約束を大切にすることが信頼につながります。"),
 ]
}

with st.sidebar:
    st.markdown("## 🌙 LUNARIA")
    st.caption("星の導きから、あなたらしい一歩を。")
    st.markdown("---")
    st.markdown("### 使い方")
    st.write("① ニックネームと生年月日を入力")
    st.write("② 占いメニューを選択")
    st.write("③「占ってもらう」を押す")
    st.markdown("---")
    st.caption("このアプリの占いは娯楽を目的としたものです。")

st.markdown('<div class="hero"><h1>☾ LUNARIA</h1><p>AI占いサロン</p><p class="small">星の導きから、あなたらしい一歩を。</p></div>', unsafe_allow_html=True)

st.markdown("### 占いメニュー")
menu = st.radio("占いたいテーマを選んでください", list(READINGS.keys()), horizontal=True, label_visibility="collapsed")

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### あなたの情報")
col1, col2 = st.columns(2)
with col1:
    nickname = st.text_input("ニックネーム", placeholder="例：ルナ")
    birthday = st.date_input("あなたの生年月日", value=date(2000, 1, 1), min_value=date(1900,1,1), max_value=date.today())
with col2:
    mood = st.selectbox("今の気分", ["前向き", "わくわく", "少し不安", "疲れ気味", "迷っている", "穏やか"])
    concern = st.text_input("気になること（任意）", placeholder="例：新しい出会い、将来のこと")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("✧ 占ってもらう ✧", type="primary", use_container_width=True):
    if not nickname.strip():
        st.warning("ニックネームを入力してね。")
    else:
        seed = f"{nickname}{birthday}{menu}{mood}{concern}{date.today()}"
        rng = random.Random(seed)
        items = rng.sample(READINGS[menu], k=len(READINGS[menu]))
        st.markdown(f"## ✦ {nickname.strip()}さんへの鑑定結果")
        st.markdown(f"**{birthday.strftime('%Y年%m月%d日')}生まれ｜{zodiac(birthday)}｜数秘ナンバー {life_path(birthday)}**")
        st.markdown(f"**今日の気分：{mood}**")
        if concern.strip():
            st.caption(f"気になること：{concern.strip()}")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"### {menu}")
        for title, body in items:
            st.markdown(f'<div class="result"><strong>{title}</strong><br>{body}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        advice = ["ラッキーカラー：ラベンダー", "ラッキーカラー：シャンパンゴールド", "ラッキーカラー：ミッドナイトブルー", "ラッキーカラー：ローズピンク"]
        st.info(rng.choice(advice) + "　｜　ラッキーアクション：自分のための時間を10分つくる")
        st.caption("※この鑑定は娯楽向けのものです。未来や相手の気持ちを保証するものではありません。")

st.markdown("---")
st.caption("LUNARIAは占いを楽しむためのアプリです。重要な決定は現実の情報も参考にしてください。")
