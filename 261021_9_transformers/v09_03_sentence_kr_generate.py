from transformers import pipeline, PreTrainedTokenizerFast, GPT2LMHeadModel

model_name = "skt/kogpt2-base-v2"

tokenizer = PreTrainedTokenizerFast.from_pretrained(
    model_name,
    bos_token="</s>", eos_token="</s>", unk_token="<unk>",
    pad_token="<pad>", mask_token="<mask>",
)
model = GPT2LMHeadModel.from_pretrained(model_name)

# 1. 텍스트 생성 파이프라인 생성
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 2. 시드 문장 입력 (이어 쓸 첫 부분)
q = input("이어서 쓸 첫 문장을 입력해주세요 : ")

# 3. 텍스트 생성 실행
# results = generator(
#     q,
#     max_new_tokens=50,       # 추가 생성할 토큰 수 (길수록 추론 시간도 길어짐)
#     num_return_sequences=1,  # 반환 문장 1개로 설정
# )

results = generator(
    q,
    max_new_tokens=80,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.8,
    repetition_penalty=1.5,
)

# 4. 결과 출력
print(results[0]['generated_text'])
"""
1.
이어서 쓸 첫 문장을 입력해주세요 : 안녕하세요
안녕하세요!
예. 아이고 네? 예. 감사합니다. 오늘이 월요일인데요.
어제는 어서 집에 가야겠어요.
오랜만에 니꺼가 한잔 좀 사달라고 했는데 이거 한번 할까요?
아~ 근데 요번에 제가 왜 못 샀는지 모르겠는데요
그래도 저한테 너무 많이 물어봐야죠 뭐 이런 말하니까 그냥 내버려두면
2.
이어서 쓸 첫 문장을 입력해주세요 : 도서관에 갔는데 
도서관에 갔는데 넌 이렇게 얘기해줘. 우리 엄마가 엄마랑 같이 와줄게."
"엄마! 너 요즘 무슨 일 있니?"
이런 대답을 하며 말을 건네는 그녀의 손에는 들린 작은 꽃바구니가 들려 있었다.
'너 이 세상에 이런 꽃이 얼마나 있었어!
그렇게 오랜 시간 사랑하고 그리워하며 혼자 간직해왔던 것이다.
그러고 보니 그녀가 정말 사랑하는 마음이 무엇이었
3.
이어서 쓸 첫 문장을 입력해주세요 : 도서관에 가서 책을
도서관에 가서 책을 읽으며 이야기하는 것이 어떠냐고 생각했습니다.
정말이지 책이 좋다고, 책에 대한 이야기를 할 수 있을 거라고 생각했기 때문이었답니다.
그런데 그 사람이 책 읽는 것을 좋아해서인지 이 사람을 만나기 시작했어요.
나는 그를 따라갔지요.
"아, 그래. 나도 도서관에서 읽고 싶다."
이번에는 정색을 하고 말문을 열었어요.
도서관에 들어가자 책상 위에
"""