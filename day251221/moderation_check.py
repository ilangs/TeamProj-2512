# 주제의 사회성 적합 여부 점검

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def moderation_check(text) :
    # 콘텐츠 모더레이션 체크
    check = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    # 부적절한 콘텐츠가 감지되면 예외 발생
    if check.results[0].flagged:
        raise ValueError("입력하신 내용이 부적절하여 처리할 수 없습니다.") 
    return True