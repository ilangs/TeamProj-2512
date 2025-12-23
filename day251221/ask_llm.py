# AI 호출하여 스크립트 생성

from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 결과물에서 2023년 문구 경우가 있어서 LLM이 현재 날짜 인식이 필요하다고 생각되어
# LLM은 자체적으로 현재 날짜를 알 수 없는데
# Python 함수 date.today()가 Excel의 =today()와 같은 역할을 수행하므로
# Function calling을 통해 LLM이 날짜 정보가 필요하다고 판단할 경우 해당 함수를 호출하고,
# 그 결과를 바탕으로 콘텐츠를 생성하도록 설계했습니다.


# 오늘 날짜 함수
def get_today() :
    today = date.today()
    return {"year": today.year,"month": today.month,"day": today.day}

# LLM에게 알려줄 함수 정의
tools = [
    {
        "type":"function", 
        "function" : {
            "name":"get_today",
            "description":"Returns today's date"
            ,"parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]


def create_script(prompt: str) -> str:
   
    # LLM 1차 호출
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "필요한 경우 현재 날짜를 함수로 확인한다."}, 
            {"role": "user", "content": f"현재 시점을 고려하여 다음을 작성 해 주세요: \n{prompt}"}
            ],
        temperature=0.7,
        tools=tools,
        tool_choice="auto"
        )
    message = response.choices[0].message

    # LLM이 함수 호출을 요청한 경우
    if response.choices[0].message.tool_calls:
            tool_call = message.tool_calls[0]
            
            if tool_call.function.name == "get_today" :
                result = get_today()
            
            # 함수 실행 결과를 다시 LLM에게 전달
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    message,{"role": "tool","tool_call_id": tool_call.id,"content": str(result)}
                    ]
                )                 

    # 최종 결과 처리
    return response.choices[0].message.content
