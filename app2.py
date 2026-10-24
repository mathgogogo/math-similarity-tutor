import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="닮음 시각화 훈련소", layout="wide")

# 한글 폰트 설정 (환경에 따라 기본 영문/심볼 병기)
plt.rcParams['axes.unicode_minus'] = False

st.title("🧩 닮음 정복 훈련: '분리해서 같은 방향으로 돌리기'")
st.markdown("""
많은 학생들이 겹쳐 있거나 회전된 그림을 눈으로만 보려다 실수를 합니다.  
가장 확실한 해결책은 **작은 삼각형을 바깥에 꺼내 큰 삼각형과 똑같은 방향으로 돌려놓는 것**입니다!
""")

# 연습할 대표 유형 3가지
st.sidebar.header("🎯 훈련 유형 선택")
problem = st.sidebar.radio(
    "도형 유형을 고르세요:",
    [
        "1. 회전형 AA 닮음 (공통각 + 한 각 동일)",
        "2. 직각삼각형 속 직각 (소 공식 체인)",
        "3. 맞꼭지각 모래시계형 (나비형)"
    ]
)

# -----------------------------------------------------------------------------
# 유형 1: 회전형 AA 닮음 (A 공통, 각 C = 각 ADE)
# -----------------------------------------------------------------------------
if problem == "1. 회전형 AA 닮음 (공통각 + 한 각 동일)":
    st.subheader("유형 1: 큰 삼각형 안에 엇갈려 들어간 작은 삼각형")
    st.info("💡 각 A는 공통각이고, 각 C와 크기가 같은 각(●)은 각 D입니다. 작은 삼각형을 큰 삼각형 모양(공통각이 위, ●가 오른쪽 아래)으로 정렬해 보세요.")
    
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
        
        # 그리기
        ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'b-', lw=2.5)
        ax.plot([D[0], E[0]], [D[1], E[1]], 'crimson', lw=2.5)
        
        # 점 라벨 및 각 표시
        ax.text(A[0], A[1] + 0.25, 'A (공통각 ★)', fontsize=12, ha='center', weight='bold')
        ax.text(B[0] - 0.4, B[1] - 0.2, 'B', fontsize=12, weight='bold')
        ax.text(C[0] + 0.2, C[1] - 0.2, 'C (●)', fontsize=12, color='blue', weight='bold')
        ax.text(D[0] - 0.45, D[1] + 0.1, 'D (●)', fontsize=12, color='crimson', weight='bold')
        ax.text(E[0] + 0.2, E[1] + 0.1, 'E', fontsize=12, color='crimson', weight='bold')
        
        # 변의 길이 정보
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
            "작은 삼각형의 각 꼭짓점 배치 선택:",
            [
                "그대로 꺼내기 (A 위, D 왼쪽, E 오른쪽)",
                "뒤집어서 같은 방향 맞추기 (A 위, E 왼쪽, D 오른쪽)"
            ]
        )
        
        fig2, (ax_L, ax_R) = plt.subplots(1, 2, figsize=(7, 3.5))
        
        # 왼쪽: 기준 큰 삼각형 ABC
        ax_L.plot([2, 0, 6, 2], [4, 0, 0, 4], 'b-', lw=2.5)
        ax_L.text(2, 4.3, 'A (★)', ha='center', weight='bold')
        ax_L.text(-0.3, -0.3, 'B')
        ax_L.text(6.2, -0.3, 'C (●)', color='blue', weight='bold')
        ax_L.text(0.5, 2.0, 'AB = 9')
        ax_L.text(4.2, 2.0, 'AC = 3+x')
        ax_L.set_title("기준: △ABC\n(★ 위, ● 오른쪽)", fontsize=11)
        ax_L.set_xlim(-1, 7)
        ax_L.set_ylim(-1, 5)
        ax_L.axis('off')
        
        # 오른쪽: 작은 삼각형
        if align_mode == "그대로 꺼내기 (A 위, D 왼쪽, E 오른쪽)":
            ax_R.plot([1.5, 0, 4, 1.5], [3, 0, 0, 3], 'gray', lw=2, linestyle='--')
            ax_R.text(1.5, 3.3, 'A (★)', ha='center', weight='bold')
            ax_R.text(-0.3, -0.3, 'D (●)', color='crimson', weight='bold')
            ax_R.text(4.2, -0.3, 'E')
            ax_R.text(0.3, 1.5, 'AD = 4')
            ax_R.text(3.0, 1.5, 'AE = 3')
            ax_R.set_title("❌ 아직 뒤집힌 상태\n(●의 위치가 서로 다름)", fontsize=11, color='red')
        else:
            ax_R.plot([1.5, 0, 4, 1.5], [3, 0, 0, 3], 'crimson', lw=2.5)
            ax_R.text(1.5, 3.3, 'A (★)', ha='center', weight='bold')
            ax_R.text(-0.3, -0.3, 'E')
            ax_R.text(4.2, -0.3, 'D (●)', color='crimson', weight='bold')
            ax_R.text(0.3, 1.5, 'AE = 3')
            ax_R.text(3.0, 1.5, 'AD = 4')
            ax_R.set_title("⭕ 완벽한 방향 정렬!\n(★ 위, ● 오른쪽 일치)", fontsize=11, color='green')
            
        ax_R.set_xlim(-1, 5)
        ax_R.set_ylim(-1, 4.5)
        ax_R.axis('off')
        st.pyplot(fig2)
        
        if align_mode == "뒤집어서 같은 방향 맞추기 (A 위, E 왼쪽, D 오른쪽)":
            st.success("대응점 순서가 완벽히 맞춰졌습니다: △ABC ∽ △AED")
            st.latex(r"\frac{\text{AB (왼쪽)}}{\text{AE (왼쪽)}} = \frac{\text{AC (오른쪽)}}{\text{AD (오른쪽)}} \implies \frac{9}{3} = \frac{3+x}{4} \implies x = 9")

# -----------------------------------------------------------------------------
# 유형 2: 직각삼각형 속 직각
# -----------------------------------------------------------------------------
elif problem == "2. 직각삼각형 속 직각 (소 공식 체인)":
    st.subheader("유형 2: 직각삼각형 꼭짓점에서 내린 수선의 발 (소 공식)")
    st.info("💡 직각(90°)과 예각 하나(●)를 기준으로, 큰 직각삼각형과 내부의 작은 직각삼각형 두 개를 모두 같은 자세(직각이 왼쪽 아래, ●가 오른쪽 아래)로 눕혀 분리해 봅니다.")
    
    col_orig, col_sep = st.columns([1, 1.2])
    
    with col_orig:
        fig, ax = plt.subplots(figsize=(5, 4))
        # 직각삼각형: 각 A = 90도, BC가 빗변
        # A=(0, 2.4), B=(-3.2, 0), C=(1.8, 0) -> AB=4, AC=3, BC=5
        A = np.array([0, 2.4])
        B = np.array([-3.2, 0])
        C = np.array([1.8, 0])
        H = np.array([0, 0]) # 수선의 발
        
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
        st.markdown("#### [세 직각삼각형을 모두 같은 모양(자세)으로 분리]")
        show_all = st.checkbox("3개의 직각삼각형 나란히 정렬하기", value=True)
        
        if show_all:
            fig3, axes = plt.subplots(1, 3, figsize=(8, 2.5))
            
            # 모양 규격: 직각(L자)이 왼쪽 아래, ●(각 C)가 오른쪽 아래, 나머지(×)가 위쪽
            # 1. 전체 큰 삼각형 (직각: A, 아래각: C(●), 윗각: B(×))
            axes[0].plot([0, 4, 0, 0], [0, 0, 3, 0], 'b-', lw=2)
            axes[0].text(-0.3, -0.4, 'A(90°)', weight='bold')
            axes[0].text(4.0, -0.4, 'C(●)', weight='bold')
            axes[0].text(-0.3, 3.1, 'B(×)', weight='bold')
            axes[0].set_title("① 전체 △ABC\n(기호: △CBA)", fontsize=10)
            axes[0].axis('off')
            
            # 2. 오른쪽 작은 삼각형 (직각: H, 아래각: C(●), 윗각: A(×))
            axes[1].plot([0, 3, 0, 0], [0, 0, 2.25, 0], 'crimson', lw=2)
            axes[1].text(-0.3, -0.4, 'H(90°)', weight='bold')
            axes[1].text(3.0, -0.4, 'C(●)', weight='bold')
            axes[1].text(-0.3, 2.35, 'A(×)', weight='bold')
            axes[1].set_title("② 오른쪽 △HAC\n(기호: △CHA)", fontsize=10, color='crimson')
            axes[1].axis('off')

            # 3. 왼쪽 중간 삼각형 (직각: H, 아래각: A(●), 윗각: B(×))
            axes[2].plot([0, 2.25, 0, 0], [0, 0, 1.7, 0], 'darkgreen', lw=2)
            axes[2].text(-0.3, -0.4, 'H(90°)', weight='bold')
            axes[2].text(2.25, -0.4, 'A(●)', weight='bold')
            axes[2].text(-0.3, 1.8, 'B(×)', weight='bold')
            axes[2].set_title("③ 왼쪽 △HBA\n(기호: △AHB)", fontsize=10, color='darkgreen')
            axes[2].axis('off')
            
            st.pyplot(fig3)
            st.success("✨ 같은 자세로 놓으면 공식($\text{AC}^2 = \text{CH} \times \text{CB}$, $\text{AH}^2 = \text{BH} \times \text{CH}$)이 눈으로 그대로 증명됩니다!")

# -----------------------------------------------------------------------------
# 유형 3: 맞꼭지각 모래시계형
# -----------------------------------------------------------------------------
else:
    st.subheader("유형 3: 평행선 사이의 모래시계형 (상하/좌우 반전)")
    st.info("💡 평행선 사이의 엇각에 의해 위쪽 삼각형과 아래쪽 삼각형은 180도 회전된 관계입니다. 아래쪽 삼각형을 180도 돌려 같은 방향으로 세워보세요.")
    
    col_orig, col_sep = st.columns([1, 1.2])
    with col_orig:
        fig, ax = plt.subplots(figsize=(5, 4))
        # AB // CD
        ax.plot([-2, 2.5], [2, 2], 'b-', lw=3)
        ax.plot([-1.5, 3], [-2, -2], 'b-', lw=3)
        ax.plot([-2, 3], [2, -2], 'gray', linestyle='--')
        ax.plot([2.5, -1.5], [2, -2], 'gray', linestyle='--')
        
        ax.text(-2.3, 2.1, 'A (●)', weight='bold')
        ax.text(2.6, 2.1, 'B (×)', weight='bold')
        ax.text(0.1, 0.1, 'O', weight='bold')
        ax.text(3.1, -2.2, 'D (●)', weight='bold', color='crimson')
        ax.text(-1.8, -2.2, 'C (×)', weight='bold', color='crimson')
        ax.axis('off')
        st.pyplot(fig)
        
    with col_sep:
        rotate = st.slider("아래 삼각형(△OCD) 회전시키기 (