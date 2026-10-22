import urllib.request   # 인터넷 주소로 자료 요청하는 도구
import json             # 글자로 된 자료를 사전(dict) 모양으로 바꾸는 도구
import pandas as pd     # 자료를 엑셀 같은 표로 다루는 도구

# 1. 인증 키 -> 정부 사이트에서 받은 "비밀 번호". 이게 있어야 자료를 준다.
key = "db5c00dc1fce45c49049bff225a0fea6"    # its 국가교통정보센터에 신청해서 발급받은 인증키
# 과금 우려있는 API KEY는 코드 노출 그리고 깃허브에 업로드 하지 않음
# .env 환경변수로 관리

# 2. 도로 유형 (its=일반도로, ex=고속도로) -> 어느 도로 CCTV 가져올지 선택
road_type = "its"

# 3. 관심 영역(경도, 위도 범위) -> 지도 위에 사각형 그려서 그 안 CCTV만 요청
minX, maxX = 120.95, 127.02     # 동서(가로) 범위 → 한국 전체 가로
minY, maxY = 30.55, 37.69       # 남북(세로) 범위 → 한국 전체 세로
getType = "json"                # 응답 형식 → JSON(글자로 정리된 자료)

# 4. API URL 조립 -> 위 정보를 모두 합쳐서 "자료 요청 주소" 한 줄로 만든다
url_cctv = (
    f"https://openapi.its.go.kr:9443/cctvInfo"
    f"?apiKey={key}&type={road_type}&cctvType=1"
    f"&minX={minX}&maxX={maxX}"
    f"&minY={minY}&maxY={maxY}&getType={getType}"
)

# 5. 요청 ("만든 주소로 자료 주세요!")
response = urllib.request.urlopen(url_cctv)
# print(response)
# <http.client.HTTPResponse object at 0x000001C1BD56C100>

# 6. bytes -> str
json_str = response.read().decode("utf-8")  # bytes -> str (사람 글자)
# print(json_str)
# {"response":{"coordtype":1,"data":[{"roadsectionid":"","coordx":126.2619601,"coordy":36.75105767,"cctvresolution":"","filecreatetime":"","cctvtype":1,"cctvformat":"HLS","cctvname":"[국도38] 태안 두야교회교차로","cctvurl":"http://cctvsec.ktict.co.kr/4027/GS9cuqRaCq9cmhurLqU/q/tmpzaPlF57N7gi/wOVZjgQFruIygDd/loR38/6Is3x4hzyKf71VEVW4kLZibjCtZbYDKUQuWomOf7FcR6EmTQ="}, ...

json_dict = json.loads(json_str)    # str -> dict (사전 모양)
# print(json_dict)
# {'response': {'coordtype': 1, 'data': [{'roadsectionid': '', 'coordx': 126.2619601, 'coordy': 36.75105767, 'cctvresolution': '', 'filecreatetime': '', 'cctvtype': 1, 'cctvformat': 'HLS', 'cctvname': '[국도38] 태안 두야교회교차로', 'cctvurl': 'http://cctvsec.ktict.co.kr/4027/GS9cuqRaCq9cmhurLqU/q/tmpzaPlF57N7gi/wOVZjgQFruIygDd/loR38/6Is3xonbQ9xxbMHNuXDvzgk0JUv3xxSRwRpYLIRdYuFRSfe4='}, ...

# 7. 데이터 프레임 변환
cctv_play = pd.json_normalize(
    json_dict["response"]["data"], sep=''
)
# print(cctv_play)
#      roadsectionid      coordx     coordy  ... cctvformat             cctvname                                            cctvurl
# 0                   126.261960  36.751058  ...        HLS    [국도38] 태안 두야교회교차로  http://cctvsec.ktict.co.kr/4027/GS9cuqRaCq9cmh...
# 1                   126.612830  36.366430  ...        HLS  [국도 21호선] 보령 봉황터널시점  http://cctvsec.ktict.co.kr/4107/YVJDetuWhH2gGu...
# 2                   126.595440  36.378530  ...        HLS  [국도 21호선] 보령 봉황터널종점  http://cctvsec.ktict.co.kr/4108/uEw2V7VUiudn1P...
# 3                   126.617068  36.506767  ...        HLS  [국도 21호선] 홍성 단아래사거리  http://cctvsec.ktict.co.kr/4109/XIgVIAd5Mc+EOX...
# 4                   126.463910  36.775370  ...        HLS   [국도 29호선] 서산 석림사거리  http://cctvsec.ktict.co.kr/4120/bUjLufPLscQPC/...

# 8. CCTV URL 출력
test_url = cctv_play["cctvurl"][999]
print(f"선택된 CCTV URL : {test_url}")
