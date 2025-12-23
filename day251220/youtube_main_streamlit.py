# 유튜브 스크립트 생성기
import streamlit as st
from prompt_template import *
from ask_llm import create_script
from moderation_check import moderation_check

def main_ytb():
    # 대화 이력 초기화
    if 'messages_ytb' not in st.session_state:
        st.session_state['messages_ytb'] = []

    st.title("유튜브 콘텐츠 메이커!")
    topic = st.text_input("유튜브 주제", placeholder="예: 생성형 AI 활용법")
    col1, col2, col3 = st.columns(3) # 화면 분할
    with col1 :
        target = st.text_input("타겟 시청자", placeholder="예: 2030 직장인, 주부")
    with col2:
        length = st.selectbox("영상 길이", ["1분(쇼츠)", "3분", "5분", "10분 이상"])
    with col3:
        tone = st.selectbox("영상 톤", ["친근한", "전문적인", "유머러스한", "감성적인"])
    submit = st.button("✨ 대본 생성하기")

    if submit :
        if not topic:
            st.warning("주제를 입력해주세요!")
        else:
            # 콘텐츠 모더레이션 체크
            moderation_check(topic)

            with st.spinner("유튜브 영상 최적화 대본을 작성 중입니다...") :
                # 프롬프트 생성
                prompt = youtube_prompt(topic, target, length, tone)
                
                # 스크립트 생성
                ai_reply = create_script(prompt)
            
                # 모델 응답 이력 추가
                st.session_state["messages_ytb"].append({"role":"assistant", "content": ai_reply})

            # 지금까지 대화 출력
    for msg in st.session_state['messages_ytb']:
        st.chat_message(msg['role']).write(msg['content'])
        st.divider()         
            

if __name__ == "__main__":
    main_ytb()