import pytesseract      # OCR 사용
from PIL import Image   # 이미지 처리 도구
import os

# 1. Tesseract 실행 파일 경로 지정
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# 2. 이미지 불러오기
# image = Image.open("261021_10_ocr/input.jpg")
# image = Image.open("261021_10_ocr/input_kr.jpg")
image = Image.open("261021_10_ocr/car4.jpg")

# 3. OCR 수행
results = pytesseract.image_to_string(
    image,
    # lang="eng"  # 언어 설정을 영어로
    lang=""kor""
    # lang="eng+kor"
)

# 4. 결과 출력
print(f"OCR 실행 결과 : {results}")
"""
1. lang="eng"
OCR 실행 결과 : 
This is a lot of 12 point text to test the
ocr code and see if it works on all types
of file format.

The quick brown dog jumped over the
lazy fox. The quick brown dog jumped
over the lazy fox. The quick brown dog
jumped over the lazy fox. The quick
brown dog jumped over the lazy fox.


2. lang="kor"
OCR 실행 결과 :
Ｌ스트스때스56<1때

이수진

팀장 / 제품개발팀

+123-456-7890
1『6110@「62117/8「620[5166.0007
123 40616 56, 407 다, 51 12345


3. lang="eng+kor"
OCR 실행 결과 :
LARANASKIN

이수진

팀장 / 제 품 개발팀

+123-456-7890
hello@reallygreatsite.com
123 Anywhere St., Any City, ST 12345
"""

## 1. 차량 번호판 이미지 인식

## 2. pytesseract 말고 다른 OCR과 성능 비교 (네이버 OCR - CLOVA OCR)


# reader = easyocr.Reader(["ko", "en"])

# OCR 실행 결과 :
# 강원 통천
# 가 3108
# 1가 2
# 3456
# 걸린 시간 : 1.48초

# result = reader.readtext("261021_10_ocr/input_car.jpg", detail=0)
# detail=0 으로 주면 값만 볼 수 있음

# paddleOCR

##
# https://www.ultralytics.com/ko/blog/build-an-anpr-system-with-ultralytics-yolo11-and-gpt-4o-mini#deploying-an-anpr-system
# https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e
