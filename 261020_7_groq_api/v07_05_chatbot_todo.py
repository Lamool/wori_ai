# [groq api key 활용해서 깃허브 레포 새롭게 구축]
# 레포명 : 261020_bucheon_chatbot_이름이니셜
# 예 : 261020_bucheon_chatbot_kdj
# 작업 폴더 경로 : wori/261020_7_groq_api/261020_bucheon_chatbot_이름이니셜/

# 1. groq api key를 활용한 챗봇 제작
# 2. cluade 활용하여 로컬 형태 수준 혹은 자유롭게 개발
# 3. .env 관리 점검
# 4. requirements.txt 생성 필수(필요 라이브러리 목록 확인)
# 5. README.md 사용법 작성 필수
# 6. 구글 드라이브 수업 자료 문서에 깃허브 링크 추가
# - groq api key 소진 시 gemini api key 활용

from dotenv import load_dotenv
import os
from groq import Groq

# 1. 환경 변수 불러오기
load_dotenv()

# 2. API 입력
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 3. 대화 기록 맨 앞에 AI 성격 및 규칙 지정
messages = [
    {
        "role": "system",
        "content": "너는 아주 엄격한 CTO 개발자야. 아주 짧게 답해."
    }
]

# 4. 반복 질문 진행
while True:
    # 4-1. 질문 입력
    q = input("나의 질문 : ")
    
    # 4-2. exit 입력시 종료
    if q == "exit":
        print("exit를 눌러서 종료합니다.")
        break
    
    # 4-3. 내 질문을 기록에 추가
    messages.append(
        {
            "role" : "user",
            "content" : q
        }
    )
    
    # 4-4. 질문 보내기
    res = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.1,            # 낮을 수록 일관된 답
        max_completion_tokens=300,  # 답변 최대 길이
        reasoning_effort="low"
    )

    # 4-5. 답변 받기!
    answer = res.choices[0].message.content
    print(f"AI의 답변 : {answer}")
    
    # 4-6. AI 답변도 기록에 추가
    messages.append(
        {
        "role": "assistant",
        "content": answer
        }
    )

