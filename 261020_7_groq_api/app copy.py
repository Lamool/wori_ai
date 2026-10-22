from dotenv import load_dotenv
import os
from groq import Groq, APIError

# 1. 환경 변수 불러오기 (.env 파일에서 API 키를 읽어옴)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("API 키가 없습니다. .env 파일에 GROQ_API_KEY를 넣어주세요.")
    exit()

# 2. 사용할 모델 이름
GROQ_MODEL = "openai/gpt-oss-20b"

# 3. API 클라이언트 만들기 (키가 있는 것만)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# 4. AI 성격 및 규칙 지정
SYSTEM_PROMPT = """너는 아주 엄격한 CTO 개발자야.
사용자가 에러 메시지나 코드를 보내면 아래 형식으로 짧게 답해.
1) 원인: 한 줄
2) 해결: 고친 코드 또는 명령어
3) 한마디: 다시는 이런 실수를 하지 않도록 따끔한 조언 한 줄
개발과 상관없는 질문에는 '개발 질문만 받는다.'라고만 답해."""

# 대화 기록 (Groq 형식으로 저장)
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 대화 기록이 너무 길어지면 토큰을 많이 쓰므로 최근 대화만 보냄
MAX_HISTORY = 10

def recent_messages():
    """system 메시지 + 최근 대화 MAX_HISTORY개만 돌려줌"""
    return [messages[0]] + messages[1:][-MAX_HISTORY:]

def ask_groq():
    res = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=recent_messages(),
        temperature=0.1,             # 낮을수록 일관된 답
        max_completion_tokens=1000,  # 추론 모델이라 생각하는 토큰까지 포함되므로 넉넉하게
        reasoning_effort="low",
    )
    return res.choices[0].message.content


# 5. 반복 질문 진행
print("=== 엄격한 CTO 에러 해결 도우미 ===")
print("에러 메시지나 코드를 입력하세요. 종료하려면 exit를 입력하세요.\n")

while True:
    # 5-1. 질문 입력
    q = input("나의 질문 : ").strip()

    # 5-2. exit 입력 시 종료
    if q == "exit":
        print("exit를 눌러서 종료합니다.")
        break

    # 빈 입력은 무시
    if not q:
        continue

    # 5-3. 내 질문을 기록에 추가
    messages.append({"role": "user", "content": q})

    # 5-4. 질문 보내고 답변 받기
    try:
        answer, provider = ask_groq(), "Groq"
    except Exception as e:
        print(f"[오류] 답변을 받지 못했습니다: {e}\n")
        messages.pop()  # 실패한 질문은 기록에서 제거
        continue

    print(f"AI의 답변 ({provider}) : {answer}\n")

    # 5-5. AI 답변도 기록에 추가
    messages.append({"role": "assistant", "content": answer})
