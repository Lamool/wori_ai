# [Transformers pipeline 과제]
# 1. 1 ~ 4번 파일 복사 후 _en_ => _kr_ 로 파일명만 변경
# 2. _kr_ 파일 안에 코드를 한국어 문장을 입력한 실습으로 수정
# 3. 모델 변경... 파이프라인 변경 등으로 접근하여 진행

# [강사님]
# [유사도]
# model = SentenceTransformer("jhgan/ko-sroberta-multitask")

# [감정 분석]
# classifier = pipeline("sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis")
# # 대체 모델 : model="matthewburke/korean_sentiment" (한국어 전용, 라벨 LABEL_0=부정 / LABEL_1=긍정)

# [문장 생성]
# generator = pipeline("text-generation", model="skt/kogpt2-base-v2")   # 최초 1회 모델 다운로드 필요

# [문장 요약]
# summarizer = pipeline("summarization", model="eenzeenee/t5-base-korean-summarization")

# =====

# 0. 라이브러리 불러오기
from sentence_transformers import SentenceTransformer, util
# SentenceTransformer -> 사전 학습 임베딩 모델 로더 클래스
# util                ->  코사인 유사도·검색 등 보조 함수 묶음

# 1. 모델 로드
model = SentenceTransformer("jhgan/ko-sroberta-multitask")
# 모델 설명 :
    # 영어 문장을 의미 공간에 맵핑
    # 빠름
    # ((문장 유사도 분석하는 모델이다?

# 2. 비교할 두 문장 정의
# 2-1. 의미상 완전히 다른 두 문장 예시 -> 낮은 유사도 기대
# 두 문장의 유사도 : -0.0401
# sen1 = "고양이가 소파에서 자고 있어"
# sen2 = "내일, 나 학교에서 수학 시험 봐"

# 2-2. 의미상 비슷한 두 문장 예시 -> 높은 유사도 기대
# 두 문장의 유사도 : 0.9501
sen1 = "그는 책을 읽고 있어 도서관에서"
sen2 = "그는 도서관에서 책을 읽고 있어"

# 2-3. 비슷한 단어
# 여기서는 dog랑 puppy의 유사도가 0.4418
# 두 문장의 유사도 : 0.7976
# sen1 = "개"
# sen2 = "강아지"

# 3. 문장 -> 숫자 좌표로 바꾸기(인코딩)
emb1 = model.encode(sen1, convert_to_tensor=True)
emb2 = model.encode(sen2, convert_to_tensor=True)

# 4. 두 문장 유사도 측정 (코사인 유사도)
cos_sim = util.pytorch_cos_sim(emb1, emb2)

# 5. 결과 출력
print(f"두 문장의 유사도 : {cos_sim.item():.4f}")
