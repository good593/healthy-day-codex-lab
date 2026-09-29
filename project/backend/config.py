"""환경 설정. 상대 경로는 실행 위치가 아닌 project 폴더를 기준으로 해석한다."""

from pathlib import Path
from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    data_dir: Path = PROJECT_ROOT.parent / "data"
    database_path: Path = PROJECT_ROOT / "var" / "healthy_day.sqlite3"
    llm_provider: Literal["stub", "groq"] = "stub"
    groq_api_key: SecretStr = SecretStr("")
    groq_model: str = ""

    @field_validator("data_dir", "database_path", mode="before")
    @classmethod
    def resolve_path(cls, value: str | Path) -> Path:
        path = Path(value)
        return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()
