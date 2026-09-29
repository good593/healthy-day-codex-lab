import sqlite3
from collections.abc import Iterator

from fastapi import Depends, HTTPException, Request

from backend.db.connection import connect_database
from backend.repositories.products import ProductRepository
from backend.services.products import ProductService


def get_connection(request: Request) -> Iterator[sqlite3.Connection]:
    try:
        connection = connect_database(request.app.state.settings.database_path)
    except sqlite3.OperationalError as exc:
        raise HTTPException(503, "DB를 열 수 없습니다. DB 초기화와 경로를 확인하세요.") from exc
    try:
        yield connection
    finally:
        connection.close()


def get_product_service(connection=Depends(get_connection)) -> ProductService:
    return ProductService(ProductRepository(connection))
