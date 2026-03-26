"""API レスポンススキーマ。"""

from pydantic import BaseModel


class ReportResponse(BaseModel):
    """日報生成レスポンス。"""

    report: str


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス。"""

    status: str
