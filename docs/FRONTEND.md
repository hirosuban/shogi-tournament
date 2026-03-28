# FRONTEND.md

フロントエンド固有のガイドラインと規約を定義します。

> 詳細な設計判断は [`docs/design-docs/`](./design-docs/index.md) を参照してください。

---

## フレームワーク・ライブラリ

- 生HTML + Vanilla JS
- Leaflet.js（CDN読み込み）
- 都道府県GeoJSON（`src/frontend/data/shutoken.geojson`）

---

## ディレクトリ構造

```
src/frontend/
├── index.html
├── style.css
├── app.js
└── data/
	└── shutoken.geojson
```

---

## 状態管理方針

- グローバル状態は最小限に保つ
- 管理対象は「選択中都道府県」「日付レンジ」のみ
- サーバー状態（大会一覧）はフィルタ変更時にAPI再取得し、常に単一の表示状態を描画する

---

## UI実装規約

- Leafletのポリゴンクリックで都道府県フィルタをトグルする
- 日付は `<input type="date">` を2つ使い、`from`/`to` クエリとしてAPIへ送る
- ローディング・エラー・0件表示の3状態を常に明示する
- APIレスポンスの文字列は `textContent` でDOMに挿入する

## ローカル起動

1. API: `uv run python -m src.api`
2. フロント: `cd src/frontend && python3 -m http.server 5173`
3. ブラウザで `http://localhost:5173` を開く

---

## パフォーマンス要件

- 重要ユーザージャーニーのいずれのスパンも 2 秒を超えない
- バンドルサイズは定期的に監視する
- 画像は遅延読み込みを標準とする

---

## アクセシビリティ

- すべてのインタラクティブ要素はキーボード操作可能にする
- `aria-label` を適切に設定する
- カラーコントラスト比は WCAG AA 基準（4.5:1）を満たす
