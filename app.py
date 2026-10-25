import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 할 일",
    page_icon="✔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 관리 (5개 할 일)
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

if "todos_5" not in st.session_state:
    st.session_state.todos_5 = [
        {"text": "오늘 플래너 및 일정 확인", "done": False},
        {"text": "핵심 과제 및 복습 마무리", "done": False},
        {"text": "집중 학습 또는 독서 30분", "done": False},
        {"text": "수분 섭취 및 가벼운 스트레칭", "done": False},
        {"text": "내일 우선순위 3가지 계획", "done": False},
    ]

# 체크박스 클릭 즉시 상태 동기화
def toggle_todo(index, key_name):
    st.session_state.todos_5[index]["done"] = st.session_state[key_name]

# 3. CSS 스타일: 모바일 줄바꿈 강제 방지 (1줄 유지 핵심)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* 상하좌우 여백 */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 520px !important;
    }

    /* 메인 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 18px !important;
        padding: 18px 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    .modern-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        white-space: nowrap !important;
    }

    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 8px !important;
    }

    /* ★ 핵심: Streamlit의 모든 모바일 세로 꺾임(flex-direction: column)을 1줄(row)로 강제 고정 ★ */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 6px !important;
        width: 100% !important;
        margin-bottom: 2px !important;
    }

    /* 1. 체크박스 칸: 딱 들어맞게 폭 32px 고정 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
        width: 32px !important;
        min-width: 32px !important;
        max-width: 32px !important;
        flex: 0 0 32px !important;
    }

    /* 2. 할 일 텍스트 칸: 남은 가로 공간을 채움 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
        width: auto !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 3. 수정 버튼 칸: 폭 40px 고정 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
        width: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        flex: 0 0 40px !important;
    }

    /* 팝오버 연필 버튼 여백 축소 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) button {
        padding: 2px 0 !important;
        width: 36px !important;
        height: 32px !important;
        min-height: 32px !important;
        border-radius: 8px !important;
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* 상단 헤더 전용(제목/초기화버튼) 컬럼 비율 복원 */
    div.header-row > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
        flex: 1 1 auto !important;
        width: auto !important;
        max-width: none !important;
    }
    div.header-row > div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
        flex: 0 0 76px !important;
        width: 76px !important;
        min-width: 76px !important;
        max-width: 76px !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. 카드 렌더링
with st.container(border=True):
    # 상단 헤더 (제목 + 초기화 버튼)
    st.markdown('<div class="header-row">', unsafe_allow_html=True)
    h_col1, h_col2 = st.columns([0.75, 0.25])
    with h_col1:
        st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)
    with h_col2:
        if st.button("🔄 초기화", key="btn_reset_all", use_container_width=True):
            for item in st.session_state.todos_5:
                item["done"] = False
            st.session_state.reset_count += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # 실시간 진행률 게이지 (5개 기준)
    completed = sum(1 for t in st.session_state.todos_5 if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 {completed} / 5개 ({int(progress * 100)}%)")
    st.write("")

    # 5개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos_5):
        # 컬럼 3개 생성 (1: 체크박스, 2: 텍스트, 3: 수정)
        c_chk, c_txt, c_pop = st.columns([1, 8, 1])
        chk_key = f"chk5_{st.session_state.reset_count}_{idx}"
        
        with c_chk:
            st.checkbox(
                "",
                value=item["done"],
                key=chk_key,
                on_change=toggle_todo,
                args=(idx, chk_key),
                label_visibility="collapsed"
            )

        with c_txt:
            if item["done"]:
                st.markdown(f"<div style='color:#94a3b8; text-decoration:line-through; font-size:0.94rem; line-height:1.3;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#1e293b; font-weight:500; font-size:0.94rem; line-height:1.3;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)

        with c_pop:
            with st.popover("✏️"):
                new_text = st.text_input(f"{idx+1}번 수정", value=item["text"], key=f"edit_input5_{idx}")
                if st.button("저장", key=f"btn_save5_{idx}", use_container_width=True):
                    st.session_state.todos_5[idx]["text"] = new_text
                    st.rerun()
