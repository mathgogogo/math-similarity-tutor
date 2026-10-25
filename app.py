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

# 3. CSS 스타일 (상단 헤더와 체크리스트 행 완벽 분리)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* 상단 여백 및 모바일 여백 */
    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 580px !important;
    }

    /* 메인 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 18px !important;
        padding: 22px 18px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    /* 상단 헤더 컨테이너: 가로 정렬 & 줄바꿈 절대 방지 */
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 8px;
    }

    .modern-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a;
        white-space: nowrap !important; /* 가로 한 줄 강제 */
        letter-spacing: -0.5px;
    }

    /* 게이지 바 색상 */
    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 8px !important;
    }

    /* ★★★ 체크리스트 목록 영역만 가로 1줄 고정 적용 ★★★ */
    div[data-testid="stVerticalBlock"] > div.element-container:has(.todo-item-marker) + div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 8px !important;
        margin-bottom: 4px !important;
    }

    /* 체크박스 고정 너비 */
    div[data-testid="stVerticalBlock"] > div.element-container:has(.todo-item-marker) + div[data-testid="stHorizontalBlock"] > div:nth-child(1) {
        flex: 0 0 28px !important;
        min-width: 28px !important;
        width: 28px !important;
    }

    /* 할 일 텍스트 가변 확장 */
    div[data-testid="stVerticalBlock"] > div.element-container:has(.todo-item-marker) + div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 수정 버튼 고정 너비 */
    div[data-testid="stVerticalBlock"] > div.element-container:has(.todo-item-marker) + div[data-testid="stHorizontalBlock"] > div:nth-child(3) {
        flex: 0 0 38px !important;
        min-width: 38px !important;
        width: 38px !important;
    }

    /* 팝오버 ✏️ 버튼 스타일 */
    button[kind="secondary"] {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 3px 0 !important;
        width: 36px !important;
        height: 32px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. 카드 렌더링
with st.container(border=True):
    # 상단: 가로 한 줄로 완벽 고정된 헤더와 우측 초기화 버튼
    col_title, col_reset = st.columns([0.7, 0.3])
    with col_title:
        st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)
    with col_reset:
        if st.button("🔄 초기화", use_container_width=True):
            for item in st.session_state.todos_5:
                item["done"] = False
            st.session_state.reset_count += 1
            st.rerun()

    st.write("")

    # 실시간 진행률 게이지 계산
    completed = sum(1 for t in st.session_state.todos_5 if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 {completed} / 5개 ({int(progress * 100)}%)")
    st.write("")

    # 5개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos_5):
        # 체크리스트 행 전용 마커 (상단 헤더에 영향을 주지 않도록 구분)
        st.markdown('<div class="todo-item-marker" style="display:none;"></div>', unsafe_allow_html=True)
        
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
                st.markdown(f"<div style='color:#94a3b8; text-decoration:line-through; font-size:0.95rem; word-break:keep-all; line-height:1.35;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#1e293b; font-weight:500; font-size:0.95rem; word-break:keep-all; line-height:1.35;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)

        with c_pop:
            with st.popover("✏️"):
                new_text = st.text_input(f"{idx+1}번 수정", value=item["text"], key=f"edit_input5_{idx}")
                if st.button("저장", key=f"btn_save5_{idx}", use_container_width=True):
                    st.session_state.todos_5[idx]["text"] = new_text
                    st.rerun()
