import datetime
import urllib.parse
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="나만의 일일 대시보드",
    page_icon="☀️",
    layout="wide"
)

# ----------------- 세션 상태 (할 일 5개 초기화) -----------------
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"text": "수업 지도안 검토하기", "done": False},
        {"text": "주요 뉴스 및 증시 확인", "done": False},
        {"text": "스트레칭 및 가벼운 운동", "done": False},
        {"text": "하루 감사한 일 3가지 적기", "done": False},
        {"text": "내일 계획 10분 정리", "done": False},
    ]

# ----------------- 상단: 시간 & 날씨 위젯 -----------------
col_time, col_weather = st.columns([1.5, 1])

with col_time:
    now = datetime.datetime.now()
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    day_str = days[now.weekday()]
    st.subheader(f"📅 {now.strftime('%Y년 %m월 %d일')} ({day_str})")
    st.markdown(f"### ⏰ 현재 시각 : **{now.strftime('%H:%M')}**")

with col_weather:
    st.subheader("🌤️ 오늘의 날씨")
    try:
        # Open-Meteo 무료 API (창원 기준 위경도: 35.228, 128.681)
        url = "https://api.open-meteo.com/v1/forecast?latitude=35.228&longitude=128.681&current_weather=true"
        res = requests.get(url, timeout=3).json()
        current = res.get("current_weather", {})
        temp = current.get("temperature", "--")
        wind = current.get("windspeed", "--")
        st.write(f"📍 **현재 기온:** `{temp}°C` | **풍속:** `{wind} km/h`")
    except Exception:
        st.caption("날씨 정보를 불러오는 중입니다.")

st.divider()

# ----------------- 중앙: 듀얼 포털 검색 -----------------
st.subheader("🔍 빠른 포털 검색")
col_engine, col_input = st.columns([1, 4])

with col_engine:
    search_engine = st.radio("검색 포털 선택", ["구글 (Google)", "네이버 (Naver)"], horizontal=True)

with col_input:
    query = st.text_input("검색어를 입력하고 엔터를 치거나 검색 버튼을 누르세요", key="search_query")
    if query:
        encoded_query = urllib.parse.quote(query)
        if "구글" in search_engine:
            target_url = f"https://www.google.com/search?q={encoded_query}"
        else:
            target_url = f"https://search.naver.com/search.naver?query={encoded_query}"
        
        st.markdown(f"👉 **[선택한 포털에서 '{query}' 검색 결과 열기]({target_url})**")

st.divider()

# ----------------- 하단: 오늘의 할 일 5개 (수정 & 체크) -----------------
completed_count = sum(1 for item in st.session_state.todos if item["done"])
progress = completed_count / 5.0

st.subheader("🎯 오늘의 핵심 할 일 (TOP 5)")
st.progress(progress, text=f"진행도: {completed_count}/5 완료 ({int(progress * 100)}%)")

# 할 일 체크박스 및 인라인 수정 아코디언
for idx, item in enumerate(st.session_state.todos):
    cols = st.columns([0.1, 0.7, 0.2])
    with cols[0]:
        # 완료 체크박스
        is_done = st.checkbox("", value=item["done"], key=f"check_{idx}")
        st.session_state.todos[idx]["done"] = is_done
    
    with cols[1]:
        # 텍스트 표시 (완료 시 취소선)
        if item["done"]:
            st.markdown(f"~~{item['text']}~~")
        else:
            st.write(item["text"])
            
    with cols[2]:
        # 바로 수정할 수 있는 드롭다운
        with st.popover("✏️ 수정"):
            new_text = st.text_input("할 일 내용", value=item["text"], key=f"edit_input_{idx}")
            if st.button("저장", key=f"save_btn_{idx}"):
                st.session_state.todos[idx]["text"] = new_text
                st.rerun()

st.write("")
col_b1, _ = st.columns([1, 4])
with col_b1:
    if st.button("🔄 체크 상태 초기화"):
        for item in st.session_state.todos:
            item["done"] = False
        st.rerun()
