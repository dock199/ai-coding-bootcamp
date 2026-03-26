"""Azure OpenAI 連携サービスのテスト。"""

import json

from server.services.openai_service import (
    AzureOpenAIReportService,
    AzureOpenAIServiceConfig,
)


def create_service() -> AzureOpenAIReportService:
    """テスト用サービスを生成する。"""

    return AzureOpenAIReportService(
        AzureOpenAIServiceConfig(
            api_key="test-key",
            endpoint="https://example.openai.azure.com/",
            deployment="gpt-4.1",
            api_version="2024-12-01-preview",
        )
    )


def test_encode_image_returns_base64_text() -> None:
    """Base64 エンコード結果を確認する。"""

    service = create_service()

    assert service.encode_image(b"hello") == "aGVsbG8="


def test_build_system_prompt_contains_required_sections() -> None:
    """システムプロンプトに必要な 3 セクションが含まれることを確認する。"""

    service = create_service()
    prompt = service.build_system_prompt()

    assert "## 作業内容" in prompt
    assert "## 進捗状況" in prompt
    assert "## 課題・問題点" in prompt


def test_generate_report_calls_chat_completions_api(monkeypatch) -> None:
    """API 呼び出し結果から日報本文を抽出することを確認する。"""

    service = create_service()

    def mock_request_chat_completion(contents):
        assert contents[0]["type"] == "text"
        assert contents[1]["type"] == "image_url"
        assert contents[1]["image_url"]["url"].startswith(
            "data:image/png;base64,aGVsbG8="
        )
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "report": "## 作業内容\n- 実装",
                            }
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr(service, "_request_chat_completion", mock_request_chat_completion)

    report = service.generate_report([("image/png", b"hello")])

    assert report == json.dumps({"report": "## 作業内容\n- 実装"})
