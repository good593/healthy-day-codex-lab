from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.config import PROJECT_ROOT, Settings
from backend.db.seed import initialize_database
from backend.main import create_app


@pytest.fixture
def data_dir() -> Path:
    return PROJECT_ROOT.parent / "data"


@pytest.fixture
def database_path(tmp_path, data_dir) -> Path:
    path = tmp_path / "test.sqlite3"
    initialize_database(path, data_dir)
    return path


@pytest.fixture
def client(database_path):
    settings = Settings(_env_file=None, database_path=database_path, llm_provider="stub")
    with TestClient(create_app(settings)) as test_client:
        yield test_client
