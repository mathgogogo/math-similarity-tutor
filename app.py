import datetime
import urllib.parse
import requests
import streamlit as st

# 1. 페이지 레이아웃 및 탭 타이틀 설정
st.set_page_config(
    page_title="Google Workspace Dashboard",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 구글 머티리얼 디자인 스타일(CSS) 주입
st.markdown("""
<style>
    /* 구글 웹폰트 & 전체 배경 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Product+Sans:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #f8fafd;
    }

    /* 카드 컨테이너 스타일 */
    .g-card {
        background: #ffffff;
        border: 1px solid #dadce0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(60,64,67, 0.08), 0 4px 8px rgba(60,64,67, 0.04);
        transition: box-shadow 0.2s ease;
    }
    .g-card:hover {
        box-shadow: 0 2px 6px rgba(60,64,67, 0.15), 0 8px 16px rgba(60,64,67, 0.08);
    }

    /* 상단 로고 스타일 */
    .g-title {
        font-family: 'Product Sans', sans-serif;
        font-size: 2.3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    .c-blue { color: #4285F4; }
    .c-red { color: #EA4335; }
    .c-yellow { color: #FBBC05; }
    .c-green { color: #34A853; }

    /* 카드 내 소제목 */
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #202124;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* 프로그레스 바 스타일 */
    .stProgress > div > div > div > div {
        background-color: #4285F4;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 (할 일 5개 초기화)
if "todos" not in st.session_state:
    st.session_state.todos =
