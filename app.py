import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="닮음 시각화 훈련소", layout="wide")

st.title("🧩 닮음 정복 훈련: '분리해서 같은 방향으로 돌리기'")
st.markdown("""
많은 학생들이 겹쳐 있거나 회전된 그림을 눈으로만 보려다 실수를 합니다.  
가장 확실한 해결책은 **작은 삼각형을 바깥에 꺼내 큰 삼각형과 똑같은 방향으로 돌려놓는 것**입니다!
""")

# 훈련 유형 선택
problem = st.sidebar.radio(
    "도형 유형을 고르세요:",
    [
        "1. 회전형 AA 닮음 (공통각 + 한 각 동일)",
        "2. 직각삼각형 속 직각 (소 공식 체인)",
        "3. 맞꼭지각 모래시계형 (나비형)"
    ]
)

# -----------------------------------------------------------------------------
# 유형 1: 회전형 AA 닮음
# -----------------------------------------------------------------------------
if problem == "1. 회전형 AA 닮음 (공통각 + 한 각 동일)":
    st.subheader("유형 1: 큰 삼각형 안에 엇갈려 들어간 작은 삼각형")
    st.info("💡 **각 A는 공통각(★)**이고, **각 C와 크기가 같은 각(●)은 각 D**입니다. 작은 삼각형을 큰 삼각형 모양(★가 위, ●가 오른쪽 아래)으로 정렬해 보세요.")
    
    col_orig, col_sep = st.columns([1, 1.2])
    
    with col_orig:
        st.markdown("#### [원본 문제 도형]")
        fig, ax = plt.subplots(figsize=(5, 4.5))
        
        # 큰 삼각형 ABC 좌표
        A = np.array([2.5, 5.0])
        B = np.array([0.0, 0.0])
        C = np.array([7.0, 0.0])
        
        # 선분 AB 위 D, 선분 AC 위 E
        D = A * 0.45 + B * 0.55
        E = A * 0.55 + C * 0.45
        
        # 도형 선 그리기
        ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'b-', lw=2.5)
        ax.plot([D[0], E[0]], [D[1], E[1]], 'crimson', lw=2.5)
        
        # 꼭짓점 라벨 (폰트 깨짐 방지를 위해 기호와 알파벳만 사용)
        ax.text(A[0], A[1] + 0.25, 'A (★)', fontsize=12, ha='center', weight='bold')
        ax.text(B[0] - 0.4, B[1] - 0.2, 'B', fontsize=12, weight='bold')
        ax.text(C[0] + 0.2, C[1] - 0.2, 'C (●)', fontsize=12, color='blue', weight='bold')
        ax.text(D[0] - 0.45, D[1] + 0.1, 'D (●)', fontsize=12, color='crimson', weight='bold')
        ax.text(E[0] + 0.2, E[1] + 0.1, 'E', fontsize=12, color='crimson', weight='bold')
        
        # 변의 길이
        ax.text(1.0, 3.2, 'AD = 4', color='gray', fontsize=10)
        ax.text(0.3, 1.0, 'DB = 5', color='gray', fontsize=10)
        ax.text(4.5, 3.2, 'AE = 3', color='gray', fontsize=10)
        ax.text(5.5, 1.0, 'EC = x', color='crimson', fontsize=11, weight='bold')
        
        ax.set_xlim(-1, 8)
        ax.set_ylim(-1, 6)
        ax.axis('off')
        st.pyplot(fig)

    with col_sep:
        st.markdown("#### [오른쪽 여백에 분리해서 같은 방향으로 세우기]")
        
        align_mode = st.radio(
            "작은 삼각형의 배치 방식을 선택하세요:",
            [
                "그대로 꺼내기 (A 위, D 왼쪽, E 오른쪽)",
                "뒤집어서 같은 방향 맞추기 (A 위, E 왼쪽, D 오른쪽)"
            ]
        )
        
        fig2, (ax_L, ax_R) = plt.subplots(1, 2, figsize=(7, 3.5))
        
        # 기준 큰 삼각형 ABC
        ax_L.plot([2, 0, 6, 2], [4, 0, 0, 4], 'b-', lw=2.5)
        ax_L.text(2, 4.3, 'A (★)', ha='center', weight='bold')
        ax_L.text(-0.3, -0.3, 'B')
        ax_L.text(6.2, -0.3, 'C (●)', color='blue', weight='bold')
        ax_L.text(0.5, 2.0, 'AB = 9')
        ax_L.text(4.2, 2.0, 'AC = 3+x')
        ax_L.set_title("Base: △ABC", fontsize=11, weight='bold')
        ax_L.set_xlim(-1, 7)
        ax_L.set_ylim(-1, 5)
        ax_L.axis('off')
        
        # 오른쪽 작은 삼각형
        if align_mode == "그대로 꺼내기 (A 위, D 왼쪽, E 오른쪽)":
            ax_R.plot([1.5, 0, 4, 1.5], [3, 0, 0, 3], 'gray', lw=2, linestyle='--')
            ax_R.text(1.5, 3.3, 'A (★)', ha='center', weight='bold')
            ax_R.text(-0.3, -0.3, 'D (●)', color='crimson', weight='bold')
            ax_R.text(4.2, -0.3, 'E')
            ax_R.text(0.3, 1.5, 'AD = 4')
            ax_R.text(3.0, 1.5, 'AE = 3')
            ax_R.set_title("Result: Not Aligned", fontsize=11, color='red', weight='bold')
        else:
            ax_R.plot([1.5, 0, 4, 1.5], [3, 0, 0, 3], 'crimson', lw=2.5)
            ax_R.text(1.5, 3.3, 'A (★)', ha='center', weight='bold')
            ax_R.text(-0.3, -0.3, 'E')
            ax_R.text(4.2, -0.3, 'D (●)', color='crimson', weight='bold')
            ax_R.text(0.3, 1.5, 'AE = 3')
            ax_R.text(3.0, 1.5, 'AD = 4')
            ax_R.set_title("Result: Aligned (△AED)", fontsize=11, color='green', weight='bold')
            
        ax_R.set_xlim(-1, 5)
        ax_R.set_ylim(-1, 4.5)
        ax_R.axis('off')
        st.pyplot(fig2)
        
        # 상태에 따른 한글 설명 (Streamlit 텍스트로 처리하여 절대 안 깨짐)
        if align_mode == "그대로 꺼내기 (A 위, D 왼쪽, E 오른쪽)":
            st.error("❌ 아직 회전이 맞지 않습니다: 기준 삼각형은 ●가 오른쪽인데, 작은 삼각형은 ●가 왼쪽에 있습니다.")
        else:
            st.success("🎯 완벽한 정렬! 기준 도형과 작은 도형의 ★(위), ●(오른쪽 아래) 위치가 완전히 일치합니다.")
            st.markdown(r"""
            **대응점 순서 확정:** $\triangle \text{ABC} \sim \triangle \text{AED}$ (AA 닮음)  
            
            **대응변 비례식 세우기:**
            $$\frac{\text{AB}}{\text{AE}} = \frac{\text{AC}}{\text{AD}} \implies \frac{9}{3} = \frac{3+x}{4}$$
            $$3 = \frac{3+x}{4} \implies 12 = 3+x \implies \mathbf{x = 9}$$
            """)

# -----------------------------------------------------------------------------
# 유형 2: 직각삼각형 속 직각
# -----------------------------------------------------------------------------
elif problem == "2. 직각삼각형 속 직각 (소 공식 체인)":
    st.subheader("유형 2: 직각삼각형 꼭짓점에서 내린 수선의 발 (소 공식)")
    st.info("💡 직각($90^\circ$)과 한 예각(●)을 기준으로, 3개의 직각삼각형을 모두 같은 모양(직각이 왼쪽 아래, ●가 오른쪽 아래)으로 정렬합니다.")
    
    col_orig, col_sep = st.columns([1, 1.2])
    
    with col_orig:
        fig, ax = plt.subplots(figsize=(5, 4))
        A = np.array([0, 2.4])
        B = np.array([-3.2, 0])
        C = np.array([1.8, 0])
        H = np.array([0, 0])
        
        ax.plot([B[0], C[0], A[0], B[0]], [B[1], C[1], A[1], B[1]], 'b-', lw=2.5)
        ax.plot([A[0], H[0]], [A[1], H[1]], 'crimson', lw=2)
        
        ax.text(A[0], A[1] + 0.2, 'A (90°)', ha='center', weight='bold')
        ax.text(B[0] - 0.4, B[1] - 0.2, 'B (×)', weight='bold')
        ax.text(C[0] + 0.2, C[1] - 0.2, 'C (●)', weight='bold')
        ax.text(H[0], H[1] - 0.35, 'H (90°)', ha='center', color='crimson', weight='bold')
        
        ax.set_xlim(-4, 3)
        ax.set_ylim(-1, 3.5)
        ax.axis('off')
        st.pyplot(fig)
        
    with col_sep:
        st.markdown("#### [세 직각삼각형을 모두 같은 자세로 분리]")
        show_all = st.checkbox("3개의 직각삼각형 분리해서 보기", value=True)
        
        if show_all:
            fig3, axes = plt.subplots(1, 3, figsize=(8, 2.5))
            
            # 1. 전체 큰 삼각형
            axes[0].plot([0, 4, 0, 0], [0, 0, 3, 0], 'b-', lw=2)
            axes[0].text(-0.3, -0.4, 'A (90°)', weight='bold')
            axes[0].text(4.0, -0.4, 'C (●)', weight='bold')
            axes[0].text(-0.3, 3.1, 'B (×)', weight='bold')
            axes[0].set_title("1. △ABC (Whole)", fontsize=10)
            axes[0].axis('off')
            
            # 2. 오른쪽 작은 삼각형
            axes[1].plot([0, 3, 0, 0], [0, 0, 2.25, 0], 'crimson', lw=2)
            axes[1].text(-0.3, -0.4, 'H (90°)', weight='bold')
            axes[1].text(3.0, -0.4, 'C (●)', weight='bold')
            axes[1].text(-0.3, 2.35, 'A (×)', weight='bold')
            axes[1].set_title("2. △HAC (Right)", fontsize=10, color='crimson')
            axes[1].axis('
