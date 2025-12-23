# 광고 카피 생성 메인 프로세스 Streamlit

import streamlit as st
from prompt_template import *
from moderation_check import moderation_check
from ask_llm import create_script
from tts import text_to_speech

def main_adcopy():
    with st.sidebar :
        st.title("광고 카피 메이커!")
    
    # 대화 이력 초기화
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        
    # 사용자 입력 화면
    with st.container():
        topic = st.text_input("제품/서비스명 입력", placeholder="예: 생성형 AI")
        message = st.text_input("핵심 문구", placeholder="예: 세계 최초")
        target = st.text_input("타겟 소비자", placeholder="예: 2030 직장인, 주부")
      
    if st.button("✨ 광고 카피 생성"):
        if not topic:
            st.warning("제품/서비스명을 입력해주세요!")
        else:
            # 콘텐츠 모더레이션 체크
            moderation_check(topic)

            with st.spinner("전문 카피 라이터가 전략을 짜는 중입니다..."):
                # 프롬프트 생성
                prompt = adcopy_prompt(topic, message, target)
                
                # 광고 카피 스크립트 생성
                ai_reply = create_script(prompt)
                
                # 음성 파일 생성 (베스트 부분만 음성 변환, 없으면 전체 변환)
                if "[BEST]" in ai_reply :
                    best_part = ai_reply.split("[BEST]")[-1].strip()
                    audio_file = text_to_speech(best_part)
                else :
                    audio_file = text_to_speech(ai_reply)
                
                # 모델 응답 이력에 텍스트와 음성을 한쌍으로 저장
                st.session_state["messages"].append(
                    {"role":"assistant", "content": ai_reply, "audio": audio_file}
                    )
            
    # 텍스트와 음성 포함한 누적 결과 출력 (최근 결과를 위쪽으로 출력)
    for msg in reversed(st.session_state["messages"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/mp3")
            st.divider()


if __name__ == "__main__":
    main_adcopy()