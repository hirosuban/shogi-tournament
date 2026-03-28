"""
統合サーバー: FastAPI + 静的フロントエンド

開発環境:
    python server.py
    または: uvicorn server:app --reload --host 0.0.0.0 --port 8000

本番環境（Render.com など）:
    ENVIRONMENT=production uvicorn server:app --host 0.0.0.0 --port 8000
"""

from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.main import create_app

# API アプリ作成
app: FastAPI = create_app()

# フロントエンド静的ファイルをマウント
# NOTE: この行の後に app.mount() を呼ぶたびに、ルートが更新される
# 複数の mount は避け、通常はこれが最後に配置される
frontend_path = Path(__file__).parent / "src" / "frontend"
if frontend_path.exists():
    app.mount(
        "/",
        StaticFiles(directory=frontend_path, html=True),
        name="frontend",
    )


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
