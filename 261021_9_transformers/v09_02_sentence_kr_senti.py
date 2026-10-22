from transformers import pipeline

# 1. 감정 분석 파이프라인 생성
classifier = pipeline("text-classification", model="matthewburke/korean_sentiment")
# LABEL_0 : 부정 / LABEL_1 : 긍정

# 2. 분석할 문장 입력
# 2-1. 긍정 문장
text = "나는 오늘 정말로 기분이 좋다"
# 문장 분석 결과 : LABEL_1 (긍정)
# 문장 분석 점수 : 0.9657

# 2-2. 부정 문장
# text = "그녀는 오늘 행복하지 않다"
# 문장 분석 결과 : LABEL_0 (부정)
# 문장 분석 점수 : 0.8181

# 2-3. 부정 단어
# text = "화남"
# 문장 분석 결과 : LABEL_0 (부정)
# 문장 분석 점수 : 0.9498

# 여기서 angry의 감정 분석 결과
# 문장 분석 결과 : LABEL_1
# 문장 분석 점수 : 0.5955

# 3. 문장 분석
results = classifier(text)

# 4. 결과 확인
print(f"문장 분석 결과 : {results[0]['label']}")        # POSITIVE, NEGATIVE
print(f"문장 분석 점수 : {results[0]['score']:.4f}")   # 1에 가까울 수록 모델 확신도 높음

