# SNS 포스팅 생성기
import streamlit as st
from prompt_template import *
from ask_llm import create_script
from moderation_check import moderation_check

def main_sns():
    # 대화 이력 초기화
    if 'messages_sns' not in st.session_state:
        st.session_state['messages_sns'] = []

    st.title("SNS 포스팅 메이커!")
    topic = st.text_input("포스팅 주제")
    col1, col2, col3 = st.columns(3) # 화면 분할
    with col1:
        target = st.text_input("타겟 시청자", placeholder="예: 퇴근 후 운동하는 직장인")
    with col2:
        channel = st.selectbox("플랫폼 선택", ["Instagram", "Facebook", "LinkedIn", "네이버 블로그"])
    with col3:
        tone = st.selectbox("포스팅 톤 선택", ["감성적인", "전문적인", "친근한"])
    submit = st.button("✨ 포스팅 문구 생성")
    
    if submit :
        if not topic:
            st.warning("주제를 입력해주세요!")
        else:
            # 콘텐츠 모더레이션 체크
            moderation_check(topic)

            with st.spinner(f"{channel} 최적화 문구를 작성 중입니다..."):
                # 프롬프트 생성
                prompt = sns_prompt(topic, target, channel, tone)
                
                # 스크립트 생성
                ai_reply = create_script(prompt)
            
                # 모델 응답 이력에 추가 및 출력
                st.session_state["messages_sns"].append({"role":"assistant", "content": ai_reply})
            
    # 지금까지 대화 출력
    for msg in st.session_state['messages_sns']:
        st.chat_message(msg['role']).write(msg['content'])
        st.divider()         


if __name__ == "__main__":
    main_sns()