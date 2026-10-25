import datetime
import urllib.parse
import requests
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Google Workspace Dashboard",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 구글 미니멀 & 카드 구분 스타일 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&family=Product+Sans:wght@700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 캔버스 배경색 */
    .stApp {
        background-color: #f1f3f4;
    }

    /* 카드 테두리 및 그림자 강화 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #e0e2e6 !important;
        border-radius: 20px !important;
        padding: 22px 24px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 1px 3px rgba(60,64,67, 0.08), 0 4px 12px rgba(60,64,67, 0.04);
    }

    /* 상단 로고 타이틀 */
    .g-header {
        text-align: center;
        margin: 10px 0 25px 0;
    }
    .g-logo {
        font-family: 'Product Sans', sans-serif;
        font-size: 2.3rem;
        letter-spacing: -0.5px;
    }
    .c-blue { color: #4285F4; }
    .c-red { color: #EA4335; }
    .c-yellow { color: #FBBC05; }
    .c-green { color: #34A853; }
    
    /* 카드 헤더 배지 스타일 */
    .card-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.95rem;
        font-weight: 700;
        color: #3c4043;
        background: #f8f9fa;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #eaedf0;
        margin-bottom: 16px;
    }

    /* 날씨·시간 내부 분할선 */
    .weather-box {
        background: #f8fafd;
        border: 1px solid #e3e8ee;
        border-radius: 14px;
        padding: 12px 16px;
    }

    /* 팝오버 버튼 미니멀화 */
    button[kind="secondary"] {
        border-radius: 10px !important;
        border: 1px solid #dadce0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 할 일 세션 초기화 (5개)
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"text": "수업 지도안 및 강의자료 점검", "done": False},
        {"text": "오늘 주요 뉴스 & 증시 동향 확인", "done": False},
        {"text": "스트레칭 및 가벼운 유산소 운동", "done": False},
        {"text": "하루 감사한 일 3가지 기록", "done": False},
        {"text": "내일 스케줄 10분 마감 점검", "done": False}
    ]

# 4. 상단 브랜드 헤더
st.markdown("""
<div class="g-header">
    <div class="g-logo">
        <span class="c-blue">G</span><span class="c-red">o</span><span class="c-yellow">o</span><span class="c-blue">g</span><span class="c-green">l</span><span class="c-red">e</span> 
        <span style="color:#3c4043; font-weight:500; font-size:1.8rem;">Daily Hub</span>
    </div>
    <div style="color: #70757a; font-size: 0.9rem; margin-top: 4px;">스마트한 하루를 위한 올인원 워크스페이스</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# [블록 1] 시간 & 실시간 날씨
# ==========================================
with st.container(border=True):
    st.markdown('<div class="card-badge">⏱️ DATE & WEATHER</div>', unsafe_allow_html=True)
    
    col_t, col_w = st.columns([1.1, 1], gap="medium")
    
    with col_t:
        now = datetime.datetime.now()
        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        day_korean = weekdays[now.weekday()]
        
        st.caption(f"{now.strftime('%Y년 %m월 %d일')} ({day_korean})")
        st.markdown(f"<div style='font-size: 2.2rem; font-weight:700; color:#1a73e8; line-height:1;'>{now.strftime('%H:%M')}</div>", unsafe_allow_html=True)
        st.write("")
        st.caption("✨ 오늘도 생산적인 하루 되세요!")

    with col_w:
        st.markdown('<div class="weather-box">', unsafe_allow_html=True)
        try:
            # Open-Meteo 실시간 기상 API (창원 기준)
            url = "https://api.open-meteo.com/v1/forecast?latitude=35.228&longitude=128.681&current_weather=true"
            res = requests.get(url, timeout=3).json()
            weather = res.get("current_weather", {})
            temp = weather.get("temperature", "--")
            wind = weather.get("windspeed", "--")
            
            st.markdown(f"🌡️ **현재 기온:** <span style='font-size:1.2rem; font-weight:700; color:#202124;'>{temp}°C</span>", unsafe_allow_html=True)
            st.markdown(f"💨 **풍속:** `{wind} km/h`")
            st.caption("📍 위치: 경남 창원시 기준")
        except Exception:
            st.caption("날씨 정보를 동기화하는 중입니다.")
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# [블록 2] 구글 & 네이버 빠른 통합 검색
# ==========================================
with st.container(border=True):
    st.markdown('<div class="card-badge">🔍 SEARCH ENGINE</div>', unsafe_allow_html=True)
    
    portal = st.segmented_control(
        "검색 포털",
        options=["Google", "NAVER"],
        default="Google",
        label_visibility="collapsed"
    )
    
    placeholder_text = "Google에서 검색할 내용을 입력하세요" if portal == "Google" else "네이버에서 검색할 내용을 입력하세요"
    query = st.text_input("통합검색", placeholder=placeholder_text, label_visibility="collapsed")
    
    if query:
        encoded_query = urllib.parse.quote(query)
        if portal == "Google":
            url = f"https://www.google.com/search?q={encoded_query}"
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none; display:inline-block; margin-top:8px;">
                <button style="background-color:#1a73e8; color:#ffffff; border:none; padding:9px 18px; border-radius:10px; font-weight:600; cursor:pointer;">
                    🔍 Google에서 '{query}' 바로 검색 ↗
                </button>
            </a>
            """, unsafe_allow_html=True)
        else:
            url = f"https://search.naver.com/search.naver?query={encoded_query}"
            st.markdown(f"""
            <a href="{url}" target="_blank" style="text-decoration:none; display:inline-block; margin-top:8px;">
                <button style="background-color:#03C75A; color:#ffffff; border:none; padding:9px 18px; border-radius:10px; font-weight:600; cursor:pointer;">
                    🔍 네이버에서 '{query}' 바로 검색 ↗
                </button>
            </a>
            """, unsafe_allow_html=True)


# ==========================================
# [블록 3] 오늘의 핵심 5가지 체크리스트
# ==========================================
with st.container(border=True):
    st.markdown('<div class="card-badge">📋 TODAY\'S TOP 5 TASKS</div>', unsafe_allow_html=True)
    
    # 진행도 바 계산
    completed = sum(1 for t in st.session_state.todos if t["done"])
    progress = completed / 5.0
    
    st.progress(progress, text=f"완료 진행률: {completed} / 5개 달성 ({int(progress * 100)}%)")
    st.write("")

    # 5개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos):
        c_chk, c_txt, c_pop = st.columns([0.09, 0.73, 0.18])
        
        with c_chk:
            checked = st.checkbox("", value=item["done"], key=f"item_chk_{idx}")
            st.session_state.todos[idx]["done"] = checked

        with c_txt:
            if item["done"]:
                st.markdown(f"<div style='margin-top:4px; color:#9aa0a6; text-decoration:line-through;'>{item['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='margin-top:4px; color:#202124; font-weight:500;'>{item['text']}</div>", unsafe_allow_html=True)

        with c_pop:
            with st.popover("✏️"):
                new_text = st.text_input("할 일 변경", value=item["text"], key=f"edit_val_{idx}")
                if st.button("적용", key=f"save_btn_{idx}", use_container_width=True):
                    st.session_state.todos[idx]["text"] = new_text
                    st.rerun()

    st.divider()
    
    # 하단 유틸리티 버튼
    if st.button("🔄 체크 표시 모두 지우기 (초기화)", use_container_width=True):
        for item in st.session_state.todos:
            item["done"] = False
        st.rerun()
