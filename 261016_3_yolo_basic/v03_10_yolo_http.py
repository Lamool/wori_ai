from ultralytics import YOLO        # YOLO 모델 라이브러리
import cv2                          # OpenCV — 영상·이미지 처리 라이브러리

# 1. 모델 로드 (n = nano, 가장 가벼운 모델 / n → s → m → l → x 순으로 무거워짐)
model = YOLO("yolo11n.pt")

# 2. CCTV 스트림 주소
stream_url = "https://cctvsec.ktict.co.kr/6570/slzNyfjZScqUil9yWzqaodLVZ3Vcd96mcByEv5wKi+FUSqSzY4ai6yMiFF+8XSbX"
cap = cv2.VideoCapture(stream_url)

# 3. 실시간 프레임 처리
while cap.isOpened():               # 스트림이 정상 열려 있는 동안 반복
    success, frame = cap.read()     # 프레임 한 장 읽기
    if not success:
        print("CCTV URL 또는 웹캠 확인해주세요.")
        break                       # 읽기 실패 -> 루프 종료
    
    # 스트림 잘 읽어왔을 때 처리
    # 3-1. 모델 추론 (프레임 한 장 YOLO 추론)
    results = model(frame, conf=0.5)
    # frame : 탐지할 이미지
    # conf=0.5 : 확률 50% 미만 탐지는 버린다 (CCTV 저화질일 경우 0.3까지 낮춰도 된다)
    
    # 3-2. 탐지 결과(박스·클래스명·확률)가 그려진 프레임 얻기
    annotated_frame = results[0].plot()
    # results[0] — 프레임 1장을 넣었으므로 결과도 1개
    
    # 3-3. 윈도우 창 그리기
    cv2.imshow("CCTV_YOLO", annotated_frame)   # frame을 넣으면 원본 영상, annotated_frame을 넣어야 탐지된 게
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q키를 눌러서 종료")
        break
    # 'q' 키 누르면 종료
    # cv2.waitKey(1) — 1ms 동안 키 입력 확인 (안 누르면 -1)
    # & 0xFF         — 키 번호의 뒤 8비트만 남김
    
# 4. 자원 해제
cap.release()
cv2.destroyAllWindows()
