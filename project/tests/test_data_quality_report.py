import csv
import hashlib
import shutil
from pathlib import Path

from scripts.data_quality_report import build_report


def hashes(folder: Path) -> dict:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob("*.csv")}


def test_report_preserves_sources_and_reports_known_blanks(data_dir):
    before = hashes(data_dir)
    report, success = build_report(data_dir)
    assert success
    assert "행 수: 44" in report
    assert "행 수: 54" in report
    assert "행 수: 228" in report
    assert "상한섭취량: 72" in report
    assert "섭취시주의사항: 1" in report
    assert hashes(data_dir) == before


def test_missing_input_is_failure_not_empty_success(tmp_path):
    report, success = build_report(tmp_path)
    assert not success
    assert report.count("결과: 실패") == 4


def test_duplicate_product_id_is_failure(tmp_path, data_dir):
    copied = tmp_path / "data"
    shutil.copytree(data_dir, copied)
    path = copied / "상품마스터.csv"
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))
    rows.append(rows[1])
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        csv.writer(file).writerows(rows)
    report, success = build_report(copied)
    assert not success
    assert "상품ID 중복: 1" in report
