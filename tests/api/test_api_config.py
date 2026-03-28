from src.api.config import ApiConfig


def test_default_frontend_origins_include_localhost_and_127(monkeypatch) -> None:
    monkeypatch.delenv("FRONTEND_ORIGINS", raising=False)

    config = ApiConfig()

    assert "http://localhost:5173" in config.frontend_origins
    assert "http://127.0.0.1:5173" in config.frontend_origins
