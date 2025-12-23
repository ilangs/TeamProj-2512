# 통합 steamlit 처리
import streamlit as st
from adcopy_main_streamlit import main_adcopy
from youtube_main_streamlit import main_ytb
from sns_main_streamlit import main_sns


with st.sidebar :
    menu = st.selectbox("메뉴 선택", ["1. 광고 카피", "2. 유튜브 스크립트","3. SNS 포스팅" ])
    
# 메뉴별 페이지 호출

if menu == "1. 광고 카피" :
   main_adcopy()

elif menu == "2. 유튜브 스크립트":
    main_ytb()
    
elif menu == "3. SNS 포스팅":
    main_sns()
