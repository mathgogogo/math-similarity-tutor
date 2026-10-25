import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 할 일",
    page_icon="✔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 세션 상태 관리 (리셋 카운터 도입으로 체크박스 먹통 버그 원천 해결)
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

# 3. 모던 & 미니멀 스타일 (상단 적정 여백 확보)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 차분하고 모던한 오프화이트 톤 배경 */
    .stApp {
        background-color: #f8fafc;
    }

    /* 상단 여백을 쾌적하게 확보 (3.5rem) */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 600px !important;
    }

    /* 모던 슬레이트 카드 컨테이너 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 20px !important;
        padding: 24px 26px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
    }

    /* 모던 타이틀 */
    .modern-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* 세련된 딥 인디고 프로그레스 바 */
    .stProgress > div > div > div > div {
        background-color: #3b82f6 !important;
        border-radius: 10px !important;
    }

    /* 행 레이아웃 정렬 */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
        margin-bottom: -4px;
        padding: 2px 0;
    }

    /* 수정 팝오버 버튼 모던 디자인 */
    button[kind="secondary"] {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #e2e8f0 !important;
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. 카드 렌더링
with st.container(border=True):
    # 타이틀
    st.markdown('<div class="modern-title">✔️ 오늘의 할 일</div>', unsafe_allow_html=True)

    # 진행률 게이지 계산
    completed = sum(1 for t in st.session_state.todos if t["done"])
    progress = completed / 10.0
    st.progress(progress, text=f"완료 {completed} / 10개 ({int(progress * 100)}%)")
    st.write("")

    # 10개 체크리스트 목록
    for idx, item in enumerate(st.session_state.todos):
        c_chk, c_txt, c_pop = st.columns([0.08, 0.77, 0.15])
        
        with c_chk:
            # reset_count를 key에 결합하여 초기화 시 체크박스 렌더링을 완전히 초기화함
            chk_key = f"chk_{st.session_state.reset_count}_{idx}"
            checked = st.checkbox("", value=item["done"], key=chk_key, label_visibility="collapsed")
            st.session_state.todos[idx]["done"] = checked

        with c_txt:
            if item["done"]:
                # 완료 시 차분한 슬레이트 그레이 취소선
                st.markdown(f"<span style='color:#94a3b8; text-decoration:line-through; font-size:0.95rem;'>{idx+1}. {item['text']}</span>", unsafe_allow_html=True)
            else:
                # 미완료 시 또렷한 다크 네이비
                st.markdown(f"<span style='color:#1e293b; font-weight:500; font-size:0.95rem;'>{idx+1}. {item['text']}</span>", unsafe_allow_html=True)

        with c_pop:
            with st.popover("수정"):
                new_text = st.text_input(f"{idx+1}번 내용", value=item["text"], key=f"edit_input_{idx}")
                if st.button("저장", key=f"btn_save_{idx}", use_container_width=True):
                    st.session_state.todos[idx]["text"] = new_text
                    st.rerun()

    st.write("")
    
    # 체크 표시 전체 초기화 버튼 (정상 작동 보장)
    if st.button("🔄 체크 표시 전체 초기화", use_container_width=True):
        for item in st.session_state.todos:
            item["done"] = False
        st.session_state.reset_count += 1  # 위젯 키를 새 번호로 갱신하여 체크 강제 해제
        st.rerun()
