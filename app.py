import json
import os
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 할 일",
    page_icon="✔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 로컬 파일 영구 저장/불러오기 함수
DATA_FILE = "my_todos.json"

DEFAULT_TODOS = [
    {"text": "오늘 플래너 및 일정 확인", "done": False},
    {"text": "핵심 과제 및 복습 마무리", "done": False},
    {"text": "집중 학습 또는 독서 30분", "done": False},
    {"text": "수분 섭취 및 가벼운 스트레칭", "done": False},
    {"text": "내일 우선순위 3가지 계획", "done": False},
]

def load_todos():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_TODOS
    return DEFAULT_TODOS

def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

# 3. 세션 상태 초기화
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

if "todos_5" not in st.session_state:
    st.session_state.todos_5 = load_todos()

# 체크박스 클릭 즉시 반영 및 파일 저장
def toggle_todo(index, key_name):
    st.session_state.todos_5[index]["done"] = st.session_state[key_name]
    save_todos(st.session_state.todos_5)

# 4. CSS 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 480px !important;
    }

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

    .stProgress {
        margin-top: 6px !important;
        margin-bottom: 8px !important;
    }
    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 6px !important;
    }

    /* ★★★ 제목 바로 옆에 초기화 버튼 밀착시키는 헤더 스타일 ★★★ */
    .title-wrapper {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        margin-bottom: 4px !important;
    }

    .title-wrapper div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        width: 100% !important;
    }

    .title-wrapper div[data-testid="column"]:nth-child(1) {
        flex: 0 0 auto !important;
        width: auto !important;
    }

    .title-wrapper div[data-testid="column"]:nth-child(2) {
        flex: 0 0 auto !important;
        width: auto !important;
    }

    .title-wrapper button {
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        color: #475569 !important;
        border-radius: 8px !important;
        padding: 2px 10px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        height: 28px !important;
        min-height: 28px !important;
        white-space: nowrap !important;
    }

    /* 체크리스트 행 가로 1줄 고정 */
    div[data-testid="stVerticalBlock"] > div.element-container + div[data-testid="stHorizontalBlock"]:not(.title-wrapper div) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 6px !important;
        width: 100% !important;
        margin-bottom: 2px !important;
    }

    /* 체크박스 영역 밀착 */
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

    /* ✏️ 연필 버튼 */
    div[data-testid="stPopover"] button {
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0 !important;
        width: 34px !important;
        height: 32px !important;
        min-height: 32px !important;
    }
</style>
""", unsafe_allow_html=True)

# 5. 카드 렌더링
with st.container(border=True):
    # 상단 헤더: "오늘의 할 일" 제목 바로 우측에 초기화 버튼 밀착
    st.markdown('<div class="title-wrapper">', unsafe_allow_html=True)
    c_title, c_btn = st.columns([0.01, 0.99])
    with c_title:
        st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)
    with c_btn:
        if st.button("🔄 초기화", key="btn_reset_header"):
            for item in st.session_state.todos_5:
                item["done"] = False
            save_todos(st.session_state.todos_5)
            st.session_state.reset_count += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 실시간 진행률 게이지 (5개 기준)
    completed = sum(1 for t in st.session_state.todos_5 if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 {completed} / 5개 ({int(progress * 100)}%)")

    # 5개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos_5):
        c_item, c_edit = st.columns([0.88, 0.12])
        chk_key = f"chk5_{st.session_state.reset_count}_{idx}"
        
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
                new_text = st.text_input(f"{idx+1}번 수정", value=item["text"], key=f"edit_input5_{idx}")
                if st.button("저장", key=f"btn_save5_{idx}", use_container_width=True):
                    st.session_state.todos_5[idx]["text"] = new_text
                    save_todos(st.session_state.todos_5)
                    st.rerun()
