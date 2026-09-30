# 건강한하루 프로젝트 문서

기존 상품 조회 기능과 추가할 RAG 상담 기능의 요구사항, 데이터 정의, 구현·검증 기준을 정리합니다. 현재 구현 상태와 실행 방법은 [프로젝트 README](../project/README.md)를 확인합니다.

## 읽는 순서

| 문서 | 읽을 부분 | 역할 |
| --- | --- | --- |
| [요구사항정의서.xlsx](요구사항정의서.xlsx) | `RAG_구현범위` | 첫 버전의 범위와 원문 요구사항 연결 |
| [데이터 정의서.xlsx](<데이터 정의서.xlsx>) | 기존 CSV 시트, `RAG_문서`, `RAG_API` | 시작 데이터와 추가할 문서·API 계약 |
| [RAG 구현 명세](<RAG 구현 명세.md>) | 전체 | 공통 구현·검증 계약 |
| [RAG 상담 요구사항 초안](<RAG 상담 요구사항 초안.md>) | 결정할 질문 | 사용자·상담 범위·완료 기준 합의 |
| [합성 테스트 자료](fixtures/README.md) | RAG 자료 | API 키 없이 검색·실패 경로 재현 |

Excel의 기존 시트는 전체 서비스 요구사항과 CSV 정의입니다. 첫 버전의 구현 범위는 `RAG_구현범위`와 RAG 구현 명세를 따릅니다. 전체 서비스의 수용 여부와 첫 버전의 완료 상태를 구분합니다.

## 작업 문서와 템플릿

템플릿을 바탕으로 `project/docs/`에 실제 결정과 결과를 작성합니다. 대괄호는 실제 값으로 바꾸며, 미결 조건과 미실행 검증은 상태와 이유를 기록합니다.

- [요구사항 템플릿](templates/rag-requirements.md) → `project/docs/requirements/rag-chatbot.md`
- [계획 템플릿](templates/rag-plan.md) → `project/docs/plans/rag-chatbot.md`
- [PR 본문 템플릿](templates/pr-body.md) → `project/docs/pr/rag-chatbot.md`
- [검증·리뷰 기록 템플릿](templates/change-review.md) → `project/docs/reports/rag-review.md`
- [변경 검증 템플릿](templates/change-validation.md) → `project/docs/reports/`의 단위별 기록·`rag-validation.md`

## 개발 작업용 Skill

검증·커밋·PR 작업에 사용할 Skill입니다. 사용하려면 아래 세 폴더를 `project/.agents/skills/`로 복사합니다. 이미 설치된 다른 Skill은 유지합니다.

| 제공 Skill | 역할 |
| --- | --- |
| [verify-changes](skills/verify-changes/SKILL.md) | 요구사항·계획 대조, 테스트·품질 검사, 현재 코드에 해당하는 검증 기록 |
| [commit-changes](skills/commit-changes/SKILL.md) | 검증 근거와 staged diff 확인, 단위별 커밋 |
| [create-pr](skills/create-pr/SKILL.md) | 본문 준비, 요청 범위의 push·Draft PR·CI 확인 |

`docs/skills/`는 배포 원본이고 `project/.agents/skills/`는 설치 위치입니다. 원본을 수정했다면 설치본도 비교·갱신합니다. 실제 동작 조건은 요구사항·계획·구현 명세를 따릅니다.

## CI 템플릿

[ci.yml](templates/ci.yml)을 Git 루트의 `.github/workflows/ci.yml`로 복사합니다. Git 루트에 `docs/`, `data/`, `project/`가 있는 구조를 기준으로 하며, `project`에서 모의 테스트와 Ruff 검사를 실행합니다.
