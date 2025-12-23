# LLM 결과물을 음성 파일로 변환

from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def text_to_speech(text) :
    
    filename = f"audio_{int(time.time())}.mp3"
    
    response = client.audio.speech.create(
    model="tts-1",
    voice="fable", 
        # "남성 - 중후한 (Onyx)": "onyx",
        # "남성 - 차분한 (Echo)": "echo",
        # "여성 - 밝은 (Nova)": "nova",
        # "여성 - 부드러운 (Shimmer)": "shimmer",
        # "여성 - 차분한 (Alloy)": "alloy",
        # "공통 - 에너제틱 (Fable)": "fable"
        input=text
    )

    response.write_to_file(filename)
    return filename
    