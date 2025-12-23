from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt_template import create_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    
# 사용자 입력 받기
    topic = input("유투브 주제 입력: ").strip()
    length = input("영상 길이 선택 [1분/3분/5분]: ").strip()
    tone = input("영상 톤 선택 [친근한/전문적인/유머러스한/감성적인]: ").strip()
    target = input("타겟 시청자: ").strip()
    
# 입력 값 검증
    if not topic:
        raise ValueError("주제가 입력되지 않았습니다.")    
    
# 콘텐츠 모더레이션 체크 : 부적절한 콘텐츠가 감지되면 예외 발생
    moderation_check(topic)
    
# 프롬프트 생성
    prompt = create_prompt(topic, length, tone, target)

# AI 모델 호출
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
# AI 응답 추출
    ai_reply = response.choices[0].message.content   

# 결과 출력
    print("\n=== 유투브 영상 스크립트 ===\n")
    print(ai_reply)
    
# 콘텐츠 모더레이션 체크
def moderation_check(text) :
    check = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
# 부적절한 콘텐츠가 감지되면 예외 발생
    if check.results[0].flagged:
        raise ValueError("입력하신 내용이 부적절하여 처리할 수 없습니다.") 
    return True

if __name__ == "__main__":
    main()