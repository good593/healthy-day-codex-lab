# Codex 실습 문서

이번 과정은 기존 상품 조회 프로젝트에 **근거를 검색하고 출처를 표시하는 RAG 상담 첫 버전**을 추가합니다. 2장에서 규칙·설정, 3장에서 요구사항, 4장에서 구현 계획을 정리하고 5장에서 구현·검증·커밋·PR까지 완료합니다.

## 읽는 순서

| 문서 | 읽을 부분 | 역할 |
| --- | --- | --- |
| [요구사항정의서.xlsx](요구사항정의서.xlsx) | `Codex_실습범위` | 이번 과정의 범위와 원문 요구사항 연결 |
| [데이터 정의서.xlsx](<데이터 정의서.xlsx>) | 기존 CSV 시트, `RAG_문서`, `RAG_API` | 시작 데이터와 추가할 문서·API 계약 |
| [실습 보완 명세](<실습 보완 명세.md>) | 전체 | 공통 구현·검증 계약 |
| [RAG 상담 요구사항 초안](<RAG 상담 요구사항 초안.md>) | 결정할 질문 | grill-me 인터뷰의 출발점 |
| [강사 진행 가이드](<강사 진행 가이드.md>) | 사전 준비·장별 산출물 | 저장소·문서·계정 준비와 검수 |
| [합성 테스트 자료](fixtures/README.md) | RAG 자료 | API 키 없이 검색·실패 경로 재현 |

기존 Excel 시트의 서비스 요구사항과 CSV 정의는 유지했습니다. `tmp_` 파일은 수정 전 원본입니다. 원문의 수용 O가 곧 이번 강의의 필수 구현을 뜻하지 않습니다. 이번 범위는 `Codex_실습범위`와 실습 보완 명세로 확인합니다.

## 학생이 만드는 문서

템플릿을 읽고 학생의 `project/docs/`에 실제 결정과 결과를 작성합니다. 대괄호는 실제 값으로 바꾸며, 비어 있는 기록을 완료 증거로 제출하지 않습니다.

- [요구사항 템플릿](templates/rag-requirements.md) → `project/docs/requirements/rag-chatbot.md`
- [계획 템플릿](templates/rag-plan.md) → `project/docs/plans/rag-chatbot.md`
- [PR 본문 템플릿](templates/pr-body.md) → `project/docs/pr/rag-chatbot.md`
- [검증·리뷰 기록 템플릿](templates/change-review.md) → `project/docs/reports/rag-review.md`

MCP·Skill 제작·예약 작업의 일반 설명은 [Work 강의](<../../1. Work/README.md>)를 참고합니다. Codex 3장에서는 기존 find-skills와 grill-me를 실제 요구사항 작업에 사용합니다.
