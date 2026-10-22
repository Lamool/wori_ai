from ultralytics import solutions
import cv2

# 1. 비디오 경로 설정
cap = cv2.VideoCapture("http://210.99.70.120:1935/live/cctv086.stream/playlist.m3u8")

# 2. 영역 좌표 설정 (dict 형식 - 키로 영역 구분)
region_points = {
    "region1" : [(76, 132), (77, 276), (308, 279), (320, 110)],    # 꼭짓점 4개 잡아서 사각형을 만들어주겠다
    "region2" : [(76, 132), (77, 276), (308, 279), (320, 110), (450, 211), (478, 68), (262, 60)],
    "region3" : [(314, 199), (244, 128), (160, 136), (105, 208), (115, 318), (292, 393), (473, 317), (467, 223), (413, 110), (342, 120)]
}

# v05_08_yolo_get_region.py에서 좌표 클랙해가지고 받아옴
# 클릭된 좌표는 (76, 132) 입니다.
# 클릭된 좌표는 (77, 276) 입니다.
# 클릭된 좌표는 (308, 279) 입니다.
# 클릭된 좌표는 (320, 110) 입니다.

# 클릭된 좌표는 (314, 199) 입니다.
# 클릭된 좌표는 (244, 128) 입니다.
# 클릭된 좌표는 (160, 136) 입니다.
# 클릭된 좌표는 (105, 208) 입니다.
# 클릭된 좌표는 (115, 318) 입니다.
# 클릭된 좌표는 (292, 393) 입니다.
# 클릭된 좌표는 (473, 317) 입니다.
# 클릭된 좌표는 (467, 223) 입니다.
# 클릭된 좌표는 (413, 110) 입니다.
# 클릭된 좌표는 (342, 120) 입니다.
# 클릭된 좌표는 (406, 160) 입니다.
# 클릭된 좌표는 (340, 155) 입니다.

# 3. 모델 로드
yolo_region = solutions.RegionCounter(
    model="yolo11n.pt",
    show=False,
    region=region_points    # 우리가 만든 좌표를 넣어준다
)

# 4. 프레임 처리
while cap.isOpened():   # 실시간으로 들어오는 처리를 계속해줘야 되니까? 반복문을 사용?
    success, frame = cap.read()
    if not success:
        print("프레임 확인해라")
        break
    
    # 4-1. 프레임 크기 조정 (좌표계 통일)
    # ((우리가 지정해둔 좌표값이 있는데 들어오는 게 매번 다르면 틀어질 수 있으니? 하는 것이다
    re_frame = cv2.resize(frame, (640, 480))
    
    # 4-2. 구역 내 객체 수 계산
    results = yolo_region(re_frame)
    
    # 4-3. 처리된 프레임 표시 (show=False => 우리가 직접 창을 띄움)
    cv2.imshow("REGION", results.plot_im)   # solutions에는 ~가 results.plot_im에 있어서 이걸 사용하는 것이다?
    
    # 4-4. q 키를 눌러서 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("q키를 눌러서 종료합니다.")
        break

# 5. 자원 해제
cap.release()
cv2.destroyAllWindows()
