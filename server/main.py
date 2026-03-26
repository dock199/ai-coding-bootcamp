"""FastAPI アプリケーションのエントリポイント。"""

from __future__ import annotations

import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

try:  # pragma: no cover - 実行方法の違いを吸収するための分岐
    from .config import get_settings
    from .models.schemas import HealthResponse, ReportResponse
    from .services.openai_service import (
        AzureOpenAIReportService,
        AzureOpenAIServiceConfig,
        UnsupportedImageFormatError,
    )
except ImportError:  # pragma: no cover
    from config import get_settings
    from models.schemas import HealthResponse, ReportResponse
    from services.openai_service import (
        AzureOpenAIReportService,
        AzureOpenAIServiceConfig,
        UnsupportedImageFormatError,
    )


logger = logging.getLogger(__name__)
settings = get_settings()
service = AzureOpenAIReportService(
    AzureOpenAIServiceConfig(
        api_key=settings.azure_openai_api_key,
        endpoint=settings.azure_openai_endpoint,
        deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
    )
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """ヘルスチェック結果を返す。"""

    return HealthResponse(status="ok")


@app.post("/api/generate-report", response_model=ReportResponse)
async def generate_report(
    files: list[UploadFile] | None = File(default=None),
) -> ReportResponse:
    """アップロード画像から日報 Markdown を生成する。"""

    if not files:
        raise HTTPException(status_code=400, detail="画像ファイルが添付されていません")

    image_payloads: list[tuple[str, bytes]] = []
    try:
        for file in files:
            try:
                service.validate_image_format(file.content_type)
            except UnsupportedImageFormatError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

            image_payloads.append((file.content_type or "", await file.read()))

        report = service.generate_report(image_payloads)
        return ReportResponse(report=report)
    except HTTPException:
        raise
    except UnsupportedImageFormatError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("日報生成に失敗しました")
        raise HTTPException(
            status_code=500,
            detail="日報の生成に失敗しました。しばらくしてから再度お試しください",
        ) from exc
    finally:
        image_payloads.clear()
        if files:
            for file in files:
                await file.close()
