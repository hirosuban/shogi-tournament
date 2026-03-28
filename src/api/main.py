from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import ApiConfig
from .repository import TournamentRepository
from .service import TournamentService
from .types import TournamentDetail, TournamentFilters, TournamentSummary


def create_app(config: ApiConfig | None = None) -> FastAPI:
    settings = config or ApiConfig()
    service = TournamentService(TournamentRepository(settings.db_path))

    app = FastAPI(title="Shogi Tournaments API", version="0.1.0")

    # CORS 設定（環境別）
    if settings.environment == "development":
        # 開発環境: localhost のすべてのポートを許可
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.frontend_origins),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif settings.frontend_origins:
        # 本番環境かつ明示的にオリジンが指定されている場合のみ CORS 追加
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.frontend_origins),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # 本番環境で FRONTEND_ORIGINS が指定されていない場合は CORS ミドルウェアを追加しない
    # （フロント + バック が同一オリジンで動作するため）

    @app.get("/tournaments", response_model=list[TournamentSummary])
    def get_tournaments(
        prefecture: list[str] | None = Query(default=None),
        from_date: date | None = Query(default=None, alias="from"),
        to_date: date | None = Query(default=None, alias="to"),
        category: str | None = Query(default=None, min_length=1),
    ) -> list[TournamentSummary]:
        filters = TournamentFilters(
            prefectures=tuple(prefecture or ()),
            date_from=from_date,
            date_to=to_date,
            category=category,
        )
        return service.list_tournaments(filters)

    @app.get("/tournaments/{tournament_id}", response_model=TournamentDetail)
    def get_tournament_detail(tournament_id: int) -> TournamentDetail:
        tournament = service.get_tournament(tournament_id)
        if tournament is None:
            raise HTTPException(status_code=404, detail="Tournament not found")
        return tournament

    @app.post("/admin/trigger-scraper")
    def trigger_scraper(token: str | None = None) -> dict[str, str]:
        """
        スクレイパーを手動トリガー（GitHub Actions や外部スケジューラからの呼び出し用）.
        本番環境では ADMIN_TOKEN による認証が必須.
        """
        if settings.environment == "production":
            if not token or token != settings.admin_token:
                raise HTTPException(
                    status_code=403, detail="Invalid or missing admin token"
                )

        # スクレイパーロジックを実行
        try:
            from ..scraper.service import run_pipeline
            from ..scraper.config import CONFIG

            run_pipeline(config=CONFIG)
            return {"status": "success", "message": "Scraper triggered successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scraper error: {str(e)}")

    return app


app = create_app()
