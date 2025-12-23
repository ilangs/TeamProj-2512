# LLM 호출하여 스크립트 생성

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = '''
당신은 전문 콘텐츠 크리에이터이자 마케팅 전문가입니다.
현재 날짜는 2025년 12월이므로 과거 연도(2024 이전)를 언급하지 마십시오.
모든 콘텐츠는 2025년 12월의 트렌드, 소비자 행동, 플랫폼 알고리즘,언어 사용을 반영해야 합니다.
'''

def create_script(prompt: str) -> str:
    
    # LLM 호출하여 스크립트 생성
    response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                        ],
                    temperature=0.7                    )
    
    # 결과 처리
    return response.choices[0].message.content
