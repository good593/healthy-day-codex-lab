---
name: create-pr
description: 기능 브랜치의 실제 변경과 검증 기록으로 PR 본문을 준비하거나 요청에 따라 push·Draft PR 생성·CI 확인을 진행할 때 사용한다. 기존 PR의 상태 확인과 본문 갱신도 지원한다.
---

# 검증 근거가 있는 PR 전달

요청 범위를 준비, 게시, 상태 확인으로 해석한다. 본문 준비 요청은 로컬 파일 작성까지, 게시 요청은 지정한 원격에 push·Draft PR 생성까지, 상태 확인은 PR·CI 읽기까지 수행한다. 기존에 받은 명확한 게시 권한을 다시 묻지 않는다.

## 입력과 프로젝트 경로

- 입력: 대상 저장소·remote, base/head, 요구사항·계획, 전체 검증·리뷰 기록, PR 본문 경로와 요청 범위.
- 프로젝트 저장소의 `origin`, base `main`, head `feat/rag-chatbot`을 기본으로 사용하되 실제 대상과 현재 요청을 확인한다.
- `project` 기준 요구사항·계획은 `docs/requirements/rag-chatbot.md`, `docs/plans/rag-chatbot.md`, 전체 검증은 `docs/reports/rag-validation.md`, 리뷰 기록은 `docs/reports/rag-review.md`다.
- 본문 템플릿은 `../docs/templates/pr-body.md`, 출력은 `docs/pr/rag-chatbot.md`다. 다른 프로젝트에서는 실제 템플릿·경로를 따른다.

## 절차

1. 적용 지침·요구사항·계획을 읽고 Git 루트·remote·현재 브랜치·base/head를 확인한다. `gh auth status`, `gh repo view --json nameWithOwner,url,defaultBranchRef`로 실제 GitHub 대상을 확인한다. 본문만 준비할 때 GitHub 접근이 불가능하면 로컬 확인 결과와 게시 시 확인할 대상을 남겨 작업을 계속한다. 상태 조회만 요청받았다면 기존 PR을 확인하고 9번과 완료 보고만 수행한다. 본문 작성·검증 갱신·커밋·push·PR 수정은 수행하지 않는다.
2. `base...HEAD`의 커밋과 전체 diff, staged/unstaged 변경과 새 파일을 확인한다. 브랜치에 작업 범위와 무관한 커밋이 섞였는지, 미커밋 기능이 본문에 포함되는지 확인한다. 준비 단계에서 미커밋 전달 문서를 작성할 수 있지만 실제 게시 전에는 PR에 필요한 변경·문서를 커밋해야 한다. 검증한 작업 트리의 소스·테스트·설정이 게시할 HEAD의 내용과 같은지도 확인한다. 다른 작업의 미커밋 변경을 자동으로 포함하지 않는다.
3. 전체 검증 기록의 포함 경로/제외 규칙으로 파일 목록·SHA256을 재수집한다. 변경·추가·삭제된 검사 대상이나 기준 변경이 있으면 필요한 재검증을 알린다. 검증이 현재 상태에 유효하지 않거나 필수 검사가 실패했으면 게시하지 않는다. 검증까지 요청받은 경우에는 필요한 검사를 갱신할 수 있다. 모의 테스트 통과, 실제 Groq 미실행, 공식 자료 미준비를 각각 표시한다. 계획에서 허용한 실제 호출 미실행은 공개하고 Draft PR로 전달할 수 있다.
4. 리뷰의 판단·수정·재검증 기록을 확인한다. 요청된 리뷰를 하지 못했다면 그 상태를 표시한다. 사용자 문제와 변경 후 동작을 먼저 쓰고 관련 요구사항ID·주요 결정·실제 테스트/Ruff/수동/외부 호출 결과·남은 사항을 템플릿에 작성한다. diff에 없는 기능·실행하지 않은 검증·과거 코드의 결과를 최종 완료로 쓰지 않는다. 비밀값·질문 원문·상담 내용은 포함하지 않는다.
5. 준비 요청이면 본문 파일·제안 제목·base/head·미완료 사항을 보여주고 끝낸다. 본문·검증/리뷰 기록을 커밋할 필요가 있으면 그 후보도 보고한다. 이 스킬이 자동으로 커밋하거나 게시하지 않는다.
6. 게시 요청이면 검토한 본문과 필요한 전달 문서가 커밋되었는지 확인한다. 본문이 달라졌다면 차이를 보고한다. `gh pr list --head <head> --base <base> --state open --json number,url,headRefName,baseRefName`으로 기존 PR을 찾아 중복 생성을 막는다. `origin`과 `gh` 대상이 다르거나 base/head가 불명확하면 대상이 확정되기 전까지 게시하지 않는다.
7. 허용된 feature 브랜치를 일반 push한다. 실패하면 원인을 보고하며 강제 push·base 브랜치 직접 push·자동 병합으로 우회하지 않는다. 새 PR은 Draft로 생성하고 `--body-file`로 파일의 실제 줄바꿈을 보존한다. 아래는 이 프로젝트의 예시다.

   ```powershell
   git push -u origin feat/rag-chatbot
   gh pr create --base main --head feat/rag-chatbot --draft --title "feat: add grounded RAG consultation" --body-file docs/pr/rag-chatbot.md
   gh pr view --json url,baseRefName,headRefName,headRefOid,isDraft
   gh pr checks
   ```

8. 기존 PR이면 그 URL을 사용한다. 후속 변경을 push하거나 본문을 갱신하라는 요청이 있으면 그 범위에서만 처리하고, 상태 확인만 요청받았다면 push나 본문 수정 없이 읽는다. `gh`가 없거나 접근 권한이 없으면 준비한 본문과 웹에서 수행할 절차를 제공하고 PR 생성은 미완료로 보고한다.
9. PR의 URL·base/head·현재 head 커밋을 확인하고 그 커밋의 CI 결과·실행 링크를 기록한다. pending·실패·검사 없음·조회 불가를 성공과 구분한다. CI 실패는 job/로그와 로컬 환경 차이를 보고하며 수정은 별도 구현 요청으로 연결한다. 게시 응답이 불명확하면 기존 PR과 원격 상태를 조회한 후에만 재시도한다.

## 완료 보고

본문 경로, PR URL 또는 미생성 이유, base/head·head 커밋, 실제 CI 상태·링크, 리뷰와 실제 호출의 남은 항목을 보고한다. Draft 해제·리뷰 요청 메시지·병합은 별도 요청 범위로 둔다.
