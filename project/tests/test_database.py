import csv
import shutil
import sqlite3
from contextlib import closing

import pytest

from backend.config import PROJECT_ROOT, Settings
from backend.db.connection import connect_database
from backend.db.seed import DATASETS, initialize_database


def test_all_csv_rows_are_imported_once(database_path, data_dir):
    counts = initialize_database(database_path, data_dir)
    for filename, table, _ in DATASETS:
        with (data_dir / filename).open(encoding="utf-8-sig", newline="") as file:
            expected = len(list(csv.DictReader(file)))
        assert counts[table] == expected


def test_seed_does_not_overwrite_existing_work(database_path, data_dir):
    with closing(connect_database(database_path)) as connection, connection:
        connection.execute(
            "UPDATE products SET name = ? WHERE product_id = ?", ("수정 상품", "P001")
        )
    initialize_database(database_path, data_dir)
    with closing(connect_database(database_path)) as connection:
        assert (
            connection.execute("SELECT name FROM products WHERE product_id = 'P001'").fetchone()[0]
            == "수정 상품"
        )


def test_missing_and_qualified_upper_limits_are_preserved(database_path):
    with closing(connect_database(database_path)) as connection:
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM intake_references WHERE upper_limit IS NULL"
            ).fetchone()[0]
            == 72
        )
        rows = connection.execute(
            "SELECT upper_limit FROM intake_references WHERE upper_limit_raw = '350(보충제)'"
        ).fetchall()
        assert rows and all(row[0] == 350 for row in rows)
        assert (
            connection.execute(
                "SELECT COUNT(*) FROM products WHERE precautions IS NULL"
            ).fetchone()[0]
            == 1
        )


def test_failed_import_rolls_back_all_records(tmp_path, data_dir):
    copied_data = tmp_path / "data"
    shutil.copytree(data_dir, copied_data)
    products_path = copied_data / "상품마스터.csv"
    with products_path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))
    rows.append(rows[1])  # 기본키 중복으로 초기 적재 실패를 재현한다.
    with products_path.open("w", encoding="utf-8-sig", newline="") as file:
        csv.writer(file).writerows(rows)
    database_path = tmp_path / "broken.sqlite3"
    with pytest.raises(sqlite3.IntegrityError):
        initialize_database(database_path, copied_data)
    with closing(connect_database(database_path)) as connection:
        for table in ("products", "nutrient_functions", "intake_references", "seed_history"):
            assert connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0


def test_relative_database_path_is_independent_of_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings = Settings(_env_file=None, database_path="var/example.sqlite3")
    assert settings.database_path == PROJECT_ROOT / "var" / "example.sqlite3"
