# 주제의 적합성 여부 점검

from openai import OpenAI  # OpenAI 서비스 도구
from dotenv import load_dotenv  # 설정값 불러오기
import os  # 시스템 접근

load_dotenv()  # 설정값 활성화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # AI 연결

def moderation_check(text) :  # 텍스트의 유해성을 체크하는 함수
    # 콘텐츠 모더레이션 체크
    check = client.moderations.create(  # OpenAI의 검열 API 호출
        model="omni-moderation-latest",  # 최신 검열 모델 사용
        input=text  # 검사할 텍스트 입력
    )
    # 부적절한 콘텐츠가 감지되면 예외 발생
    if check.results[0].flagged:  # 만약 유해성 기준에 걸렸다면
        raise ValueError("입력하신 내용이 부적절하여 처리할 수 없습니다.")  # 에러 메시지 띄우고 중단
    return True  # 통과 시 정상 진행
