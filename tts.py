# LLM 결과물을 음성 파일로 변환

from openai import OpenAI  # OpenAI 서비스 도구
from dotenv import load_dotenv  # 설정값 불러오기
import os  # 시스템 접근
import time  # 시간 정보 활용

load_dotenv()  # 설정값 활성화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # AI 연결

def text_to_speech(text) :  # 텍스트를 받아서 음성 파일로 만드는 함수
    
    filename = f"audio_{int(time.time())}.mp3"  # 겹치지 않게 현재 시간을 파일 이름으로 설정
    
    response = client.audio.speech.create(  # OpenAI 음성 생성 API 호출
    model="tts-1",  # 사용할 TTS 모델
    voice="fable",  # 목소리 종류 (에너제틱한 느낌의 Fable)
        # 다양한 목소리 옵션 예시 (선택 가능)
        input=text  # 읽어줄 텍스트 입력
    )

    response.write_to_file(filename)  # 생성된 음성을 파일로 저장
    return filename  # 저장된 파일 이름 반환