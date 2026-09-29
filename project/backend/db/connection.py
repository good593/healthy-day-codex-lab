import sqlite3
from pathlib import Path


def connect_database(path: Path, *, create: bool = False) -> sqlite3.Connection:
    """API는 존재하는 DB만 연다. 새 DB 생성은 초기화 명령에서만 허용한다."""
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
    mode = "rwc" if create else "rw"
    connection = sqlite3.connect(
        f"{path.resolve().as_uri()}?mode={mode}", uri=True, check_same_thread=False
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
