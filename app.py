import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="오늘의 할 일 🎀",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 10대 감성 파스텔 핑크/라벤더 커스텀 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 사랑스러운 파스텔 그라데이션 배경 */
    .stApp {
        background: linear-gradient(145deg, #fff5f7 0%, #fdf2f8 50%, #f5f3ff 100%);
    }

    /* 상단 기본 여백 축소 */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 580px !important;
    }

    /* 다이어리 느낌의 뽀송한 화이트 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.92) !important;
        border: 2px solid #ffd6e0 !important;
        border-radius: 24px !important;
        padding: 18px 20px !important;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.2) !important;
    }

    /* 타이틀 폰트 & 뱃지 */
    .diary-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #ff5d8f;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 6px;
    }
    
    /* 프로그레스 바 핑크 커스텀 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff9ebb, #ff5d8f) !important;
        border-radius: 12px !important;
    }

    /* 체크박스 행 간격 최적화 */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        margin-bottom: -5px;
        padding: 3px 0;
    }

    /* 수정 팝오버 버튼 큐티 스타일 */
    button[kind="secondary"] {
        background-color: #fff0f3 !important;
        color: #ff5d8f !important;
        border: 1px solid #ffccd5 !important;
        border-radius: 10px !important;
        padding: 2px 7px !important;
        font-size: 0.8rem !important;
    }
    button[kind="secondary"]:hover {
        background-color: #ffe3e8 !important;
        border-color: #ffb3c1 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 10대 감성에 맞춘 10가지 기본 할 일 세션
if "teen_todos" not in st.session_state:
    st.session_state.teen_todos = [
        {"text": "오늘 플래너 & 시간표 확인하기 📝", "done": False},
        {"text": "수학 숙제 & 복습 끝내기 📐", "done": False},
        {"text": "좋아하는 노래 들으며 힐링 🎧", "done": False},
        {"text": "영어 단어 15개 외우기 🔤", "done": False},
        {"text": "물 1L 이상 자주 마시기 💧", "done": False},
        {"text": "가벼운 스트레칭 & 바른 자세 🧘‍♀️", "done": False},
        {"text": "친구한테 다정한 말 한마디 건네기 💬", "done": False},
        {"text": "책상 위 깔끔하게 정리하기 🫧", "done": False},
        {"text": "하루 일기 또는 감사한 일 쓰기 🎀", "done": False},
        {"text": "내일 입을 옷 & 챙길 물건 미리 챙기기 🎒", "done": False},
    ]

# 4. 카드 렌더링
with st.container(border=True):
    # 감성 헤더
    st.markdown('<div class="diary-title">✨ 오늘의 할 일 🎀</div>', unsafe_allow_html=True)

    # 진행률 게이지
    completed = sum(1 for t in st.session_state.teen_todos if t["done"])
    progress = completed / 10.0
    st.progress(progress, text=f"💖 오늘 달성도: {completed} / 10개 ({int(progress * 100)}%)")
    st.write("")

    # 10개 체크리스트 렌더링
    for idx, item in enumerate(st.session_state.teen_todos):
        c_chk, c_txt, c_pop = st.columns([0.08, 0.77, 0.15])
        
        with c_chk:
            checked = st.checkbox("", value=item["done"], key=f"teen_chk_{idx}", label_visibility="collapsed")
            st.session_state.teen_todos[idx]["done"] = checked

        with c_txt:
            if item["done"]:
                # 완료 시 딸기우유빛 연회색 + 취소선
                st.markdown(f"<span style='color:#c08497; text-decoration:line-through; font-size:0.94rem;'>{idx+1}. {item['text']}</span>", unsafe_allow_html=True)
            else:
                # 미완료 시 또렷한 다크 플럼/핑크 톤
                st.markdown(f"<span style='color:#4a2835; font-weight:600; font-size:0.94rem;'>{idx+1}. {item['text']}</span>", unsafe_allow_html=True)

        with c_pop:
            with st.popover("✏️"):
                new_text = st.text_input(f"{idx+1}번 수정하기", value=item["text"], key=f"teen_edit_{idx}")
                if st.button("저장 꾹!", key=f"teen_btn_{idx}", use_container_width=True):
                    st.session_state.teen_todos[idx]["text"] = new_text
                    st.rerun()

    st.write("")
    
    # 핑크 리셋 버튼
    if st.button("🫧 체크표시 전부 비우고 새로 시작하기", use_container_width=True):
        for item in st.session_state.teen_todos:
            item["done"] = False
        st.rerun()
