from transformers import pipeline

# 1. 텍스트 생성 파이프라인 생성
generator = pipeline("text-generation", model="gpt2")   # 최초 1회 모델 다운

# 2. 시드 문장 입력 (이어 쓸 첫 부분)
q = input("이어서 쓸 첫 문장을 입력해주세요 : ")

# 3. 텍스트 생성 실행
results = generator(
    q,
    max_new_tokens=50,       # 추가 생성할 토큰 수 (길수록 추론 시간도 길어짐)
    num_return_sequences=1,  # 반환 문장 1개로 설정
)

# 4. 결과 출력
print(results[0]['generated_text'])
"""
1.
이어서 쓸 첫 문장을 입력해주세요 : a book
a book. We are looking for an original artist for this project. We feel that the book
is a great opportunity to bring the world of "The Book of Mormon" to life as a whole.
We will be creating a new book, which will be written
2.
이어서 쓸 첫 문장을 입력해주세요 : 안녕 
안녕탄이 다시라타진진서방니다.

두크를 가�
3.
어서 쓸 첫 문장을 입력해주세요 : Hello
Hello, there are two things that I want to make clear:

1. You can't change my character's name. This is not possible.

2. I want you to leave an impression on me.

The following is the
4.
이어서 쓸 첫 문장을 입력해주세요 : 아주 졸릴 때
아주 졸릴 때도 있어람었 었아주를 우자이 이체는 이자
"""