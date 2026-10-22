from ultralytics import SAM
import time     # 시간을 측정하기 위해 가져옴
import cv2

# 1. 모델 로드
model = SAM("sam_b.pt")     # pt가 파이토치였어?
# sam_b(빠름), l(정확, b보다는 속도 느림)

# 2. 이미지 경로 설정
image_path = "261019_5_yolo_advan/input_sam.jpg"

 # 나는 성공했긴 한데, 이미지 사이즈(?)가 커서? 안 된 사람들 이렇게 해보자고. (2-1, 2-2)
# 2-1. 이미지 읽기
input_image = cv2.imread(image_path)

# 2-2. 이미지 리사이즈
re_input_image = cv2.resize(input_image, (197, 236))

# 3. 추론 시간 측정 시작
start_time = time.time()

# 4. 모델 추론
# model(image_path, save=True)      # 원래
# model(re_input_image, save=True)  # 이미지 사이즈(?)가 커서? 안 된 사람들?
results = model(re_input_image)     # 라벨 제거를 위해 추가

# 5. 추론 시간 측정 종료
end_time = time.time()

# 라벨 제거
no_label_output = results[0].plot(labels=False, boxes=False)

# 결과 이미지 저장  # 라벨 제거를 위해 추가
cv2.imwrite("./output_sam.jpg", no_label_output)

# 6. 결과 로그 출력
if_time = end_time - start_time
print(f"총 추론 시간 : {if_time:.2f}")
print("추론 완료")
