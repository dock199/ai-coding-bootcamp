"""FastAPI エンドポイントのテスト。"""

from fastapi.testclient import TestClient

from server import main


client = TestClient(main.app)


def test_health_check_returns_ok() -> None:
    """ヘルスチェックが正常応答を返すことを確認する。"""

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_report_without_files_returns_400() -> None:
    """画像なしリクエストは 400 を返すことを確認する。"""

    response = client.post("/api/generate-report")

    assert response.status_code == 400
    assert response.json() == {"detail": "画像ファイルが添付されていません"}


def test_generate_report_with_unsupported_format_returns_400() -> None:
    """不正な画像形式は 400 を返すことを確認する。"""

    response = client.post(
        "/api/generate-report",
        files=[("files", ("notes.txt", b"hello", "text/plain"))],
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "サポートされていない画像形式です: text/plain"
    }


def test_generate_report_returns_report_when_service_succeeds(monkeypatch) -> None:
    """正常系で日報テキストを返すことを確認する。"""

    def mock_generate_report(images: list[tuple[str, bytes]]) -> str:
        assert len(images) == 1
        assert images[0][0] == "image/png"
        assert images[0][1] == b"png-bytes"
        return "## 作業内容\n- 実装\n\n## 進捗状況\n- 順調\n\n## 課題・問題点\n- 特になし"

    monkeypatch.setattr(main.service, "generate_report", mock_generate_report)

    response = client.post(
        "/api/generate-report",
        files=[("files", ("screen.png", b"png-bytes", "image/png"))],
    )

    assert response.status_code == 200
    assert response.json() == {
        "report": "## 作業内容\n- 実装\n\n## 進捗状況\n- 順調\n\n## 課題・問題点\n- 特になし"
    }
