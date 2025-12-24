from functools import lru_cache
from os import environ
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    name: str = "App Name"
    version: str = "0.1"
    root_path: str = "/api/v1"
    DEBUG: bool = True

    # Application configuration
    env: str = environ.get("FASTAPI_ENV", "dev")

    GEMINI_API_KEY: str
    FIREBASE_CREDENTIALS_PATH: str

    SECRET_KEY: str

    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 9001

    CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:5173",
    ]

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=str(Path(__file__).parent.parent.parent / "docker" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
