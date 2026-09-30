# 작업 환경과 규칙 확인

확인일: 2026-09-30 (Asia/Seoul)

## 경로와 지침

- 현재 작업 폴더: `C:\dev\study\healthy-day-codex-lab\project`
- Git 루트: `C:\dev\study\healthy-day-codex-lab`
- 이 폴더에 적용되는 저장소 지침 파일: `C:\dev\study\healthy-day-codex-lab\project\AGENTS.md`
- 실행 방법을 확인한 파일: `C:\dev\study\healthy-day-codex-lab\project\README.md`
- 확인한 상위 경로에는 다른 `AGENTS.md`가 없었다. 이번 대화에서 제공된 프로젝트 지침도 적용 중이다.

## 검증 규칙

- Python 3.13과 `uv`를 사용하고, 설치는 `uv sync --locked`로 수행한다. 의존성을 바꾸면 `pyproject.toml`과 `uv.lock`을 함께 검토한다.
- 코드 변경 뒤 `uv run --locked python -m pytest -q --basetemp=.pytest_cache/tmp`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `git diff --check`, `git diff`, `git status --short`를 실행하고 실제 결과를 기록한다. 새 파일은 내용을 별도로 읽는다.
- 기본 테스트와 CI는 임시 SQLite DB와 모의 생성기·HTTP 응답을 사용한다. 로컬 DB 변경 및 실제 Groq 호출은 하지 않는다. 상품 기능 변경 시 `/health`의 `products=44`, 목록·상세, 화면 페이지별 20/20/4개와 오류 처리를 확인한다.
- LLM 모의 점검은 `uv run --locked python -m scripts.check_llm`을 사용한다. 실제 연결은 별도 `--live` 명령으로 점검하고 모델·환경·시각·소요시간·성공 여부를 기록한다. 두 결과를 혼동하지 않는다.
- 최초 환경 확인에서는 이 기록 문서만 작성했으므로 내용·경로·diff를 검토했고, Python 테스트와 Ruff는 실행하지 않았다.

## 커밋과 PR 규칙

- Git 루트는 `project/`의 상위 폴더이며 `docs/`, `data/`, `project/`를 함께 포함한다. 작업 관련 파일만 명시적으로 stage하고 다른 변경은 섞거나 되돌리지 않는다.
- 커밋 전 `git diff --cached --check`, `git diff --cached`, `git status --short`로 stage 대상과 내용을 확인한다.
- push·PR 전 `git rev-parse --show-toplevel`, `git remote`, `git branch --show-current`와 실제 대상 저장소 및 base/head를 확인한다. remote URL에 든 비밀값은 출력하거나 공유하지 않는다.
- PR에는 목적, 요구사항 ID, 주요 변경, 실제 검증 명령·결과, 미실행 항목·이유를 기록하고 `../docs/templates/pr-body.md`를 참고한다. 기준 브랜치 대비 변경과 새 파일을 모두 리뷰한다. 실행하지 않은 CI·실제 Groq 호출·수동 확인을 성공으로 보고하지 않는다.
- `.env`, DB, `.venv/`, 캐시는 커밋하지 않는다. 비밀값과 상담 입력·답변은 로그·보고서·PR에 남기지 않는다.

## 설정 적용 확인

- `project/.codex/config.toml` 파일에서 `approval_policy = "on-request"`, `sandbox_mode = "workspace-write"`를 확인했다. 현재 세션에 전달된 도구 환경은 `workspace-write`로 표시되어 파일 설정과 일치한다.
- 파일이 존재한다는 사실만으로 Codex가 이 파일을 실제로 읽었는지, `approval_policy`가 이 세션에 적용됐는지는 확정할 수 없다. 확인하려면 `project/`에서 새 Codex 세션을 시작해 세션의 유효 sandbox·approval 설정 표시를 확인한다. 승인 정책은 실제로 승인이 필요한 작업에서 나타나는 승인 요청 동작으로도 확인할 수 있다. 이 기록을 위해 권한 밖 파일 변경이나 승인 요청은 수행하지 않았다.
- 최초 확인 당시 브랜치는 `chore/codex-setup`, remote 이름은 `origin`이었다. 그때 `AGENTS.md`와 `.codex/`는 추적되지 않은 기존 항목이었으며 수정하거나 stage하지 않았다.

## 최초 환경 확인 결과

- `git diff --check`: 통과(출력 없음). 변경 전 `git status --short`: `?? .codex/`, `?? AGENTS.md`.
- 이 문서는 새 파일이므로 일반 `git diff`에는 내용이 나타나지 않는다. 작성 후 파일 내용과 `git status --short`를 별도로 확인했다.
- 테스트, Ruff, LLM 점검, CI, 수동 화면 확인은 문서 기록 작업의 범위가 아니어서 실행하지 않았다. 커밋·push·PR도 수행하지 않았다.
