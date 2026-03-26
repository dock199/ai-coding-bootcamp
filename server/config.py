"""FastAPI サーバー向け設定管理。"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")


@dataclass(frozen=True)
class Settings:
    """Azure OpenAI 接続設定。"""

    azure_openai_api_key: str = getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_deployment: str = getenv("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_api_version: str = getenv(
        "AZURE_OPENAI_API_VERSION", "2024-12-01-preview"
    )


@lru_cache
def get_settings() -> Settings:
    """設定値をキャッシュして返す。"""

    return Settings()
