import httpx
from streamlit.testing.v1 import AppTest

from backend.config import PROJECT_ROOT
from frontend.api_client import ProductApi


def test_screen_uses_api_and_can_change_page(client, monkeypatch):
    def api_get(url, *, params, timeout):
        return client.get("/api/products", params=params)

    monkeypatch.setattr("frontend.api_client.httpx.get", api_get)
    app = AppTest.from_file(str(PROJECT_ROOT / "frontend" / "app.py")).run()
    assert not app.exception
    assert not app.error
    assert len(app.expander) == 20
    assert "뉴메릿 비타민C&D 메가" in app.expander[0].label
    app.number_input[0].set_value(3).run()
    assert not app.exception
    assert len(app.expander) == 4


def test_screen_handles_api_outage(monkeypatch):
    def unavailable(*args, **kwargs):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr("frontend.api_client.httpx.get", unavailable)
    app = AppTest.from_file(str(PROJECT_ROOT / "frontend" / "app.py")).run()
    assert not app.exception
    assert len(app.error) == 1
    assert "상품 목록을 불러오지 못했습니다" in app.error[0].value


def test_api_client_sends_pagination_and_timeout(monkeypatch):
    captured = {}

    def api_get(url, **kwargs):
        captured.update(url=url, **kwargs)
        return httpx.Response(
            200, json={"total": 0, "items": []}, request=httpx.Request("GET", url)
        )

    monkeypatch.setattr("frontend.api_client.httpx.get", api_get)
    assert ProductApi("http://example.test/").list_products(limit=10, offset=20)["total"] == 0
    assert captured == {
        "url": "http://example.test/api/products",
        "params": {"limit": 10, "offset": 20},
        "timeout": 10.0,
    }
