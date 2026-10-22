# 파일 쓰기 : 새롭게 생성, 기존 내용이 있

# 파일 읽기
# from pydoc import text

# with open("memo.txt", 'w', encoding="utf+8") as f:
#     f.write("새로운 한 줄 추가")
    
# print(text)
# print("완료")

# # print(text)


# # 파일 이어 쓰기
# with open("memo.txt", 'a', encoding="utf+8") as f:
#     f.write("\n 줄바꿈 가능합니까?")
#     print("완료")
    
    
#-----
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("안녕, 파이썬!\n")
    f.write("with문이 자동으로 닫아줌\n")
# 블록을 빠져나오면 파일은 알아서 닫힘

with open("memo.txt", "r", encoding="utf-8") as f:
    text = f.read()
print(text)
# 안녕, 파이썬!
# with문이 자동으로 닫아줌

with open("memo.txt", "a", encoding="utf-8") as f:
    f.write("새로운 한 줄 추가\n")
# 기존 내용은 그대로, 끝에만 한 줄이 더 붙음