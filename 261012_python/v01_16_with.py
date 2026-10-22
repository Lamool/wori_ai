# 1. x 모드
# with open("memo2.txt", 'x', encoding="utf+8") as f:
#     f.write("x모드")

# 2. rb 모드 (이미지 읽기)
# with open("temp.img", 'rb') as img:
#    img_data = img.read()
# print(img_data)

# # 3. wb 모드 (이미지 쓰기)
# with open("wb_img.img", 'wb') as m_img:
#     m_img.write(img_data)

# 4. r+ 모드 (읽기와 쓰기 둘 다)
with open("memo.txt", 'r+', encoding="utf+8") as f:
    text = f.read() # 먼저 읽기
    f.seek(0)       # 맨 앞부터 사용
    
    
    
    f.write("r+모드")
    print(f.read())
