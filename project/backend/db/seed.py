"""배포 CSV의 초기 적재. 원본 파일과 기존 레코드를 덮어쓰지 않는다."""

import csv
import math
import re
from contextlib import closing
from pathlib import Path

from backend.db.connection import connect_database

# 아래 매핑은 배포된 데이터 정의서의 항목명을 그대로 사용한다.
PRODUCT_FIELDS = dict(
    zip(
        [
            "상품ID",
            "상품명",
            "업소명",
            "카테고리",
            "검색키워드(주요원료)",
            "관련_증상",
            "신고번호",
            "등록일자",
            "소비기한",
            "성상",
            "섭취량_섭취방법",
            "섭취시주의사항",
            "기능성_내용",
            "신고번호_상세조회URL",
            "데이터출처",
        ],
        [
            "product_id",
            "name",
            "manufacturer",
            "category",
            "ingredient_keyword",
            "concern",
            "report_number",
            "registered_on",
            "shelf_life",
            "appearance",
            "intake_method",
            "precautions",
            "functionality",
            "source_url",
            "data_source",
        ],
        strict=True,
    )
)
FUNCTION_FIELDS = dict(
    zip(
        [
            "영양소",
            "분류",
            "기능성",
            "관련_증상",
            "키워드",
            "근거_수준",
            "근거_설명",
            "신뢰도",
            "출처",
            "출처_URL",
        ],
        [
            "nutrient",
            "category",
            "functionality",
            "concern",
            "keyword",
            "evidence_level",
            "evidence_description",
            "reliability",
            "source",
            "source_url",
        ],
        strict=True,
    )
)
INTAKE_FIELDS = dict(
    zip(
        [
            "영양소",
            "연령대",
            "성별",
            "임신여부",
            "수유여부",
            "권장섭취량",
            "충분섭취량",
            "상한섭취량",
            "단위",
            "출처",
            "기관",
            "비고",
            "출처_URL",
        ],
        [
            "nutrient",
            "age_group",
            "sex",
            "pregnancy",
            "lactation",
            "recommended",
            "adequate",
            "upper_limit",
            "unit",
            "source",
            "organization",
            "note",
            "source_url",
        ],
        strict=True,
    )
)
DATASETS = (
    ("상품마스터.csv", "products", PRODUCT_FIELDS),
    ("영양소_기능성_추천DB_확장판.csv", "nutrient_functions", FUNCTION_FIELDS),
    ("영양소별_권장섭취량_확장판_한글.csv", "intake_references", INTAKE_FIELDS),
)


def read_records(path: Path, fields: dict[str, str]) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if set(reader.fieldnames or []) != set(fields):
            raise ValueError(f"{path.name}: CSV 컬럼이 데이터 정의와 다릅니다.")
        records = []
        for line, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{path.name}:{line}: 컬럼 수를 확인하세요.")
            record = {target: row[source].strip() or None for source, target in fields.items()}
            if "upper_limit" in record:
                # '350(보충제)'의 조건을 잃지 않도록 원문과 수치를 별도로 보존한다.
                record["upper_limit_raw"] = record["upper_limit"]
                raw = record["upper_limit"]
                if raw is not None and raw.endswith("(보충제)"):
                    if not re.fullmatch(r"\d+(?:\.\d+)?\(보충제\)", raw):
                        raise ValueError(f"{path.name}:{line}: 상한섭취량 형식을 확인하세요.")
                    record["upper_limit"] = raw.removesuffix("(보충제)")
            for key in ("recommended", "adequate", "upper_limit"):
                if key in record and record[key] is not None:
                    value = float(record[key])
                    if not math.isfinite(value) or value < 0:
                        raise ValueError(f"{path.name}:{line}: 유효하지 않은 수치입니다.")
                    record[key] = value
            records.append(record)
    if not records:
        raise ValueError(f"{path.name}: 데이터가 없습니다.")
    return records


def initialize_database(database_path: Path, data_dir: Path) -> dict[str, int]:
    """원본의 누락값은 NULL로 보존한다. 초기 적재는 하나의 트랜잭션이다."""
    datasets = [(table, read_records(data_dir / name, fields)) for name, table, fields in DATASETS]
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    with closing(connect_database(database_path, create=True)) as connection:
        connection.executescript(schema)
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            seeded = connection.execute(
                "SELECT 1 FROM seed_history WHERE seed_name = ?", ("starter-v1",)
            ).fetchone()
            if not seeded:
                for table, records in datasets:
                    columns = ", ".join(records[0])
                    placeholders = ", ".join("?" for _ in records[0])
                    # 테이블/컬럼 이름은 위의 내부 상수에서만 가져온다.
                    connection.executemany(
                        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                        [tuple(record.values()) for record in records],
                    )
                connection.execute(
                    "INSERT INTO seed_history (seed_name) VALUES (?)", ("starter-v1",)
                )
        return {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for _, table, _ in DATASETS
        }
