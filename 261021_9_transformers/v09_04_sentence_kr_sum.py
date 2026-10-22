from transformers import pipeline
# pip install transformers==5.20.2
# 다운 그레이드
# pip install transformers==4.57.6
# pip install transformers==4.46.3
# pip list로 버전 확인

# 1. 요약 파이프라인
summarizer = pipeline("summarization", model="eenzeenee/t5-base-korean-summarization")

# 2.  요약할 원문 (영어 단락)
text = """
인공지능 기술이 빠르게 발전하면서 다양한 산업 분야에서 활용이 늘어나고 있다.
특히 의료 분야에서는 영상 진단 보조, 신약 개발 등에 인공지능이 적극적으로 도입되고 있으며,
금융 분야에서도 사기 탐지와 고객 상담 자동화에 쓰이고 있다.
하지만 개인정보 보호와 책임 소재 같은 문제도 함께 제기되고 있어
관련 제도 마련이 필요하다는 목소리가 커지고 있다.
"""

# 3. 요약 실행
summary = summarizer(
    "summarize: " + text,
    min_length=20,      # 최소 토큰 수
    max_length=100,     # 최대 토큰 수
    do_sample=False     # 매번 동일 결과 출력
)

# 4. 결과 확인
sum_text = summary[0]["summary_text"]
print(f"요약된 문장 : {sum_text}")
# 요약된 문장 : 인공지능 기술이 빠르게 발전하면서 다양한 산업 분야에서 활용이 늘어나고 있다.
# 하지만 개인정보 보호와책임 소재 같은 문제도 함께 제기되고 있어 관련 제도 마련이 필요하다는 목소리가 커지고 있다.
