from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os
from prompt_template import create_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    st.title("유튜브 영상 스크립트 챗봇!")
    
    # 대화 이력 초기화
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        
    # 지금까지 대화 출력
    for msg in st.session_state['messages']:
        st.chat_message(msg['role']).write(msg['content'])         
    
    # 사용자 입력 화면       
    with st.container():
        topic = st.text_input("유튜브 주제 입력", placeholder="예: 생성형 AI로 돈 버는 법")
        
        col1, col2 = st.columns(2) # 화면 2분할
        with col1:
            length = st.selectbox("영상 길이", ["1분 (쇼츠)", "3분", "5분", "10분 이상"])
        with col2:
            tone = st.selectbox("영상 톤", ["친근한", "전문적인", "유머러스한", "감성적인"])
            
        target = st.text_input("타겟 시청자", placeholder="예: 2030 직장인, 주부")
        
        if st.button("✨ 대본 생성하기"):
            if not topic:
                st.warning("주제를 입력해주세요!")
            else:
            
                # 콘텐츠 모더레이션 체크
                moderation_check(topic)

                with st.spinner("AI가 대본을 작성 중입니다..."):
                    # 프롬프트 생성
                    prompt = create_prompt(topic, length, tone, target)
                    
                    # 유투브 스크립트 생성
                    response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9
                    )
                    ai_reply = response.choices[0].message.content
                
                    # 모델 응답 이력에 추가 및 출력
                    st.session_state["messages"].append({"role":"assistant", "content": ai_reply})
                    with st.chat_message("assistant"):
                        st.markdown(ai_reply)


def moderation_check(text: str) -> bool:
    # 콘텐츠 모더레이션 체크
    check = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    if check.results[0].flagged:
        raise ValueError("입력하신 내용이 부적절하여 처리할 수 없습니다.") 


if __name__ == "__main__":
    main()