import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ApiConfig:
    environment: str = field(
        default_factory=lambda: os.getenv("ENVIRONMENT", "development")
    )
    db_path: Path = field(
        default_factory=lambda: Path(os.getenv("TOURNAMENT_DB_PATH", "data/shogi.db"))
    )
    frontend_origins: tuple[str, ...] = field(
        default_factory=lambda: _get_default_origins(
            os.getenv("ENVIRONMENT", "development"),
            os.getenv("FRONTEND_ORIGINS"),
        )
    )
    admin_token: str = field(
        default_factory=lambda: os.getenv("ADMIN_TOKEN", "development-token")
    )


def _get_default_origins(
    environment: str, custom_origins: str | None
) -> tuple[str, ...]:
    """
    フロント許可オリジンを決定する.

    Args:
        environment: "development" or "production"
        custom_origins: カスタム環境変数（ある場合は優先）

    Returns:
        許可オリジンのタプル
    """
    if custom_origins:
        return _parse_origins(custom_origins)

    if environment == "production":
        # 本番環境: 明示的に指定されたオリジンのみ
        # Render.com の場合: https://myapp.render.com など
        return tuple()

    # 開発環境: ローカルホストのすべての主要ポート
    return _parse_origins(
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    )


def _parse_origins(raw: str) -> tuple[str, ...]:
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return tuple(origins)
