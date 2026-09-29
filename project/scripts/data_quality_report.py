"""7~8장용 CSV 구조 점검. 원본과 DB를 변경하지 않고 Markdown 보고서를 만든다."""

import argparse
import csv
import hashlib
from datetime import UTC, datetime
from pathlib import Path

from backend.config import PROJECT_ROOT
from backend.db.seed import DATASETS


def build_report(data_dir: Path) -> tuple[str, bool]:
    lines = [
        "# CSV 데이터 품질 점검",
        "",
        f"점검 시각(UTC): {datetime.now(UTC).isoformat(timespec='seconds')}",
        "",
        "CSV 구조와 빈 값만 확인합니다. 출처의 정확성·최신성 검증이나 데이터 갱신이 아닙니다.",
    ]
    success = True
    for filename, _, mapping in DATASETS:
        lines.extend(["", f"## {filename}", ""])
        path = data_dir / filename
        try:
            raw = path.read_bytes()
            with path.open(encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames or []
                rows = list(reader)
            if len(headers) != len(set(headers)) or set(headers) != set(mapping):
                raise ValueError("컬럼 구성이 정의와 다릅니다.")
            if any(None in row or any(v is None for v in row.values()) for row in rows):
                raise ValueError("데이터 행의 컬럼 수가 다릅니다.")
            if not rows:
                raise ValueError("데이터 행이 없습니다.")
        except (OSError, UnicodeError, csv.Error, ValueError) as exc:
            success = False
            # OS 오류의 경로나 환경 정보 대신 오류 분류만 보고한다.
            detail = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
            lines.append(f"- 결과: 실패 ({detail})")
            continue
        lines.extend(
            [
                "- 결과: 구조 점검 완료",
                f"- 행 수: {len(rows)}",
                f"- SHA-256: `{hashlib.sha256(raw).hexdigest()}`",
                "- 빈 값 (0과 구분하며, 빈 값이 모두 오류라는 뜻은 아닙니다):",
            ]
        )
        blanks = {key: sum(not row[key].strip() for row in rows) for key in headers}
        for key, count in blanks.items():
            if count:
                lines.append(f"  - {key}: {count}")
        if not any(blanks.values()):
            lines.append("  - 없음")
        if "상품ID" in headers:
            duplicates = len(rows) - len({row["상품ID"] for row in rows})
            empty_ids = blanks["상품ID"]
            lines.append(f"- 상품ID 중복: {duplicates}, 누락: {empty_ids}")
            if duplicates or empty_ids:
                success = False
                lines.append("- 결과: 실패 (상품ID 유일성 또는 필수값 위반)")
    lines.extend(["", f"전체 실행 결과: {'완료' if success else '실패'}", ""])
    return "\n".join(lines), success


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=PROJECT_ROOT.parent / "data")
    parser.add_argument(
        "--output", type=Path, default=PROJECT_ROOT / "docs" / "reports" / "data-quality.md"
    )
    args = parser.parse_args()
    data_dir = args.data_dir.resolve()
    output = args.output.resolve()
    # 원본 데이터 폴더에 보고서를 써서 입력을 덮어쓰는 것을 막는다.
    if output == data_dir or data_dir in output.parents:
        parser.error("보고서는 입력 data 폴더 밖에 저장하세요.")
    report, success = build_report(data_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"보고서: {output}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
