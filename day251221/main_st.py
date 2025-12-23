# 통합 streamlit 처리

import streamlit as st
from adcopy_main_streamlit import main_adcopy
from youtube_main_streamlit import main_ytb
from sns_main_streamlit import main_sns

# 페이지 전체 너비 사용
st.set_page_config(layout="wide")

# 입출력 영역 지정
input_area = st.container()  # 입력창 위치
# output_area = st.container() # 출력창 위치

with st.sidebar :
    st.title("콘텐츠 에이전트!")
    menu = st.selectbox("메뉴 선택", ["1. 광고 카피", "2. 유튜브 스크립트","3. SNS 포스팅" ])
    
# 메뉴별 페이지 호출

if menu == "1. 광고 카피" :
   main_adcopy(input_area)

elif menu == "2. 유튜브 스크립트":
    main_ytb(input_area)
    
elif menu == "3. SNS 포스팅":
    main_sns(input_area)
    
