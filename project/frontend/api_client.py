import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class ApiUnavailableError(Exception):
    pass


class ProductApi:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or os.getenv("API_BASE_URL", "http://127.0.0.1:8000")).rstrip("/")

    def list_products(self, *, limit: int = 50, offset: int = 0) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/products",
                params={"limit": limit, "offset": offset},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            raise ApiUnavailableError(
                "상품 목록을 불러오지 못했습니다. 잠시 후 다시 시도하세요."
            ) from exc
