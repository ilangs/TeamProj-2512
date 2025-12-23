# LLM 호출하여 스크립트 생성

from openai import OpenAI  # OpenAI 서비스 이용을 위한 도구
from dotenv import load_dotenv  # 환경변수(.env) 파일 읽기용
import os  # 운영체제 시스템 정보 접근용

load_dotenv()  # .env 파일에 저장된 설정값 불러오기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 내 API 키로 AI 연결

system_prompt = '''  # AI에게 부여할 기본 인격(페르소나) 설정
당신은 전문 콘텐츠 크리에이터이자 마케팅 전문가입니다.
현재 날짜는 2025년 12월이므로 과거 연도(2024 이전)를 언급하지 마십시오.
모든 콘텐츠는 2025년 12월의 트렌드, 소비자 행동, 플랫폼 알고리즘,언어 사용을 반영해야 합니다.
'''

def create_script(prompt: str) -> str:  # 프롬프트를 받아 답변을 주는 함수
    
    # LLM 호출하여 스크립트 생성
    response = client.chat.completions.create(  # AI 모델에 질문 던지기
                    model="gpt-4o",  # 사용할 모델명 지정
                    messages=[
                        {"role": "system", "content": system_prompt},  # AI의 역할 전달
                        {"role": "user", "content": prompt}  # 사용자의 구체적 요청 전달
                        ],
                    temperature=0.7  # 창의성 조절 (0~2 사이, 높을수록 창의적임)
                    )
    
    # 결과 처리
    return response.choices[0].message.content  # AI가 생성한 텍스트만 추출해서 반환