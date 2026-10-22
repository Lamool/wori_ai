from sahi.predict import get_sliced_prediction
from sahi import AutoDetectionModel

# 1. 모델 경로
model_path="yolo11n.pt" # yolo11n.pt 상대경로 복사해서 붙여넣음

# 2. 모델 로드
detection_model = AutoDetectionModel.from_pretrained(
    model_type="ultralytics",
    model_path=model_path,
    confidence_threshold=0.4    # 신뢰도. 0.4 이상만 탐지하겠다
)

# 3. SAHI 적용
results = get_sliced_prediction(
    # "demo_data/small-vehicles1.jpeg",
    "demo_data/pexels-ecem-harmankaya-2160554257-37038813.jpg",     # 그냥 궁금해서 이거로 돌려본 건데 결과가...
    detection_model,
    # 어느 정도 크기로 잘라서 볼 것인가
    slice_height=200,
    slice_width=200,
    # 어느 정도 겹쳐서 보게 할 것인가?
    overlap_height_ratio=0.1,
    overlap_width_ratio=0.1
)

# 4. 결과 저장
results.export_visuals(export_dir="sahi/")

# 탐지 출력 로그
print("모든 코드가 성공적으로 수행됐습니다.")
