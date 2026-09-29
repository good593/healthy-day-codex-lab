import sqlite3
from contextlib import closing

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.api.products import router
from backend.config import Settings
from backend.db.connection import connect_database


def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(title="건강한하루 실습 API", version="0.1.0")
    app.state.settings = settings or Settings()
    app.include_router(router, prefix="/api")

    @app.exception_handler(sqlite3.OperationalError)
    async def database_error_handler(request, exc):
        return JSONResponse(
            status_code=503,
            content={"detail": "DB 상태를 확인하세요. 초기화가 필요할 수 있습니다."},
        )

    @app.get("/health", tags=["health"])
    def health():
        with closing(connect_database(app.state.settings.database_path)) as connection:
            row = connection.execute("SELECT COUNT(*) FROM products").fetchone()
        return {"status": "ok", "products": row[0]}

    return app


app = create_app()
