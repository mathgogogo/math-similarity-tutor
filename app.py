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

# 체크박스 클릭 즉시 동기화
def toggle_todo(index, key_name):
    st.session_state.todos_5[index]["done"] = st.session_state[key_name]

# 3. CSS 스타일: 모바일 1줄 고정 & 불필요한 위아래 여백 압축
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* 상단 여백을 컴팩트하게 조정하여 스크롤 방지 */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 480px !important;
    }

    /* 메인 화이트 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 16px 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    .modern-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        white-space: nowrap !important;
    }

    /* 게이지 바 */
    .stProgress {
        margin-top: -6px !important;
        margin-bottom: 8px !important;
    }
    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 6px !important;
    }

    /* 모바일 세로 꺾임 방지 (무조건 가로 1줄 유지) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 6px !important;
        width: 100% !important;
        margin-bottom: 2px !important;
    }

    /* 좌측 체크박스+텍스트 영역 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 우측 버튼 영역 (초기화 및 연필 버튼) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        flex: 0 0 auto !important;
        width: auto !important;
    }

    /* 체크박스와 글자 사이의 불필요한 빈틈 제거 및 정렬 */
    div[data-testid="stCheckbox"] {
        min-height: auto !important;
        margin-bottom: 0 !important;
    }
    div[data-testid="stCheckbox"] label {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 4px 0 !important;
    }
    div[data-testid="stCheckbox"] label p {
        font-size: 0.93rem !important;
        margin: 0 !important;
        line-height: 1.35 !important;
        word-break: keep-all !important;
    }

    /* 연필 ✏️ 버튼 미니멀 규격 */
    div[data-testid="stPopover"] button {
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0 !important;
        width: 34px !important;
        height: 32px !important;
        min-height: 32px !important;
    }

    /* 초기화 버튼 */
    #btn_reset_header {
        border-radius: 8px !important;
        padding: 3px 10px !important;
        font-size: 0.85rem !important;
        height: 32px !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. 카드 렌더링
with st.container(border=True):
    # 상단 헤더: 타이틀과 초기화 버튼 (한 줄 나란히 배치)
    col_t, col_b = st.columns([0.72, 0.28])
    with col_t:
        st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)
    with col_b:
        if st.button("🔄 초기화", key="btn_reset_header"):
            for item in st.session_state.todos_5:
                item["done"] = False
            st.session_state.reset_count += 1
            st.rerun()

    # 실시간 진행률 게이지 (5개 기준)
    completed = sum(1 for t in st.session_state.todos_5 if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 {completed} / 5개 ({int(progress * 100)}%)")

    # 5개 체크리스트 목록 (각각 가로 1줄로 고정)
    for idx, item in enumerate(st.session_state.todos_5):
        c_item, c_edit = st.columns([0.88, 0.12])
        chk_key = f"chk5_{st.session_state.reset_count}_{idx}"
        
        # 완료 시 취소선 및 슬레이트 그레이 색상 적용
        if item["done"]:
            label_text = f"~:gray[{idx+1}. {item['text']}]~"
        else:
            label_text = f"**{idx+1}. {item['text']}**"

        with c_item:
            st.checkbox(
                label_text,
                value=item["done"],
                key=chk_key,
                on_change=toggle_todo,
                args=(idx, chk_key)
            )

        with c_edit:
            with st.popover("✏️"):
                new_text = st.text_input(f"{idx+1}번 수정", value=item["text"], key=
