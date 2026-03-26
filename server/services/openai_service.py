"""Azure OpenAI を利用した日報生成サービス。"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request


ALLOWED_IMAGE_TYPES = {
    "image/png": "png",
    "image/jpeg": "jpeg",
    "image/gif": "gif",
    "image/webp": "webp",
}


class UnsupportedImageFormatError(ValueError):
    """サポート対象外の画像形式。"""


@dataclass(frozen=True)
class AzureOpenAIServiceConfig:
    """Azure OpenAI 接続設定。"""

    api_key: str
    endpoint: str
    deployment: str
    api_version: str


class AzureOpenAIReportService:
    """スクリーンショット群から日報 Markdown を生成する。"""

    def __init__(self, config: AzureOpenAIServiceConfig) -> None:
        """サービスを初期化する。"""

        self._config = config

    def validate_image_format(self, content_type: str | None) -> str:
        """許可された画像形式かを検証して MIME タイプを返す。"""

        if content_type in ALLOWED_IMAGE_TYPES:
            return content_type

        invalid_format = content_type or "unknown"
        raise UnsupportedImageFormatError(
            f"サポートされていない画像形式です: {invalid_format}"
        )

    def encode_image(self, image_bytes: bytes) -> str:
        """画像バイト列を Base64 文字列に変換する。"""

        return base64.b64encode(image_bytes).decode("utf-8")

    def build_system_prompt(self) -> str:
        """日報生成用のシステムプロンプトを返す。"""

        return (
            "あなたは日報作成アシスタントです。\n"
            "ユーザーから提供されるPCの作業画面のスクリーンショットを分析し、\n"
            "以下の3セクション構成でマークダウン形式の日報を生成してください。\n\n"
            "## 作業内容\n"
            "- スクリーンショットから読み取れる具体的な作業内容を箇条書きで記述\n\n"
            "## 進捗状況\n"
            "- 作業の進捗に関する記述を箇条書きで記述\n\n"
            "## 課題・問題点\n"
            "- 発見された課題や問題点があれば箇条書きで記述（なければ「特になし」）\n\n"
            "注意事項:\n"
            "- 日本語で出力すること\n"
            "- 各セクションは箇条書き形式で記述すること\n"
            "- スクリーンショットから読み取れる情報のみに基づくこと\n"
            "- 個人情報や機密情報が含まれる場合は伏字にすること"
        )

    def generate_report(self, images: list[tuple[str, bytes]]) -> str:
        """複数画像を Azure OpenAI に送信して日報を生成する。"""

        contents: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": (
                    "添付したスクリーンショットをもとに、"
                    "マークダウン形式の日報を生成してください。"
                ),
            }
        ]

        try:
            for content_type, image_bytes in images:
                valid_content_type = self.validate_image_format(content_type)
                encoded_image = self.encode_image(image_bytes)
                contents.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{valid_content_type};base64,{encoded_image}"
                            )
                        },
                    }
                )

            response_body = self._request_chat_completion(contents)
            return self._extract_report(response_body)
        finally:
            contents.clear()

    def _request_chat_completion(
        self, contents: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Azure OpenAI Chat Completions API を呼び出す。"""

        endpoint = self._config.endpoint.rstrip("/")
        url = (
            f"{endpoint}/openai/deployments/{self._config.deployment}"
            f"/chat/completions?api-version={self._config.api_version}"
        )
        payload = {
            "messages": [
                {"role": "system", "content": self.build_system_prompt()},
                {"role": "user", "content": contents},
            ],
            "temperature": 0.2,
        }
        req = request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "api-key": self._config.api_key,
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.URLError as exc:  # pragma: no cover - 例外経路は main 側で確認
            raise RuntimeError("Azure OpenAI API の呼び出しに失敗しました") from exc

    def _extract_report(self, response_body: dict[str, Any]) -> str:
        """Chat Completions の応答から本文を抽出する。"""

        try:
            return response_body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Azure OpenAI API の応答形式が不正です") from exc
