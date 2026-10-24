import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="중2 수학 | 도형의 닮음 퀴즈",
    page_icon="📐",
    layout="centered"
)

# 문제 데이터베이스 (PDF 대단원 평가 14문항 기반)
QUESTIONS = [
    {
        "id": 1,
        "type": "choice",
        "category": "항상 닮은 도형",
        "question": "다음 중에서 항상 서로 닮음인 도형은?",
        "options": ["① 두 삼각형", "② 두 원기둥", "③ 두 직사각형", "④ 두 삼각뿔", "⑤ 두 정오각형"],
        "answer": "⑤ 두 정오각형",
        "explanation": "변의 개수가 같은 정다각형(정오각형 등)이나 모든 원, 구, 정다면체는 항상 서로 닮은 도형입니다."
    },
    {
        "id": 2,
        "type": "choice",
        "category": "삼각형의 닮음조건",
        "question": "△ABC ∽ △DEF 가 되기 위해 만족해야 하는 올바른 조건은?\n(단, 대응점 순서는 A-D, B-E, C-F)",
        "options": [
            "① ∠C = 45°, ∠D = 75° (두 각이 같아져 AA 닮음)",
            "② ∠C = 55°, ∠E = 80°",
            "③ AB = 6 cm, DE = 8 cm",
            "④ AC = 12 cm, DF = 16 cm",
            "⑤ AB = 12 cm, DF = 15 cm"
        ],
        "answer": "① ∠C = 45°, ∠D = 75° (두 각이 같아져 AA 닮음)",
        "explanation": "삼각형의 내각의 합은 180°이므로, 대응하는 두 쌍의 각의 크기가 같아지면 AA 닮음이 성립합니다."
    },
    {
        "id": 3,
        "type": "choice",
        "category": "닮은 삼각형 찾기",
        "question": "직각삼각형 조건에서 세 수선 관계가 주어졌을 때, 다음 중 △ABC와 닮음이 아닌 삼각형은?",
        "options": ["① △DBE", "② △DEA", "③ △EAC", "④ △EBA", "⑤ △FBD"],
        "answer": "⑤ △FBD",
        "explanation": "공통각과 직각(90°) 관계를 이용해 AA 닮음을 따져보면, △FBD는 각의 조건이 일치하지 않아 닮음이 아닙니다."
    },
    {
        "id": 4,
        "type": "choice",
        "category": "평행선과 선분의 비",
        "question": "△ADE에서 BC // DE이다. AB = 3 cm, BD = x cm, BC = 4 cm, DE = 7 cm일 때, x의 값은?",
        "options": ["① 2", "② 9/4", "③ 15/4", "④ 9/2", "⑤ 14/3"],
        "answer": "② 9/4",
        "explanation": "AB : AD = BC : DE 이므로 3 : (3 + x) = 4 : 7 입니다.\n4(3 + x) = 21  ==>  12 + 4x = 21  ==>  4x = 9  ==>  x = 9/4"
    },
    {
        "id": 5,
        "type": "choice",
        "category": "평행선과 선분의 길이",
        "question": "△ABC에서 BC // DE이고, B-Q-C 선분 위 BQ=5 cm, QC=10 cm이다. PE=6 cm일 때, DP의 길이는?",
        "options": ["① 2 cm", "② 3 cm", "③ 4 cm", "④ 5 cm", "⑤ 6 cm"],
        "answer": "② 3 cm",
        "explanation": "평행선 사이의 선분 비에 의해 DP : PE = BQ : QC 가 성립합니다.\nDP : 6 = 5 : 10 = 1 : 2  ==>  DP = 3 cm"
    },
    {
        "id": 6,
        "type": "choice",
        "category": "평행사변형과 닮음",
        "question": "평행사변형 ABCD에서 AB = 4 cm이고, 변 BC 위의 점 E에 대해 BE : EC = 3 : 2이다. 이때 선분 CF의 길이는?",
        "options": ["① 1 cm", "② 2 cm", "③ 8/3 cm", "④ 3 cm", "⑤ 14/3 cm"],
        "answer": "③ 8/3 cm",
        "explanation": "△ABE ∽ △FCE (AA 닮음)이므로 AB : FC = BE : CE 가 성립합니다.\n4 : CF = 3 : 2  ==>  3 * CF = 8  ==>  CF = 8/3 cm"
    },
    {
        "id": 7,
        "type": "choice",
        "category": "무게중심과 중점연결",
        "question": "점 G가 △ABC의 무게중심이고, 중선 및 중점 연결선과의 교점을 P라 할 때, AP / PG 의 값은?",
        "options": ["① 1", "② 3/2", "③ 5/2", "④ 3", "⑤ 4"],
        "answer": "④ 3",
        "explanation": "중점연결정리에 의해 AP = 3등분 단위 중 3에 해당하며, PG = 1에 해당하므로 AP : PG = 3 : 1 입니다. 따라서 AP/PG = 3 입니다."
    },
    {
        "id": 8,
        "type": "choice",
        "category": "중점연결정리와 둘레",
        "question": "점 D, E, F가 각각 △ABC의 변 AB, BC, CA의 중점이다. △ABC의 둘레가 32 cm일 때, △DEF의 둘레는?",
        "options": ["① 12 cm", "② 16 cm", "③ 24 cm", "④ 32 cm", "⑤ 64 cm"],
        "answer": "② 16 cm",
        "explanation": "삼각형의 중점연결정리에 의해 △DEF의 각 변의 길이는 △ABC 각 변의 길이의 1/2입니다.\n따라서 둘레도 32 * (1/2) = 16 cm입니다."
    },
    {
        "id": 9,
        "type": "choice",
        "category": "직각삼각형의 닮음 응용",
        "question": "AB ⊥ BC, DC ⊥ BC, PH ⊥ BC이고 AB = 8 cm, CD = 12 cm일 때, 선분 PH의 길이는?",
        "options": ["① 3.2 cm", "② 4.8 cm", "③ 5.9 cm", "④ 6.1 cm", "⑤ 7.2 cm"],
        "answer": "② 4.8 cm",
        "explanation": "1/PH = 1/AB + 1/CD 공식에 의해,\n1/PH = 1/8 + 1/12 = 5/24  ==>  PH = 24/5 = 4.8 cm입니다."
    },
    {
        "id": 10,
        "type": "text",
        "category": "삼각형의 닮음과 변의 길이",
        "question": "△ABC의 변 AC 위의 점 D, 변 BC 위의 점 E에 대해 ∠BAC = ∠DEC이다.\nAB = 9 cm, DE = 5 cm, BC = 12 cm일 때, 선분 DC의 길이는? (숫자 또는 분수만 입력)",
        "answer": "20/3",
        "alt_answers": ["6.67", "6.6", "20/3"],
        "explanation": "∠C 공통, ∠BAC = ∠DEC이므로 △ABC ∽ △EDC (AA 닮음)입니다.\nAB : ED = BC : DC  ==>  9 : 5 = 12 : DC  ==>  9 * DC = 60  ==>  DC = 60/9 = 20/3 cm"
    },
    {
        "id": 11,
        "type": "text",
        "category": "닮음의 실생활 활용",
        "question": "강 건너편의 폭 PQ를 구하기 위해 측량하였다.\n강폭 PQ ⊥ QB, AB ⊥ QB이고, Q-C-B 일직선상에서 QC = 40 m, CB = 10 m, AB = 5 m일 때, PQ의 길이는 몇 m인가?",
        "answer": "20",
        "alt_answers": ["20m", "20"],
        "explanation": "△PQC ∽ △ABC (AA 닮음)이므로 PQ : AB = QC : BC 입니다.\nPQ : 5 = 40 : 10 = 4 : 1  ==>  PQ = 20 m"
    },
    {
        "id": 12,
        "type": "text",
        "category": "무게중심과 사각형의 넓이",
        "question": "점 E, F가 변 AB, AC의 중점이고 G가 무게중심이다. △ABC의 전체 넓이가 36 cm²일 때, 사각형 AEGF의 넓이는 몇 cm²인가?",
        "answer": "12",
        "alt_answers": ["12", "12cm2"],
        "explanation": "무게중심 G와 세 꼭짓점을 이으면 전체 넓이가 6개(각 6 cm²)로 나누어집니다.\n사각형 AEGF = △AGE + △AGF = 6 + 6 = 12 cm²입니다."
    },
    {
        "id": 13,
        "type": "text",
        "category": "평행선과 삼각형 넓이의 비",
        "question": "AC // DE이고 BE = 6 cm, EC = 4 cm이다. △DBE의 넓이가 18 cm²일 때, 사각형 ADEC의 넓이는 몇 cm²인가?",
        "answer": "32",
        "alt_answers": ["32", "32cm2"],
        "explanation": "△DBE ∽ △ABC에서 닮음비는 BE : BC = 6 : 10 = 3 : 5 입니다.\n넓이의 비는 3² : 5² = 9 : 25이므로, △ABC의 넓이는 18 * (25/9) = 50 cm²입니다.\n따라서 사각형 ADEC = △ABC - △DBE = 50 - 18 = 32 cm²입니다."
    },
    {
        "id": 14,
        "type": "text",
        "category": "입체도형 부피의 비",
        "question": "원뿔 모양의 그릇에 20 cm³의 물을 부었더니 그릇 높이의 1/3만큼 채워졌다.\n이 그릇에 물을 가득 채우기 위해 '더 넣어야 할' 물의 양은 몇 cm³인가?",
        "answer": "520",
        "alt_answers": ["520", "520cm3"],
        "explanation": "채워진 물과 전체 원뿔의 닮음비는 1 : 3입니다.\n부피의 비는 1³ : 3³ = 1 : 27이므로, 전체 부피는 20 * 27 = 540 cm³입니다.\n더 넣어야 할 물의 양 = 전체 부피 - 현재 물의 양 = 540 - 20 = 520 cm³입니다."
    }
]

# 세션 상태 초기화
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(QUESTIONS)
    st.session_state.submitted = False
    st.session_state.user_answer = None

def pick_next_question():
    st.session_state.current_q = random.choice(QUESTIONS)
    st.session_state.submitted = False
    st.session_state.user_answer = None

# 상단 헤더
st.title("📐 중2 수학: 도형의 닮음 마스터")
st.caption("대단원 핵심 개념 및 기출 문제 랜덤 퀴즈 훈련 프로그램")
st.divider()

# 새 문제 뽑기 버튼
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    st.markdown(f"**[유형] {st.session_state.current_q['category']}** (문제 #{st.session_state.current_q['id']})")
with col_top2:
    if st.button("🎲 다른 문제 뽑기", use_container_width=True):
        pick_next_question()
        st.rerun()

q = st.session_state.current_q

# 문제 지문 출력
st.subheader("Q. " + q["question"])

# 입력 폼
with st.form("quiz_form"):
    if q["type"] == "choice":
        user_input = st.radio("정답을 선택하세요:", q["options"], index=None)
    else:
        user_input = st.text_input("정답을 입력하세요 (예: 숫자 또는 분수 형태):")

    submit_btn = st.form_submit_button("정답 확인하기")
    if submit_btn:
        st.session_state.submitted = True
        st.session_state.user_answer = user_input

# 채점 및 풀이 결과 표시
if st.session_state.submitted:
    ans = str(st.session_state.user_answer).strip() if st.session_state.user_answer else ""
    correct_ans = q["answer"]

    is_correct = False
    if q["type"] == "choice":
        is_correct = (ans == correct_ans)
    else:
        valid_answers = [a.replace(" ", "").lower() for a in q.get("alt_answers", [correct_ans])]
        is_correct = (ans.replace(" ", "").lower() in valid_answers)

    st.markdown("---")
    if is_correct:
        st.success("🎉 **정답입니다! 완벽하게 이해하고 있네요.**")
    else:
        st.error(f"❌ **아쉽네요! 다시 확인해 보세요.**\n\n* **정답:** `{correct_ans}`")

    with st.expander("📖 친절한 해설 확인하기", expanded=True):
        st.write(q["explanation"])
