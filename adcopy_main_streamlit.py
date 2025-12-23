# 광고 카피 생성 메인 프로세스 Streamlit

import streamlit as st  # 웹 UI 도구
from prompt_template import * # 미리 짜둔 질문 양식들 불러오기
from moderation_check import moderation_check  # 안전 검사 함수 불러오기
from ask_llm import create_script  # AI 답변 요청 함수 불러오기
from tts import text_to_speech  # 음성 변환 함수 불러오기

def main_adcopy():
    with st.sidebar :  # 사이드바 영역
        st.title("광고 카피 메이커!")
    
    # 대화 이력 초기화
    if 'messages' not in st.session_state:  # 세션(대화 저장소)에 데이터가 없으면
        st.session_state['messages'] = []  # 빈 리스트로 시작
        
    # 사용자 입력 화면
    with st.container():  # 입력창들을 모아두는 상자
        topic = st.text_input("제품/서비스명 입력", placeholder="예: 생성형 AI")   # 제품 또는 서비스 이름 입력
        message = st.text_input("핵심 문구", placeholder="예: 세계 최초")         # 핵심문구 입력
        target = st.text_input("타겟 소비자", placeholder="예: 2030 직장인, 주부") # 타겟 소비자 입력
      
    if st.button("✨ 광고 카피 생성"): # 버튼을 클릭하면 실행
        if not topic:
            st.warning("제품/서비스명을 입력해주세요!")  # 경고창 띄우기
        else:
            # 콘텐츠 모더레이션 체크
            moderation_check(topic)  # 입력한 주제가 유해한지 확인  

            with st.spinner("전문 카피 라이터가 전략을 짜는 중입니다..."):  # 로딩 표시
                # 프롬프트 생성
                prompt = adcopy_prompt(topic, message, target)  # 질문 양식 완성
                
                 # 스크립트 생성
                ai_reply = create_script(prompt)  # AI에게 답변 받아오기
            
                # 음성 파일 생성 (베스트 부분만 음성 변환, 없으면 전체 변환)
                if "[BEST]" in ai_reply :  # 만약 AI가 'BEST'라고 표시한 부분이 있다면
                    best_part = ai_reply.split("[BEST]")[-1].strip()  # BEST 이후의 텍스트만 추출
                    audio_file = text_to_speech(best_part)  # 그 부분만 음성으로 만듦
                else :
                    audio_file = text_to_speech(ai_reply)  # 없으면 전체를 음성으로 만듦
                
                # 모델 응답 이력에 텍스트와 음성을 한쌍으로 저장
                st.session_state["messages"].append(  # 대화 기록에 추가
                    {"role":"assistant", "content": ai_reply, "audio": audio_file}
                    )
            
    # 텍스트와 음성 포함한 누적 결과 출력 (최근 결과를 위쪽으로 출력)
    for msg in reversed(st.session_state["messages"]) :  # 저장된 기록을 최신순으로 반복 출력
        with st.chat_message(msg["role"]):  # 채팅 메시지 형태로 표시
            st.markdown(msg["content"])  # 텍스트 내용 출력
            if "audio" in msg:
                st.audio(msg["audio"], format="audio/mp3")  # 오디오 플레이어 출력
            st.divider()  # 구분선


if __name__ == "__main__":
    main_adcopy()