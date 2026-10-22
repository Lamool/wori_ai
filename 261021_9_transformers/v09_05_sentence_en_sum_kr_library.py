# 라이브러리를 사용해서 번역
from deep_translator import GoogleTranslator    # 구글 번역
from transformers import pipeline
# pip install transformers==5.20.2
# 다운 그레이드
# pip install transformers==4.57.6
# pip install transformers==4.46.3
# pip list로 버전 확인

def trans_en_to_ko(sum_en_text:str)-> str: 
    """
    주어진 영어 문장을 한국어로 번역하는 함수
    """
    sum_ko_text = GoogleTranslator(source="en", target="ko").translate(sum_en_text)
    return sum_ko_text

# MyMemoryTranslator로 한다면
# def trans_en_to_ko(sum_en_text:str)-> str:
#     """
#     주어진 영어 문장을 한국어로 번역하는 함수
#     """
#     sum_ko_text = MyMemoryTranslator(source="en-US", target="ko-KR").translate(sum_en_text)
#     return sum_ko_text
    
# 1. 요약 파이프라인
summarizer = pipeline("summarization", model="t5-small")

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
sum_en_text = summary[0]["summary_text"]
print(f"요약된 문장 : {sum_en_text}")
# 요약된 문장 : the truth of what happened that night lives somewhere inside her brain .
# from #1 New York Times bestselling author Freida McFadden comes a scalpel-sharp psychological
# thriller about fractured memory and buried secrets .

sum_ko_text = trans_en_to_ko(sum_en_text)
print(f"한국어로 번역 후 요약된 문장 : {sum_ko_text}")



# GoogleTranslator 사용 시
# Exception has occurred: TooManyRequests
# Server Error: You made too many requests to the server.According to google, you are allowed to make 5 requests per secondand up to 200k requests per day. You can wait and try again later oryou can try the translate_batch function
# 에러 발생

# 다른 방법
# 1. translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", src_lang="eng_Latn", tgt_lang="kor_Hang")
# from deep_translator import MyMemoryTranslator
