import datetime
import urllib.parse
import requests
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="My Daily Workspace",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 구글 머티리얼 디자인 스타일(CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Product+Sans:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stApp {
        background-color: #f8fafd;
    }
    .g-card {
        background: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(60,64,67, 0.08), 0 4px 8px rgba(60,64,67, 0.04);
    }
    .g-title {
        font-family: 'Product Sans', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .c-blue { color: #4285F4; }
    .c-red { color: #EA4335; }
    .c-yellow { color: #FBBC05; }
    .c-green { color: #34A853; }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #202124;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 할 일 5개 세션 상태 초기화 (문법 오류 수정 부분)
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"text": "수업 지도안 검토하기", "done": False},
        {"text": "주요 뉴스 및 증시 확인", "done": False},
        {"text": "스트레칭 및 가벼운 운동", "done": False},
        {"text": "하루 감사한 일 3가지 적기", "done": False},
        {"text": "내일 계획 10분 정리", "done": False}
    ]

# 4. 상단 구글 스타일 타이틀
st.markdown("""
<div class="g-title">
    <span class="c-blue">M</span><span class="c-red">y</span> 
    <span class="c-blue">G</span><span class="c-red">o</span><span class="c-yellow">o</span><span class="c-blue">g</span><span class="c-green">l</span><span class="c-red">e</span> 
    <span style="color:#5f6368; font-weight:400;">Workspace</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# [카드 1] 시간 및 실시간 날씨
# ==========================================
with st.container():
    st.markdown('<div class="g-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⏱️ 시간 & 실시간 날씨</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        now = datetime.datetime.now()
        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        day_korean = weekdays[now.weekday()]
        st.markdown(f"**📅 {now.strftime('%Y년 %m월 %d일')} ({day_korean})**")
        st.markdown(f"### 🕒 **{now.strftime('%H:%M')}**")
    
    with col2:
        try:
            url = "https://api.open-meteo.com/v1/forecast?latitude=35.228&longitude=128.681&current_weather=true"
            res = requests.get(url, timeout=3).json()
            weather = res.get("current_weather", {})
            temp = weather.get("temperature", "--")
            wind = weather.get("windspeed", "--")
            st.markdown(f"📍 **현재 기온:** `{temp}°C`")
            st.markdown(f"💨 **풍속:** `{wind} km/h`")
        except Exception:
            st.caption("날씨 정보를 불러오는 중입니다.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# [카드 2] 빠른 포털 검색
# ==========================================
with st.container():
    st.markdown('<div class="g-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔍 빠른 포털 검색</div>', unsafe_allow_html=True)
    
    portal = st.radio(
        "검색 포털",
        options=["구글 (Google)", "네이버 (NAVER)"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    placeholder_text = "Google 검색" if "Google" in portal else "네이버 검색"
    query = st.text_input("검색창", placeholder=placeholder_text, label_visibility="collapsed")
    
    if query:
        encoded_query = urllib.parse.quote(query)
        if "Google" in portal:
            url = f"https://www.google.com/search?q={encoded_query}"
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none;">
                <button style="background:#4285F4; color:#fff; border:none; padding:8px 18px; border-radius:8px; font-weight:500; cursor:pointer;">
                    Google에서 '{query}' 검색 결과 열기 ↗
                </button>
            </a>
            """, unsafe_allow_html=True)
        else:
            url = f"https://search.naver.com/search.naver?query={encoded_query}"
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none;">
                <button style="background:#03C75A; color:#fff; border:none; padding:8px 18px; border-radius:8px; font-weight:500; cursor:pointer;">
                    네이버에서 '{query}' 검색 결과 열기 ↗
                </button>
            </a>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# [카드 3] 오늘의 핵심 할 일 5개
# ==========================================
with st.container():
    st.markdown('<div class="g-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 오늘의 할 일 (Top 5 Tasks)</div>', unsafe_allow_html=True)
    
    completed = sum(1 for t in st.session_state.todos if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 진행률: {completed} / 5 항목 ({int(progress * 100)}%)")
    st.write("")

    for idx, item in enumerate(st.session_state.todos):
        col_chk, col_txt, col_edit = st.columns([0.1, 0.7, 0.2])
        
        with col_chk:
            checked = st.checkbox("", value=item["done"], key=f"todo_chk_{idx}")
            st.session_state.todos[idx]["done"] = checked

        with col_txt:
            if item["done"]:
                st.markdown(f"<span style='color:#9aa0a6; text-decoration:line-through;'>{item['text']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:#202124; font-weight:500;'>{item['text']}</span>", unsafe_allow_html=True)

        with col_edit:
            with st.popover("수정"):
                new_val = st.text_input("내용 편집", value=item["text"], key=f"input_edit_{idx}")
                if st.button("확인", key=f"btn_save_{idx}"):
                    st.session_state.todos[idx]["text"] = new_val
                    st.rerun()

    st.write("")
    if st.button("🔄 완료 상태 전체 해제", use_container_width=True):
        for item in st.session_state.todos:
            item["done"] = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
