import pytest
from fastapi.testclient import TestClient

from backend.config import Settings
from backend.main import create_app


def test_health_and_product_pagination(client):
    assert client.get("/health").json() == {"status": "ok", "products": 44}
    first = client.get("/api/products", params={"limit": 2}).json()
    second = client.get("/api/products", params={"limit": 2, "offset": 2}).json()
    assert first["total"] == second["total"] == 44
    assert [p["product_id"] for p in first["items"]] == ["P001", "P002"]
    assert [p["product_id"] for p in second["items"]] == ["P003", "P004"]
    assert client.get("/api/products", params={"offset": 1000}).json()["items"] == []


def test_detail_and_unknown_product(client):
    response = client.get("/api/products/P001")
    assert response.status_code == 200
    assert response.json()["name"] == "뉴메릿 비타민C&D 메가"
    assert client.get("/api/products/unknown").status_code == 404
    assert client.get("/api/products/' OR 1=1 --").status_code == 404


@pytest.mark.parametrize("query", [{"limit": 0}, {"limit": 101}, {"offset": -1}])
def test_invalid_pagination_is_rejected(client, query):
    assert client.get("/api/products", params=query).status_code == 422


def test_missing_database_has_actionable_error(tmp_path):
    path = tmp_path / "not-created.sqlite3"
    settings = Settings(_env_file=None, database_path=path)
    with TestClient(create_app(settings)) as client:
        assert client.get("/api/products").status_code == 503
        assert client.get("/health").status_code == 503
    assert not path.exists()
