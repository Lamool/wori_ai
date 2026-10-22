import cv2  # 카메라를 다루는 도구
import os   # 폴더를 만드는 도구
from datetime import datetime   # 지금 시간을 알려주는 도구
import schedule

# 사진 캡쳐 간격 설정
interval_time = 5

def capture_image():
    # [1단계] 사진을 저장할 폴더 준비
    save_dir = "./captured_images"  # ((./ 하면 현재 경로에서
    os.makedirs(save_dir, exist_ok=True)    # 폴더가 없으면 자동으로 만듦

    # [2단계] 카메라를 켭니다.
    cap = cv2.VideoCapture(0)   # cv2.VideoCapture(0) — 카메라를 켜는 코드 (0은 내 컴퓨터의 첫 번째 카메라)

    # [3단계] 사진을 한 장 찍는다.
    success, frame = cap.read()  # success=True면 성공, frame=찍힌이미지
    # cap.read() — 카메라에서 사진 한 장을 가져옴
    if success:
        # 사진 파일명 : 찍은 시간을 쓰면 여러 장을 찍어도 이름이 겹치지 않는다. + 언제 찍었는지 알 수 있다.
        timestamp = datetime.now().strftime("%Y%m_%H%M%S")
        # Example: "%d/%m/%Y, %H:%M:%S" 이걸로 했다가 사진이 안 만들어짐.
        # window에서 /를 폴더로 인식해서 그런 거였다.
        file_path = os.path.join(save_dir, f"result_{timestamp}.jpg")
        
        # 파일로 저장
        cv2.imwrite(file_path, frame)   # cv2.imwrite() — 사진을 파일로 저장
        print(f"사진이 잘!! 저장됐습니다.{file_path}")
    else :
        print("카메라 읽기 실패!!")

    # [4단계] 카메라를 끕니다.
    cap.release()
    
# 스케줄러 설정
schedule.every(interval_time).seconds.do(capture_image)

# 스케줄러 실행
while True:
    schedule.run_pending()  # 예약된 작업 실행
