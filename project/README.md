# 건강한하루

건강기능식품의 상품 목록과 상세 정보를 조회하는 애플리케이션입니다.
Streamlit 화면에서 FastAPI를 호출하고, 서비스·저장소 계층을 거쳐 SQLite의 데이터를 조회합니다.
Python 3.13과 uv를 사용합니다.

- 상품 목록 페이지 이동과 상품별 기능성·섭취 방법·주의사항·출처 조회
- CSV 기반 상품·영양소 기능·섭취 기준 데이터 초기 적재
- DB 상태 확인 API와 LLM 연결 점검 도구

현재 상품 조회 기능은 LLM을 사용하지 않으며, RAG 검색·상담 API와 상담 화면은 구현되어 있지 않습니다.

## 1. 폴더 열기

VS Code에서 이 `project` 폴더를 엽니다. 터미널의 현재 위치도 `project`여야 합니다.
기본 데이터 경로는 `../data`입니다. 폴더 구성은 다음과 같습니다.

```text
healthy-day-codex-lab/
├── data/       # 원본 CSV 3개
├── docs/       # 데이터 정의서와 요구사항정의서
└── project/    # 이 프로젝트
```

## 2. 설치와 DB 초기화

```powershell
uv sync --locked
Copy-Item .env.example .env
uv run --locked python -m scripts.init_db
```

이미 `.env`를 작성했다면 복사 명령은 건너뜁니다. macOS/Linux에서는 `cp .env.example .env`를 사용합니다.
처음 동기화할 때 패키지를 내려받습니다. Python 3.13이 없다면 uv가 설치할 수 있습니다.
별도의 가상환경 활성화나 pip 설치는 필요하지 않습니다.

초기화 결과는 `products: 44`, `nutrient_functions: 54`, `intake_references: 228`입니다.
`var/healthy_day.sqlite3`에 저장하며, 같은 명령을 재실행해도 기존 레코드를 덮어쓰거나 중복 적재하지 않습니다.
이 명령은 최초 적재용입니다. CSV 갱신이나 기존 테이블의 컬럼 변경을 반영하는 마이그레이션 명령이 아닙니다.

## 3. 서버 실행

터미널 1 — FastAPI:

```powershell
uv run --locked python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

터미널 2 — Streamlit:

```powershell
uv run --locked python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

- 화면: http://127.0.0.1:8501
- API 문서: http://127.0.0.1:8000/docs
- DB 연결 확인: http://127.0.0.1:8000/health
- 상품 목록: http://127.0.0.1:8000/api/products
- 상품 상세: http://127.0.0.1:8000/api/products/P001

화면에 전체 44개 상품이 표시되고, 첫 페이지에 20개, 3페이지에 4개가 보이면 정상입니다.
상품을 펼쳐 기능성·섭취 방법·주의사항·출처를 확인할 수 있습니다.
종료는 각 터미널에서 `Ctrl+C`를 누릅니다.

## 4. 검증

```powershell
# Windows 사용자 Temp 권한 문제를 피하도록 테스트 임시 경로를 지정합니다.
uv run --locked python -m pytest -q --basetemp=.pytest_cache/tmp
uv run --locked ruff check .
uv run --locked ruff format --check .
```

테스트는 임시 SQLite DB를 만들며 로컬 `var/` DB를 변경하지 않습니다.
CSV 적재·재실행·실패 시 롤백, API 페이지 이동·오류 입력, Streamlit 화면과 API 연결, Groq 모듈을 검증합니다.
Groq는 모의 HTTP 응답으로 검증하므로 테스트에 키나 API 비용이 필요하지 않습니다.

## 5. 코드 구조

```text
backend/
  main.py                 # FastAPI 앱 구성
  config.py               # 환경변수와 경로 설정
  api/                    # HTTP 요청과 응답
  schemas/                # 응답 데이터 형식
  services/               # 업무 로직
  repositories/           # SQL 조회
  db/                     # 연결, 초기 스키마, CSV 적재
  integrations/llm.py      # 고정 응답과 Groq 호출
frontend/
  app.py                  # Streamlit 화면
  api_client.py           # FastAPI HTTP 호출
scripts/                  # DB 초기화와 LLM 연결 점검
tests/                    # 기본 검증
```

화면은 DB나 Groq를 직접 호출하지 않습니다. SQL은 저장소 계층과 DB 초기화 코드에 있습니다.
DB 접근은 Python 표준 라이브러리 `sqlite3`로 구현되어 있습니다.

## 6. LLM 연결 점검

연결 모듈은 고정 응답(`stub`)과 Groq API 호출(`groq`)을 지원합니다. 기본값은 `stub`입니다.

키 없는 고정 응답 확인:

```powershell
uv run --locked python -m scripts.check_llm
```

실제 연결을 점검하려면 `.env`에 `GROQ_API_KEY`와 계정에서 사용할 수 있는 `GROQ_MODEL`을 작성합니다.
연결 모듈을 앱에서 사용할 때는 `LLM_PROVIDER=groq`로 전환합니다. `.env`는 Git에 포함되지 않습니다.

```powershell
uv run --locked python -m scripts.check_llm --live
```

`--live`를 지정했을 때만 이 점검 명령이 Groq에 연결 테스트 문장을 한 번 보냅니다.
실패를 고정 응답으로 감추지 않고 오류로 알립니다. 실제 계정 호출 성공 여부는 별도 확인이 필요합니다.

## 7. 데이터 특성과 제약

CSV의 원본 값과 누락 값을 보존합니다. 데이터 출처의 원문 대조는 아직 수행하지 않았습니다.

- 상품 1개의 `섭취시주의사항`이 비어 있습니다. 누락을 그대로 보존하며 임의 문구로 채우지 않습니다.
- 상한섭취량 72개가 비어 있습니다. `NULL`로 보존하며 0으로 바꾸지 않습니다.
- `350(보충제)` 같은 상한섭취량은 수치와 `upper_limit_raw` 원문을 함께 저장합니다. 경고 기능 구현 시 적용 조건과 단위까지 확인해야 합니다.
- 제품별 영양소 함량이 없어 현재 자료만으로 여러 제품의 섭취량 합산을 구현할 수 없습니다.
- RAG 상담용 공식 근거 문서 원문은 포함되어 있지 않습니다.

## 8. 데이터 품질 점검

CSV의 컬럼 구성, 빈 값, 상품 ID 중복을 확인하려면 다음 명령을 실행합니다.

```powershell
uv run --locked python -m scripts.data_quality_report
```

입력 CSV를 읽고 프로젝트 내부의 `docs/reports/data-quality.md`에 보고서를 생성합니다.
원본 CSV와 DB를 변경하지 않으며, 출처의 정확성·최신성을 검증하지 않습니다.

## 문제 해결

- `uv`를 찾지 못하면 설치 후 VS Code 터미널을 다시 엽니다.
- `backend` 또는 `frontend` 모듈을 찾지 못하면 `project` 폴더에서 위의 `python -m` 명령으로 실행하세요.
- DB 오류(503)가 나오면 `.env`의 `DATABASE_PATH`와 초기화 결과를 확인하세요.
- 화면에서 목록을 읽지 못하면 FastAPI가 실행 중인지, `/health`가 정상인지 확인하세요.
- 포트 8000이 사용 중이면 다른 포트로 API를 실행하고 `.env`의 `API_BASE_URL`도 맞춘 뒤 화면 서버를 재시작하세요.
- Groq 오류는 키·계정 권한·모델 이름·네트워크를 확인하세요. 키를 프롬프트나 저장소에 붙여 넣지 않습니다.

## 참고 문서

- [uv 프로젝트와 잠금 파일](https://docs.astral.sh/uv/guides/projects/)
- [FastAPI 모듈 구성](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)
- [Groq Quickstart](https://console.groq.com/docs/quickstart)
- [Groq 모델 목록](https://console.groq.com/docs/models)
