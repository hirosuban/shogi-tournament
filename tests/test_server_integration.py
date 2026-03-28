"""Tests for server.py integration (frontend + backend)."""

import pytest
from fastapi.testclient import TestClient

from server import app
from src.api.config import ApiConfig


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


class TestIntegration:
    """統合テスト: フロント配信 + API."""

    def test_frontend_root(self, client):
        """ルート / がフロントエンド HTML を返す."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "首都圏 将棋大会スケジュール" in response.text

    def test_frontend_css(self, client):
        """CSS ファイルが配信可能."""
        response = client.get("/style.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_frontend_js(self, client):
        """JS ファイルが配信可能."""
        response = client.get("/app.js")
        assert response.status_code == 200

    def test_api_tournaments(self, client):
        """API エンドポイント /tournaments が動作."""
        response = client.get("/tournaments")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_api_with_filters(self, client):
        """フィルタ付きで API 呼び出し可能."""
        response = client.get(
            "/tournaments",
            params={"prefecture": "東京都", "from": "2026-03-01", "to": "2026-12-31"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_admin_trigger_scraper_development(self, client):
        """開発環境でスクレイパートリガーが認証なしで動作."""
        # 開発環境ではトークン不要
        response = client.post("/admin/trigger-scraper")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_cors_production_logic(self):
        """production config のロジックが正しい."""
        # _get_default_origins 関数の動作を検証
        from src.api.config import _get_default_origins

        # 本番環境・custom_origins なし → 空
        origins = _get_default_origins("production", None)
        assert origins == tuple()

        # 本番環境・custom_origins あり → custom を使用
        origins = _get_default_origins("production", "https://myapp.render.com")
        assert origins == ("https://myapp.render.com",)

        # 開発環境・custom_origins なし → localhost を許可
        origins = _get_default_origins("development", None)
        assert len(origins) > 0
        assert any("localhost" in o for o in origins)

    def test_development_config_allows_localhost(self):
        """開発環境（ENVIRONMENT=development）では localhost 許可."""
        dev_config = ApiConfig(environment="development")
        origins_str = ",".join(dev_config.frontend_origins)
        assert "localhost" in origins_str or "127.0.0.1" in origins_str
