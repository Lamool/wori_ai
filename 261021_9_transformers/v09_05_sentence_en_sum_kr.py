# 모델을 사용해서 번역 - 내가 한 거
from transformers import pipeline
# pip install transformers==5.20.2
# 다운 그레이드
# pip install transformers==4.57.6
# pip install transformers==4.46.3
# pip list로 버전 확인

# 1. 요약 파이프라인
summarizer = pipeline("summarization", model="t5-small")

# 2) 번역 모델 (영어 → 한국어)
translator = pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M",
    src_lang="eng_Latn",   # 영어
    tgt_lang="kor_Hang",   # 한국어
)

# 2.  요약할 원문 (영어 단락)
text = """
How can you survive when you can't remember who wants you dead?
Dr. Charly McKenna had the perfect life: a thriving dermatology practice, a luxury apartment overlooking Central Park, and a handsome husband who adored her.
Until the night a bullet tore through her skull… and stole everything.
Now Charly wakes in a rehabilitation hospital unable to walk, speak, or remember her own name. All she knows is that someone tried to kill her―and they may still be out there. As fragments of memory surface, so do unsettling questions about the people around her, including the attentive man who keeps appearing at her bedside.
The truth of what happened that night lives somewhere inside her brain. And as Charly pieces together the jagged edges of her past, she begins to realize the most terrifying possibility: the person who wants her dead might be the one she once trusted most.
From #1 New York Times bestselling author Freida McFadden comes a scalpel-sharp psychological thriller about fractured memory, buried secrets, and how far the mind will go to protect you from the truth.
"""

# 3. 요약 실행
summary = summarizer(
    text,
    min_length=20,      # 최소 토큰 수
    max_length=100,     # 최대 토큰 수
    do_sample=False     # 매번 동일 결과 출력
)

# 4. 결과 확인
sum_text = summary[0]["summary_text"]
print(f"요약된 문장 : {sum_text}")
# v09_04 -> 요약된 문장 : the truth of what happened that night lives somewhere inside her brain .
# from #1 New York Times bestselling author Freida McFadden comes a scalpel-sharp psychological
# thriller about fractured memory and buried secrets .

# 요약된 문장 : the truth of what happened that night lives somewhere inside her brain .
# from #1 New York Times bestselling author Freida McFadden comes a scalpel-sharp psychological
# thriller about fractured memory and buried secrets .


## 과제
# 결과 확인 => 영어 => 번역 => 한국어
# 번역
translated = translator(sum_text, max_length=200)[0]["translation_text"]
print("번역:", translated)

# 번역: 그 밤의 진실은 그녀의 뇌 안에서 어딘가에 살고 있습니다. 뉴욕 타임즈의 베스트셀러 작가 프라이다 맥팩든에서
# 스칼펠처럼 날카로운 심리 스릴러가 등장합니다.
