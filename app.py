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

# 3. CSS 스타일: 체크박스와 글자 사이 불필요한 공백 완전 제거
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* 본문 여백 */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 520px !important;
    }

    /* 화이트 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 18px !important;
        padding: 20px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    /* 상단 타이틀 */
    .modern-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        white-space: nowrap !important;
    }

    /* 진행 바 */
    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 8px !important;
    }

    /* ★★★ 할 일 리스트 행 레이아웃 (공백 밀착 고정) ★★★ */
    .todo-row {
        margin-bottom: 2px !important;
    }
    
    .todo-row div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0px !important; /* 내부 빈틈 제거 */
        width: 100% !important;
    }

    /* 1. 체크박스 칸: 딱 체크박스 크기(34px)만 차지하고 우측으로 늘어나지 않음 */
    .todo-row div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
        width: 34px !important;
        min-width: 34px !important;
        max-width: 34px !important;
        flex: 0 0 34px !important;
        margin-right: 4px !important;
    }

    /* 2. 할 일 내용 칸: 체크박스 바로 옆에서 남은 공간을 차지 */
    .todo-row div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        width: calc(100% - 80px) !important;
    }

    /* 3. 연필 버튼 칸: 우측 끝 고정 (38px) */
    .todo-row div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) {
        width: 38px !important;
        min-width: 38px !important;
        max-width: 38px !important;
        flex: 0 0 38px !important;
        margin-left: 4px !important;
    }

    /* 연필 팝오버 버튼 규격 */
    .todo-row div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) button {
        padding: 0 !important;
        width: 36px !important;
        height: 32px !important;
        min-height: 32px !important;
        border-radius: 8px !important;
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. 카드 렌더링
with st.container(border=True):
    # 상단 헤더: 타이틀과 초기화 버튼
    col_t, col_b = st.columns([0.72, 0.28])
    with col_t:
        st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)
    with col_b:
        if st.button("🔄 초기화", key="btn_reset_header", use_container_width=True):
            for item in st.session_state.todos_5:
                item["done"] = False
            st.session_state.reset_count += 1
            st.rerun()

    st.write("")

    # 실시간 진행률 게이지 (5개 기준)
    completed = sum(1 for t in st.session_state.todos_5 if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 {completed} / 5개 ({int(progress * 100)}%)")
    st.write("")

    # 5개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos_5):
        # 행 전용 래퍼로 감싸서 공백을 밀착시킴
        st.markdown(f'<div class="todo-row">', unsafe_allow_html=True)
        c_chk, c_txt, c_pop = st.columns([1, 10, 1])
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
                st.markdown(f"<div style='color:#94a3b8; text-decoration:line-through; font-size:0.95rem; line-height:1.35; padding-left:2px;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#1e293b; font-weight:500; font-size:0.95rem; line-height:1.35; padding-left:2px;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)

        with c_pop:
            with st.popover("✏️"):
                new_text = st.text_input(f"{idx+1}번 수정", value=item["text"], key=f"edit_input5_{idx}")
                if st.button("저장", key=f"btn_save5_{idx}", use_container_width=True):
                    st.session_state.todos_5[idx]["text"] = new_text
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
