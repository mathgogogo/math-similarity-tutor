import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 페이지 설정
st.set_page_config(page_title="중2 수학: 닮음 마스터", layout="wide")

st.title("📐 중2 수학: 도형의 닮음 정복 프로젝트")
st.markdown("""
닮음 문제를 풀 때 가장 중요한 것은 **‘대응점 순서를 정확히 맞추어 기호($\triangle \text{ABC} \sim \triangle \text{ADE}$)로 적는 것’**입니다!  
그림을 분리해 같은 방향으로 놓고, 대응점을 찾아 비례식을 완성해 보세요.
""")

# 세션 상태 초기화
if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 1

# 유형 선택
problem_type = st.sidebar.selectbox(
    "유형을 선택하세요",
    ["유형 1: 회전형 AA 닮음 (공통각 + 동위각/한 각 동일)", "유형 2: 모래시계형 (맞꼭지각 + 엇각)"]
)

# -------------------------------------------------------------
# 유형 1: 회전형 AA 닮음
# -------------------------------------------------------------
if problem_type == "유형 1: 회전형 AA 닮음 (공통각 + 동위각/한 각 동일)":
    st.subheader("💡 유형 1: 큰 삼각형 안에 뒤집혀 들어간 삼각형")
    
    col1, col2 = st.columns([1, 1])
    
    # 도형 좌표 정의
    # A=(2, 4), B=(0, 0), C=(6, 0)
    # D는 AB 위 (1, 2), E는 AC 위 (4, 2)
    # 각 ADE = 각 ACB (회전형)
    
    with col1:
        st.markdown("### [문제 그림]")
        fig, ax = plt.subplots(figsize=(5, 4))
        
        # 큰 삼각형 ABC
        A, B, C = np.array([2, 5]), np.array([0, 0]), np.array([7, 0])
        D = A * 0.4 + B * 0.6  # 선분 AB 위
        E = A * 0.5 + C * 0.5  # 선분 AC 위
        
        # 선 그리기
        ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'b-', lw=2)
        ax.plot([D[0], E[0]], [D[1], E[1]], 'r-', lw=2)
        
        # 꼭짓점 텍스트
        ax.text(A[0], A[1]+0.2, 'A (공통각)', fontsize=12, ha='center', weight='bold')
        ax.text(B[0]-0.3, B[1]-0.2, 'B', fontsize=12, color='blue', weight='bold')
        ax.text(C[0]+0.2, C[1]-0.2, 'C (●)', fontsize=12, color='blue', weight='bold')
        ax.text(D[0]-0.3, D[1]+0.1, 'D (●)', fontsize=12, color='red', weight='bold')
        ax.text(E[0]+0.2, E[1]+0.1, 'E', fontsize=12, color='red', weight='bold')
        
        # 변의 길이 예시 표시
        ax.text(1.2, 3.8, 'AD = 4', fontsize=10, color='darkgray')
        ax.text(0.3, 1.2, 'DB = 5', fontsize=10, color='darkgray')
        ax.text(4.8, 3.8, 'AE = 3', fontsize=10, color='darkgray')
        ax.text(6.0, 1.2, 'EC = x', fontsize=10, color='crimson', weight='bold')
        
        ax.set_xlim(-1, 8)
        ax.set_ylim(-1, 6)
        ax.axis('off')
        st.pyplot(fig)

    with col2:
        st.markdown("### 🔍 시각적 힌트: '분리해서 같은 방향으로 보기'")
        show_separated = st.checkbox("삼각형 분리해서 같은 방향으로 돌려보기")
        
        if show_separated:
            fig2, (ax_big, ax_small) = plt.subplots(1, 2, figsize=(6, 3))
            
            # 큰 삼각형 ABC (A 위, B 왼쪽, C 오른쪽)
            ax_big.plot([2, 0, 7, 2], [5, 0, 0, 5], 'b-', lw=2)
            ax_big.text(2, 5.2, 'A (공통)', ha='center', weight='bold')
            ax_big.text(-0.3, -0.3, 'B')
            ax_big.text(7.2, -0.3, 'C (●)', weight='bold')
            ax_big.text(0.5, 2.5, 'AB = 9')
            ax_big.text(5.0, 2.5, 'AC = 3+x')
            ax_big.set_title("△ABC", fontsize=11)
            ax_big.axis('off')
            
            # 작은 삼각형: 대응점 순서대로 (A 위, E 왼쪽, D 오른쪽)
            # 왜냐하면 각 D가 ●이므로 큰 삼각형의 각 C(●)와 대응!
            ax_small.plot([1, 0, 3.5, 1], [3, 0, 0, 3], 'r-', lw=2)
            ax_small.text(1, 3.2, 'A (공통)', ha='center', weight='bold')
            ax_small.text(-0.3, -0.3, 'E')
            ax_small.text(3.7, -0.3, 'D (●)', weight='bold')
            ax_small.text(0.0, 1.5, 'AE = 3')
            ax_small.text(2.6, 1.5, 'AD = 4')
            ax_small.set_title("방향을 맞춘 작은 삼각형", fontsize=11, color='red')
            ax_small.axis('off')
            
            st.pyplot(fig2)
            st.success("✨ 같은 각(공통각 A, ●표시 각)을 같은 위치에 두니 대응 관계가 바로 보이죠?")

    # 인터랙티브 퀴즈
    st.markdown("---")
    st.subheader("📝 대응점 순서 맞추기 퀴즈")
    
    st.write("$\triangle \text{ABC}$ 와 닮음인 삼각형의 기호를 대응점 순서에 맞게 선택하세요.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        p1 = st.selectbox("점 A의 대응점", ["A", "D", "E"], index=0)
    with c2:
        p2 = st.selectbox("점 B의 대응점", ["A", "D", "E"], index=1)
    with c3:
        p3 = st.selectbox("점 C의 대응점", ["A", "D", "E"], index=2)
        
    ans_selected = f"△{p1}{p2}{p3}"
    
    if st.button("정답 확인 및 비례식 세우기"):
        # 점 C(●)에 대응하는 점은 D(●), 점 A는 공통각이므로 A, 나머지 B는 E에 대응 -> △AED
        if p1 == "A" and p2 == "E" and p3 == "D":
            st.success(f"🎉 정답입니다! $\\triangle \\text{{ABC}} \\sim {ans_selected}$ (AA 닮음)")
            st.markdown(r"""
            **대응점 순서대로 비례식을 적으면 실수가 없습니다:**
            $$\frac{\text{AB}}{\text{AE}} = \frac{\text{BC}}{\text{ED}} = \frac{\text{AC}}{\text{AD}}$$
            
            수치를 대입하면:
            $$\frac{4 + 5}{3} = \frac{3 + x}{4} \implies \frac{9}{3} = \frac{3 + x}{4}$$
            $$3 = \frac{3 + x}{4} \implies 12 = 3 + x \implies \mathbf{x = 9}$$
            """)
        else:
            st.error(f"다시 확인해보세요! 선택하신 결과: $\\triangle \\text{{ABC}} \\sim {ans_selected}$")
            st.info("💡 힌트: 각 A는 공통각이고, 표시(●)가 되어 있는 각 C의 대응점은 각 D입니다.")

# -------------------------------------------------------------
# 유형 2: 모래시계형 닮음
# -------------------------------------------------------------
else:
    st.subheader("💡 유형 2: 평행선 사이의 모래시계(나비)형 닮음")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        # AB // CD
        # O는 교점
        A, B = np.array([-2, 3]), np.array([3, 3])
        O = np.array([0, 1])
        # O를 중심으로 연장
        C = O + (O - A) * 0.7
        D = O + (O - B) * 0.7
        
        # 선분 그리기
        ax.plot([A[0], B[0]], [A[1], B[1]], 'b-', lw=3, label="AB // CD")
        ax.plot([D[0], C[0]], [D[1], C[1]], 'b-', lw=3)
        ax.plot([A[0], C[0]], [A[1], C[1]], 'gray', linestyle='--')
        ax.plot([B[0], D[0]], [B[1], D[1]], 'gray', linestyle='--')
        
        ax.text(A[0]-0.3, A[1]+0.1, 'A (●)', fontsize=11, weight='bold')
        ax.text(B[0]+0.1, B[1]+0.1, 'B (×)', fontsize=11, weight='bold')
        ax.text(O[0]+0.2, O[1]+0.1, 'O', fontsize=11, weight='bold')
        ax.text(C[0]-0.3, C[1]-0.3, 'C (●)', fontsize=11, weight='bold')
        ax.text(D[0]+0.1, D[1]-0.3, 'D (×)', fontsize=11, weight='bold')
        
        ax.axis('off')
        st.pyplot(fig)
        
    with col2:
        st.markdown("""
        ### 🔍 핵심 원리: 엇각 찾기
        * $\\text{AB} \parallel \\text{CD}$ 이므로:
          * $\\angle \\text{OAB} = \\angle \\text{OCD}$ (엇각, ●)
          * $\\angle \\text{OBA} = \\angle \\text{ODC}$ (엇각, $\\times$)
          * $\\angle \\text{AOB} = \\angle \\text{COD}$ (맞꼭지각)
        * 따라서 모래시계형은 좌우가 뒤집히는 형태의 대응을 가집니다.
        """)
        
        st.markdown("---")
        st.markdown("#### $\\triangle \\text{OAB}$ 와 닮음인 삼각형은?")
        choice = st.radio("대응 순서가 바른 것을 고르세요:", ["△OCD", "△ODC", "△CDO"])
        
        if st.button("확인"):
            if choice == "△OCD":
                st.success(r"정답입니다! $\triangle \text{OAB} \sim \triangle \text{OCD}$")
                st.latex(r"\frac{\text{OA}}{\text{OC}} = \frac{\text{OB}}{\text{OD}} = \frac{\text{AB}}{\text{CD}}")
            else:
                st.error("오답입니다. 점 A(●)의 대응점은 점 C(●), 점 B(×)의 대응점은 점 D(×)입니다!")
