from ultralytics import YOLO
import cv2

# 1. 모델 로드
# model = YOLO("yolo11n.pt")    # 나노 모델
# model = YOLO("yolo11s.pt")    # 스몰 모델
model = YOLO("yolo11n.pt")

# 2. 모델 추론
# results = model("261014_2_yolo_basic/input_det.jpg") # 탐지하고 싶은 이미지
results = model("261014_2_yolo_basic/input_video2.mp4")         # 탐지하고 싶은 동영상

# 3. 결과 시각화
results_image = results[0].plot()

# 4. 결과 이미지 저장
# 기존 방식
# output_path = "./outputde.jpg"
# cv2.imwrite(output_path, results_image)
cv2.imwrite("./output_det_video2.jpg", results_image)

print("결과 이미지 잘 저장 됐습니다!!")
