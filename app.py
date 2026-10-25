import json
import os
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘도 건강해지자!",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 로컬 파일 영구 저장/불러오기
DATA_FILE = "my_todos.json"

DEFAULT_DATA = {
    "completion_count": 0,
    "todos": [
        {"text": "턱걸이 20개", "done": False},
        {"text": "팔굽혀펴기 20개", "done": False},
        {"text": "스쿼트 50개", "done": False},
        {"text": "유머 ai대화", "done": False},
        {"text": "내일 우선순위 3가지 계획", "done": False},
    ]
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {"completion_count": 0, "todos": data}
                return data
        except Exception:
            return DEFAULT_DATA
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 3. 세션 상태 초기화
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

if "app_data" not in st.session_state:
    st.session_state.app_data = load_data()

def toggle_todo(index, key_name):
    st.session_state.app_data["todos"][index]["done"] = st.session_state[key_name]
    save_data(st.session_state.app_data)

# 4. 모바일 1줄 고정 & 한 화면 밀착 최적화 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* 본문 상하 여백 압축 */
    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 1.0rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        max-width: 440px !important;
    }

    /* 메인 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 12px 10px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    /* 타이틀 */
    .modern-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        white-space: nowrap !important;
    }

    /* 목표 달성 누적 배지 */
    .count-badge {
        display: inline-flex;
        align-items: center;
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #dbeafe;
        font-size: 0.80rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
        white-space: nowrap !important;
    }

    /* 프로그레스 바 */
    .stProgress {
        margin-top: 2px !important;
        margin-bottom: 4px !important;
    }
    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 6px !important;
    }

    /* 가로 1줄 고정 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 4px !important;
        width: 100% !important;
        margin-bottom: 0px !important;
    }

    /* 좌측 칸 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 우측 버튼 칸 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        flex: 0 0 34px !important;
        min-width: 34px !important;
        max-width: 34px !important;
    }

    /* 체크박스 정렬 및 밀착 */
    div[data-testid="stCheckbox"] {
        min-height: auto !important;
        margin-bottom: 0 !important;
    }
    div[data-testid="stCheckbox"] label {
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 2px 0 !important;
        margin: 0 !important;
    }
    div[data-testid="stCheckbox"] label p {
        font-size: 0.90rem !important;
        margin: 0 !important;
        line-height: 1.25 !important;
        word-break: keep-all !important;
    }

    /* 연필 ✏️ 버튼 */
    div[data-testid="stPopover"] button {
        background-color: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 0 !important;
        width: 30px !important;
        height: 28px !important;
        min-height: 28px !important;
    }

    /* 상단 초기화 버튼 규격 */
    .header-reset-btn button {
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        color: #475569 !important;
        border-radius: 6px !important;
        padding: 1px 7px !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        height: 26px !important;
        min-height: 26px !important;
        white-space: nowrap !important;
    }

    /* 카운트 관리 팝오버 버튼 */
    .count-manage-btn button {
        background-color: #eff6ff !important;
        border: 1px solid #bfdbfe !important;
        color: #1d4ed8 !important;
        border-radius: 6px !important;
        padding: 0 6px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        height: 24px !important;
        min-height: 24px !important;
        width: auto !important;
    }

    /* 하단 오늘 완료 버튼 */
    .finish-btn-wrap button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border-radius: 8px !important;
        border: none !important;
        height: 38px !important;
        min-height: 38px !important;
        margin-top: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# 5. 메인 카드 렌더링
with st.container(border=True):
    # 상단 1줄: "오늘도 건강해지자!" 제목 + 체크 초기화 버튼
    col_t, col_r = st.columns([0.76, 0.24])
    with col_t:
        st.markdown('<div class="modern-title">✔️ 오늘도 건강해지자!</div>', unsafe_allow_html=True)
    with col_r:
        st.markdown('<div class="header-reset-btn">', unsafe_allow_html=True)
        if st.button("🔄 초기화", key="btn_reset_header"):
            for item in st.session_state.app_data["todos"]:
                item["done"] = False
            save_data(st.session_state.app_data)
            st.session_state.reset_count += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 누적 완료 배지 및 카운트 관리 (낮추기/초기화)
    col_badge, col_cnt_opt = st.columns([0.75, 0.25])
    with col_badge:
        count = st.session_state.app_data.get("completion_count", 0)
        st.markdown(f'<div class="count-badge">🏆 누적 완료: {count} / 100</div>', unsafe_allow_html=True)
    with col_cnt_opt:
        st.markdown('<div class="count-manage-btn">', unsafe_allow_html=True)
        with st.popover("⚙️ 관리"):
            st.caption("누적 횟수 조정")
            # 1회 낮추기 버튼
            if st.button("➖ 1회 낮추기", key="btn_minus_count", use_container_width=True):
                if st.session_state.app_data.get("completion_count", 0) > 0:
                    st.session_state.app_data["completion_count"] -= 1
                    save_data(st.session_state.app_data)
                    st.rerun()
            # 0으로 완전 초기화 버튼
            if st.button("🔄 0으로 리셋", key="btn_reset_count_zero", use_container_width=True):
                st.session_state.app_data["completion_count"] = 0
                save_data(st.session_state.app_data)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 5개 기준 진행률 바
    completed = sum(1 for t in st.session_state.todos if t["done"]) if "todos" in st.session_state.app_data else sum(1 for t in st.session_state.app_data["todos"] if t["done"])
    progress = completed / 5.0
    st.progress(progress, text=f"완료 {completed} / 5개 ({int(progress * 100)}%)")

    # 5개 체크리스트 목록
    for idx, item in enumerate(st.session_state.app_data["todos"]):
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
                    st.session_state.app_data["todos"][idx]["text"] = new_text
                    save_data(st.session_state.app_data)
                    st.rerun()

    # 하단: 오늘 완료 및 자동 초기화 버튼
    st.markdown('<div class="finish-btn-wrap">', unsafe_allow_html=True)
    if st.button("🎉 오늘 할 일 완료!", key="btn_finish_today", use_container_width=True):
        st.session_state.app_data["completion_count"] = st.session_state.app_data.get("completion_count", 0) + 1
        for item in st.session_state.app_data["todos"]:
            item["done"] = False
        save_data(st.session_state.app_data)
        st.session_state.reset_count += 1
        st.balloons()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
