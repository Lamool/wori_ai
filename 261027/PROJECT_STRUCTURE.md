# FastAPI 프로젝트 구조

경사로 계산 코드(`core/`)는 웹 코드(`app/`)와 분리한다.

```
project/
├─ app/
│  ├─ main.py            # FastAPI 앱 생성, 라우터 등록
│  ├─ config.py          # 설정 (.env 읽기)
│  ├─ database.py        # DB 연결, 세션
│  ├─ models.py          # DB 테이블 (SQLAlchemy)
│  ├─ schemas.py         # 요청/응답 형식 (Pydantic)
│  ├─ deps.py            # 공통 의존성 (현재 사용자, 관리자 체크)
│  ├─ routers/
│  │  ├─ routes.py       # 경로 추천, 구간 난이도
│  │  ├─ users.py        # 로그인, 이동 조건 설정
│  │  ├─ reports.py      # 장애물·불편 구간 제보
│  │  ├─ facilities.py   # 주변 장애 시설 검색
│  │  └─ admin.py        # 제보 검수, 관리자 기능
│  ├─ services/          # 라우터가 부르는 비즈니스 로직
│  ├─ templates/         # Jinja2 HTML
│  └─ static/            # JS, CSS, 이미지
├─ core/                 # 기존 경사로 계산 코드 (FastAPI 의존 없음)
│  ├─ slope.py
│  └─ pathfinding.py
├─ tests/
├─ .env                  # 비밀 정보 (커밋 금지)
├─ .gitignore
└─ requirements.txt
```

## 원칙

- `routers/`는 요청을 받고 응답만 한다. 실제 로직은 `services/`와 `core/`로 넘긴다.
- `core/`는 FastAPI를 import하지 않는다. 단독 테스트와 재사용이 쉽다.
- `models.py`는 DB 구조, `schemas.py`는 API 입출력이다. 둘을 분리한다.
- 기능이 커지면 `routers/reports/` 같은 폴더로 쪼갠다.
- 처음부터 다 만들 필요 없다. `main.py`, `routers/routes.py`, `core/`로 시작해 기능이 생길 때마다 추가한다.

## 폴더·파일 설명

### app/
웹 서버 코드 전체. 계산 로직(`core/`)과 웹 코드를 분리하려고 따로 둔다.

### app/main.py
- 앱을 만들고 라우터를 등록하는 시작점.
- 서버 실행 때 가장 먼저 읽힌다 (`uvicorn app.main:app`).
- 전체 연결만 하고 로직은 넣지 않는다.

### app/config.py
- `.env`에서 DB 주소, 비밀키 같은 설정을 읽는다.
- 설정이 코드 곳곳에 흩어지는 것을 막고, 비밀 정보를 코드에 쓰지 않기 위해 둔다.

### app/database.py
- DB 연결과 세션을 만든다.
- 연결 코드를 한 곳에 모아야 SQLite에서 PostgreSQL로 바꿀 때 여기만 고치면 된다.

### app/models.py
- DB 테이블 정의 (User, Report, Facility 등).
- 데이터 구조를 한눈에 보기 위해 둔다.

### app/schemas.py
- API가 받고 주는 데이터 형식 (Pydantic).
- 잘못된 입력을 자동 검증하고 `/docs` 문서도 만든다.
- `models.py`와 분리하는 이유는 비밀번호 같은 DB 컬럼을 응답에 실수로 노출하지 않기 위해서다.

### app/deps.py
- 여러 곳에서 쓰는 공통 처리: 현재 로그인 사용자 확인, 관리자 권한 체크, DB 세션 주입.
- 라우터마다 같은 코드를 반복하지 않으려고 둔다.

### app/routers/
URL별 요청 처리 파일. 기능별로 나눈다.

- `routes.py`: 경로 추천, 구간 난이도
- `users.py`: 로그인, 이동 조건 설정
- `reports.py`: 제보 등록·조회
- `facilities.py`: 주변 시설 검색
- `admin.py`: 제보 검수, 관리자 기능

한 파일에 몰면 수백 줄이 되어 찾기 어렵고, 팀 작업 시 충돌이 나서 나눈다.

### app/services/
- 라우터가 부르는 실제 업무 로직 (예: 제보 승인 시 처리, 사용자 조건을 반영한 경로 계산 호출).
- 라우터는 얇게, 로직은 여기에 둬야 테스트와 재사용이 쉽다.

### app/templates/
Jinja2 HTML 파일. 서버가 데이터를 넣어 화면을 만든다.

### app/static/
브라우저가 그대로 받아가는 파일 (JS, CSS, 이미지, Leaflet 설정 코드).

### core/
기존 경사로 계산 코드.

- `slope.py`: 경사도 계산, 난이도 판정
- `pathfinding.py`: 대체 경로 탐색

FastAPI를 import하지 않으므로 웹 없이 단독 실행·테스트가 되고, 나중에 웹 프레임워크를 바꿔도 건드리지 않는다.

### tests/
자동 테스트. 경사도 계산이 맞는지, API가 제대로 응답하는지 확인한다. 기능을 고칠 때 기존 기능이 깨졌는지 바로 알 수 있다.

### .env
DB 비밀번호, API 키 같은 비밀 정보. 코드에 직접 쓰면 깃에 올라가 유출된다.

### .gitignore
깃에 올리면 안 되는 파일 목록 (`.env`, `*.pt`, `*.npy`, `__pycache__` 등).

### requirements.txt
필요한 라이브러리 목록. 다른 사람이나 서버에서 `pip install -r requirements.txt`로 같은 환경을 만든다.
