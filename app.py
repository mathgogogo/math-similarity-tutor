import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="중2 수학 | 도형의 닮음 퀴즈", page_icon="📐", layout="centered")

# --- 도형 그리기 함수 모음 ---
def draw_fig_parallel_triangle(x_label="x cm", b_len="3 cm", bc_len="4 cm", de_len="7 cm"):
    fig, ax = plt.subplots(figsize=(4, 3))
    A, D, E = [2.5, 4], [0.5, 0.5], [4.5, 0.5]
    r = 0.55
    B = [A[0]*(1-r) + D[0]*r, A[1]*(1-r) + D[1]*r]
    C = [A[0]*(1-r) + E[0]*r, A[1]*(1-r) + E[1]*r]

    ax.plot([A[0], D[0], E[0], A[0]], [A[1], D[1], E[1], A[1]], 'k-', lw=2)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'b-', lw=2)

    ax.text(A[0], A[1]+0.2, 'A', fontsize=12, ha='center', weight='bold')
    ax.text(B[0]-0.25, B[1], 'B', fontsize=12, ha='right', weight='bold')
    ax.text(C[0]+0.25, C[1], 'C', fontsize=12, ha='left', weight='bold')
    ax.text(D[0]-0.2, D[1]-0.25, 'D', fontsize=12, ha='center', weight='bold')
    ax.text(E[0]+0.2, E[1]-0.25, 'E', fontsize=12, ha='center', weight='bold')

    ax.text((A[0]+B[0])/2 - 0.25, (A[1]+B[1])/2, b_len, color='crimson', fontsize=10)
    ax.text((B[0]+D[0])/2 - 0.25, (B[1]+D[1])/2, x_label, color='crimson', fontsize=10)
    ax.text((B[0]+C[0])/2, B[1]+0.15, bc_len, color='blue', fontsize=10, ha='center')
    ax.text((D[0]+E[0])/2, D[1]-0.25, de_len, color='blue', fontsize=10, ha='center')

    ax.set_xlim(-0.2, 5.2)
    ax.set_ylim(0, 4.5)
    ax.axis('off')
    return fig

def draw_fig_right_triangle():
    fig, ax = plt.subplots(figsize=(4.5, 2.5))
    B, C, A, D = [0.5, 0.5], [4.5, 0.5], [0.5, 2.5], [4.5, 3.5]
    # 교점 P
    # AC: y - 0.5 = (2.0/-4.0)(x - 4.5) -> y = -0.5x + 2.75
    # BD: y - 0.5 = (3.0/4.0)(x - 0.5)  -> y = 0.75x + 0.125
    # 1.25x = 2.625 -> x = 2.1, y = 1.7
    P = [2.1, 1.7]
    H = [2.1, 0.5]

    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', lw=2)
    ax.plot([B[0], A[0]], [B[1], A[1]], 'k-', lw=2)
    ax.plot([C[0], D[0]], [C[1], D[1]], 'k-', lw=2)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'gray', lw=1.5, ls='--')
    ax.plot([B[0], D[0]], [B[1], D[1]], 'gray', lw=1.5, ls='--')
    ax.plot([P[0], H[0]], [P[1], H[1]], 'red', lw=2)

    ax.text(A[0]-0.2, A[1], 'A (8cm)', color='crimson', fontsize=10, ha='right', weight='bold')
    ax.text(D[0]+0.2, D[1], 'D (12cm)', color='crimson', fontsize=10, ha='left', weight='bold')
    ax.text(B[0]-0.15, B[1]-0.2, 'B', fontsize=11, weight='bold')
    ax.text(C[0]+0.15, C[1]-0.2, 'C', fontsize=11, weight='bold')
    ax.text(H[0], H[1]-0.25, 'H', fontsize=11, weight='bold')
    ax.text(P[0], P[1]+0.15, 'P', fontsize=11, weight='bold')

    ax.set_xlim(-0.8, 5.8)
    ax.set_ylim(0, 4.0)
    ax.axis('off')
    return fig

# --- 문제 데이터베이스 (그림 함수 연동) ---
QUESTIONS = [
    {
        "id": 4,
        "type": "choice",
        "category": "평행선과 선분의 비",
        "question": "아래 그림에서 BC // DE일 때, x의 값은?",
        "draw_func": draw_fig_parallel_triangle,
        "options": ["① 2", "② 9/4", "③ 15/4", "④ 9/2", "⑤ 14/3"],
        "answer": "② 9/4",
        "explanation": "AB : AD = BC : DE 이므로 3 : (3 + x) = 4 : 7 입니다.\n4(3 + x) = 21  ==>  12 + 4x = 21  ==>  4x = 9  ==>  x = 9/4"
    },
    {
        "id": 9,
        "type": "choice",
        "category": "직각삼각형의 닮음 응용",
        "question": "아래 그림에서 AB ⊥ BC, DC ⊥ BC, PH ⊥ BC일 때, 선분 PH의 길이는?",
        "draw_func": draw_fig_right_triangle,
        "options": ["① 3.2 cm", "② 4.8 cm", "③ 5.9 cm", "④ 6.1 cm", "⑤ 7.2 cm"],
        "answer": "② 4.8 cm",
        "explanation": "1/PH = 1/AB + 1/CD 공식에 의해,\n1/PH = 1/8 + 1/12 = 5/24  ==>  PH = 24/5 = 4.8 cm입니다."
    },
    {
        "id": 1,
        "type": "choice",
        "category": "항상 닮은 도형",
        "question": "다음 중에서 항상 서로 닮음인 도형은?",
        "draw_func": None,
        "options": ["① 두 삼각형", "② 두 원기둥", "③ 두 직사각형", "④ 두 삼각뿔", "⑤ 두 정오각형"],
        "answer": "⑤ 두 정오각형",
        "explanation": "변의 개수가 같은 정다각형(정오각형 등)이나 모든 원, 구, 정다면체는 항상 서로 닮은 도형입니다."
    }
]

# --- 상태 관리 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(QUESTIONS)
    st.session_state.submitted = False
    st.session_state.user_answer = None

def pick_next():
    st.session_state.current_q = random.choice(QUESTIONS)
    st.session_state.submitted = False
    st.session_state.user_answer = None

# --- UI 레이아웃 ---
st.title("📐 중2 수학: 도형의 닮음 퀴즈")
st.caption("그림과 함께 푸는 도형 문제")
st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**[유형] {st.session_state.current_q['category']}**")
with col2:
    if st.button("🎲 다른 문제", use_container_width=True):
        pick_next()
        st.rerun()

q = st.session_state.current_q
st.subheader("Q. " + q["question"])

# 그림이 연결되어 있으면 화면에 출력
if q.get("draw_func"):
    fig = q["draw_func"]()
    st.pyplot(fig)
    plt.close(fig)

with st.form("quiz_form"):
    user_input = st.radio("정답 선택:", q["options"], index=None)
    submit = st.form_submit_button("정답 확인")
    if submit:
        st.session_state.submitted = True
        st.session_state.user_answer = user_input

if st.session_state.submitted:
    st.markdown("---")
    if st.session_state.user_answer == q["answer"]:
        st.success("🎉 **정답입니다!**")
    else:
        st.error(f"❌ **틀렸습니다.** 정답: `{q['answer']}`")
    with st.expander("📖 해설 보기", expanded=True):
        st.write(q["explanation"])
