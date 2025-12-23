# 통합 메인 프로세스

import streamlit as st  # 웹 화면을 만들기 위한 라이브러리 불러오기
from adcopy_main_streamlit import main_adcopy  # 광고 카피 모듈 불러오기
from youtube_main_streamlit import main_ytb  # 유튜브 스크립트 모듈 불러오기
from sns_main_streamlit import main_sns  # SNS 포스팅 모듈 불러오기

# 페이지 전체 너비 사용
st.set_page_config(layout="wide")  # 웹 화면을 넓게 쓰도록 설정

# 사이드바 제목과 메뉴 선택
with st.sidebar :   # 왼쪽 사이드바 영역 설정
    st.title("콘텐츠 에이전트!")  # 사이드바 제목 표시
    menu = st.selectbox("메뉴선택", ["1.광고 카피", "2.유튜브 스크립트", "3.SNS 포스팅"])  # 드롭다운 메뉴 생성

# 선택된 메뉴별 메인 코드 호출
if menu == "1.광고 카피" :     # '광고 카피' 선택 시
    main_adcopy()             # 광고 카피 화면 실행
elif menu == "2.유튜브 스크립트" :  # '유튜브 스크립트' 선택 시
    main_ytb()                    # 유튜브 스크립트 화면 실행
elif menu == "3.SNS 포스팅" :  # 'SNS 포스팅' 선택 시
    main_sns()                # SNS 포스팅 화면 실행   