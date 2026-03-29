# Phase 6: 完全静的化（Render Web Service → Static Site）

## 目標

サーバープロセスを廃止し、フロントエンドを完全な静的サイトとして配信する。
Render 無料プランのスリープ問題を根本的に解消する。

## 背景・動機

Render 無料プランの Web Service は約15分間アクセスがないとスリープし、復帰に数十秒かかる。
大会データは約86件と小規模であり、サーバーサイドでの動的クエリは不要。
全データを静的 JSON として配信し、クライアントサイドでフィルタリングする構成に変更する。

## アプローチ

- スクレイパーを SQLite 経由から直接 JSON 出力に変更
- フロントエンドを API 呼び出しからローカル JSON 読み込み + クライアントサイドフィルタリングに変更
- Render の設定を Web Service → Static Site に切り替え
- `server.py` / `src/api/` / `src/scraper/repository.py` / SQLite 関連コードを削除
- `data/shogi.db` をリポジトリから削除

## タスク

### Phase A: エージェントが実行すること

- [ ] `src/scraper/` を JSON 直接出力に変更
  - `repository.py` を削除（SQLite 操作不要）
  - `service.py`: `run_pipeline()` を修正。`migrate` / `upsert` → JSON 書き出しに変更
  - `config.py`: `db_path` → `output_path` (`src/frontend/data/tournaments.json`) に変更
  - 出力: 全フィールド（`source_url` 含む）、`date` 昇順ソート、compact JSON
- [ ] `.github/workflows/scraper-schedule.yml` を更新
  - コミット対象を `data/shogi.db` → `src/frontend/data/tournaments.json` に変更
- [ ] `src/frontend/app.js` を書き換え
  - `buildQueryParams()` / `fetchAndRenderTournaments()` を削除
  - `loadTournaments()`: 初回に JSON を fetch してキャッシュ
  - `filterAndRenderTournaments()`: キャッシュデータをクライアントサイドでフィルタ
  - 全呼び出し元を `filterAndRenderTournaments()` に置換
- [ ] `render.json` を Static Site 用に変更
- [ ] 削除対象:
  - `server.py`
  - `src/api/` ディレクトリ
  - `src/scraper/repository.py`
  - `data/shogi.db`
  - 関連テスト
- [ ] `pyproject.toml` から不要な依存を整理（`fastapi`, `uvicorn` 等）
- [ ] 初期 `tournaments.json` を生成してコミット

### Phase B: 人間が実施すること

- [ ] Render ダッシュボードで Web Service → Static Site に切り替え（または旧サービス削除 → 新規 Static Site 作成）
  - Publish directory: `src/frontend`
- [ ] 本番 URL でアプリが表示されることを確認
- [ ] フィルタ・地図が正常に動作することを目視確認

## 意思決定ログ

- JSON 形式: 単一フラットな配列。データ量が小さいため分割不要。`source_url` も含めることで将来のリンク対応が容易
- フィルタリング: 全件をクライアントサイドでフィルタ。86件程度なら一瞬で完了し、サーバー往復より高速
- API コード: 削除する。ローカル確認は `python -m http.server` で十分。必要時は git 履歴から復元可能
- SQLite 廃止: ソースページが毎回全件返すため、重複排除・データ蓄積は不要。スクレイパーが直接 JSON を出力する構成に簡素化

## 完了条件

- 本番 URL で静的サイトとして配信されている（サーバープロセスなし）
- スリープせず即座にページが表示される
- 地図クリック・日付フィルタが正常に動作する
- GitHub Actions でスクレイパー実行後に `tournaments.json` が自動更新される
