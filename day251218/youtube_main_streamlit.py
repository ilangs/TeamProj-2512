from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    st.title("유튜브 영상 스크립트 생성 챗봇!")
    
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
                    # 유튜브 스크립트 생성
                    ai_reply=generate_script(topic, length, tone, target)
                
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


def generate_script(topic, length, tone, target) -> str:
    # 프롬프트 생성
    prompt = f'''
    # Role (역할 부여)
    당신은 100만 구독자를 보유한 전문 유튜브 콘텐츠 기획자이자 스크립트 작가입니다.
    시청자의 이탈을 막고 끝까지 보게 만드는 몰입감 있는 대본을 작성해야 합니다.

    # Input Data (입력 정보)
    - 주제: {topic}
    - 목표 영상 길이: {length}
    - 영상 톤앤매너: {tone}
    - 타겟 시청자: {target}

    # Task Instructions (지시 사항)
    위 정보를 바탕으로 아래 구조에 맞춰 유튜브 스크립트를 작성하세요.

    1. **[후킹(Hook)]**: 영상 시작 0~10초 사이. 시청자가 영상을 끄지 않도록 강렬한 질문, 충격적인 사실, 또는 결과 미리보기를 제시하세요.
    2. **[인트로]**: 오늘 다룰 내용이 무엇인지, 왜 이 영상을 끝까지 봐야 하는지 이득(Benefit)을 제시하세요.
    3. **[본론]**: 내용을 논리적으로 3~4가지 핵심 포인트로 나누어 설명하세요. 지루하지 않게 스토리텔링 기법을 사용하세요.
    4. **[결론 및 CTA]**: 내용을 요약하고, 구독/좋아요/댓글을 유도하는 멘트(Call To Action)를 자연스럽게 넣으세요.

    # Output Format (출력 형식)
    1. {topic}에 맞는 제목 만들어 주세요.
    2. [5가지 아이디어 추천] (간략히 제목과 컨셉만)
    3. [베스트 선정 및 추천 사유] (논리적 근거)
    4. [최종 output] (아래 표(Table) 형식으로 작성해 주세요. 300자 이내)
    | 타임코드(예상)   | 화면 설명 (비주얼 가이드)   | 내레이션/대사 (스크립트)   |
    |----------------|--------------------------|-------------------------|
    | 0:00-0:10      | 후킹 장면 설명             | 후킹 대사 작성            |
    | 0:10-0:30      | 인트로 장면 설명           | 인트로 대사 작성          |
    | ...            | ...                      | ...                     |
    | 마무리          | 결론 및 CTA 장면 설명      | 결론 및 CTA 대사 작성     |
    5. 썸네일 문구 만들어 주세요.
    6. 해시테그는 10개 만들어 주세요.
    
    '''
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    main()