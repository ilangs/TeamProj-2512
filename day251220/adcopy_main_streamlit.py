# 광고 문구 생성기
import streamlit as st
from prompt_template import *
from ask_llm import create_script
from moderation_check import moderation_check

def main_adcopy():
    # 대화 이력 초기화
    if 'messages_ad' not in st.session_state:
        st.session_state['messages_ad'] = []

    st.title("광고 카피 메이커!")
    topic = st.text_input("광고할 제품/서비스 이름")
    usp = st.text_input("핵심 문구", placeholder="예: 업계 최초 100% 천연 성분")
    col1, col2 , col3 = st.columns(3) # 화면 분할
    with col1:
        target = st.text_input("타겟 소비자", placeholder="예: 퇴근 후 운동하는 직장인")
    with col2:
        length = st.selectbox("영상 길이", ["1분", "3분", "5분", "10분 이상"])
    with col3:
        channel = st.selectbox("광고 채널", ["유튜브 쇼츠", "틱톡", "페이스북/인스타", "웹페이지 상단"])
    submit = st.button("✨ 광고 카피 생성")

    if submit:
        if not topic:
            st.warning("주제를 입력해주세요!")
        else:
            # 콘텐츠 모더레이션 체크
            moderation_check(topic)

            with st.spinner("전문 카피 라이터가 전략을 짜는 중입니다..."):
                # 프롬프트 생성
                prompt = adcopy_prompt(topic, usp, target, length, channel)
                
                # 스크립트 생성
                ai_reply = create_script(prompt)
            
                # 모델 응답 이력에 추가 및 출력
                st.session_state["messages_ad"].append({"role":"assistant", "content": ai_reply})

    # 지금까지 대화 출력
    for msg in st.session_state['messages_ad']:
        st.chat_message(msg['role']).write(msg['content'])
        st.divider()


if __name__ == "__main__":
    main_adcopy()