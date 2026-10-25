import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 할 일",
    page_icon="✔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 관리
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

if "todos" not in st.session_state:
    st.session_state.todos = [
        {"text": "오늘 플래너 및 일정 확인", "done": False},
        {"text": "핵심 과제 및 복습 마무리", "done": False},
        {"text": "집중 학습 또는 독서 30분", "done": False},
        {"text": "수분 섭취 및 가벼운 스트레칭", "done": False},
        {"text": "필요한 물품 및 준비물 챙기기", "done": False},
        {"text": "중요 연락 및 메일 회신", "done": False},
        {"text": "책상 및 주변 환경 정돈", "done": False},
        {"text": "하루 성과 3가지 기록", "done": False},
        {"text": "마음 정리 및 휴식 시간 갖기", "done": False},
        {"text": "내일 우선순위 3가지 계획", "done": False},
    ]

# 체크박스 클릭 즉시 상태 동기화
def toggle_todo(index, key_name):
    st.session_state.todos[index]["done"] = st.session_state[key_name]

# 3. 핵심 CSS: 모바일 및 좁은 해상도 강제 1줄 배치 (No-wrap)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* 상단 여백 확보 및 모바일 좌우 여백 최적화 */
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
        padding: 20px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    .modern-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 8px !important;
    }

    /* ★★★ 모바일에서 컬럼이 밑으로 떨어지는 것 방지 ★★★ */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 절대 줄바꿈 되지 않음 */
        align-items: center !important;
        gap: 8px !important;
        margin-bottom: 4px !important;
    }

    /* 체크박스 영역 고정 너비 및 여백 축소 */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) {
        flex: 0 0 28px !important;
        min-width: 28px !important;
        width: 28px !important;
    }

    /* 텍스트 영역 유연한 확장 */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 수정 버튼 영역 고정 너비 */
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) {
        flex: 0 0 38px !important;
        min-width: 38px !important;
        width: 38px !important;
    }

    /* 수정 팝오버 버튼 미니멀 아이콘 스타일 */
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
    st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)

    # 진행률 게이지
    completed = sum(1 for t in st.session_state.todos if t["done"])
    progress = completed / 10.0
    st.progress(progress, text=f"완료 {completed} / 10개 ({int(progress * 100)}%)")
    st.write("")

    # 10개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos):
        c_chk, c_txt, c_pop = st.columns([1, 8, 1])
        chk_key = f"chk_{st.session_state.reset_count}_{idx}"
        
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
                st.markdown(f"<div style='color:#94a3b8; text-decoration:line-through; font-size:0.92rem; word-break:keep-all; line-height:1.35;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#1e293b; font-weight:500; font-size:0.92rem; word-break:keep-all; line-height:1.35;'>{idx+1}. {item['text']}</div>", unsafe_allow_html=True)

        with c_pop:
            # 좁은 화면에서도 차지하지 않도록 아이콘(✏️) 단독 표시
            with st.popover("✏️"):
                new_text = st.text_input(f"{idx+1}번 수정", value=item["text"], key=f"edit_input_{idx}")
                if st.button("저장", key=f"btn_save_{idx}", use_container_width=True):
                    st.session_state.todos[idx]["text"] = new_text
                    st.rerun()

    st.write("")
    
    # 체크 표시 전체 초기화 버튼
    if st.button("🔄 체크 표시 전체 초기화", use_container_width=True):
        for item in st.session_state.todos:
            item["done"] = False
        st.session_state.reset_count += 1
        st.rerun()
