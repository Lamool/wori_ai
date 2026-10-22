from ultralytics import YOLO

# 1. 모델 로드
model = YOLO("yolo11n.pt")

# 2. 모델 내보내기
# 파이토치의 모델 형식을 CPU(Intel...)에 최적화된 모델로 내보내 볼 것이다?
model.export(format="openvino")
