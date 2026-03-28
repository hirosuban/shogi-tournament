# AGENTS.md

このファイルはエージェントへの **マップ** です。百科事典ではありません。
詳細は各リンク先の信頼できる情報源を参照してください。

---

## このリポジトリについて

個人プロダクトのソースコードを管理するリポジトリです。
アプリケーションロジック・インフラ・ドキュメント・内部ツールをすべてこのリポジトリで管理します。

> **原則**: エージェントの実行時コンテキスト内でアクセスできないものは、存在しないも同然です。
> Slack のスレッド・Google Docs・人間の暗黙知は参照できません。
> すべての重要な知識はこのリポジトリ内にバージョン管理されたアーティファクトとして存在しなければなりません。

---

## ナビゲーション

### アーキテクチャ
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — ドメイン構造・パッケージ階層・依存関係ルールのトップレベルマップ

### ドキュメント
| ファイル | 内容 |
|---|---|
| [`docs/DESIGN.md`](./docs/DESIGN.md) | デザイン原則・ビジュアルガイドライン |
| [`docs/FRONTEND.md`](./docs/FRONTEND.md) | フロントエンド固有のガイドライン |
| [`docs/PLANS.md`](./docs/PLANS.md) | 実行プランの管理方針・インデックス |
| [`docs/PRODUCT_SENSE.md`](./docs/PRODUCT_SENSE.md) | プロダクト理念・ユーザー中心の原則 |
| [`docs/QUALITY_SCORE.md`](./docs/QUALITY_SCORE.md) | 品質スコアリング基準・ギャップ追跡 |
| [`docs/RELIABILITY.md`](./docs/RELIABILITY.md) | 信頼性要件・パフォーマンス目標 |
| [`docs/SECURITY.md`](./docs/SECURITY.md) | セキュリティ原則・境界バリデーション要件 |

### 設計ドキュメント
- [`docs/design-docs/index.md`](./docs/design-docs/index.md) — 設計判断のカタログ
- [`docs/design-docs/core-beliefs.md`](./docs/design-docs/core-beliefs.md) — エージェントファーストの中核的信念

### 実行プラン
- [`docs/exec-plans/active/`](./docs/exec-plans/active/) — 進行中のプラン
- [`docs/exec-plans/completed/`](./docs/exec-plans/completed/) — 完了したプラン
- [`docs/exec-plans/tech-debt-tracker.md`](./docs/exec-plans/tech-debt-tracker.md) — 技術的負債の追跡

### プロダクト仕様
- [`docs/product-specs/index.md`](./docs/product-specs/index.md) — 仕様書のインデックス

### 自動生成ドキュメント
- [`docs/generated/db-schema.md`](./docs/generated/db-schema.md) — DBスキーマ（自動生成）

### 外部リファレンス
- [`docs/references/`](./docs/references/) — 外部ツールの llms.txt など

---

## エージェントへの作業指示

### タスクの進め方
1. まず `ARCHITECTURE.md` を読んでドメイン構造を把握する
2. 該当する `docs/` 配下のドキュメントを参照して制約を確認する
3. 関連する `docs/exec-plans/active/` のプランがあれば確認する
4. コードを書く前に、既存パターンをコードベースから直接読み取る

### 判断に迷ったとき
- 技術選定・設計判断・仕様の解釈で複数の選択肢があり、人間の決定が必要な場合は **実装前に** `AskUserQuestion` ツールでヒアリングする
- 「どちらでも大差ない」と判断できる場合は自律的に決定し、該当プランの `## 意思決定ログ` に理由を記録する

### プルリクエスト
- PR は小さく・短命に保つ
- すべての変更にテストを含める
- CI がパスするまでマージしない

### ドキュメント更新
- 動作が変わった場合は対応するドキュメントも同じPRで更新する
- 新しいアーキテクチャ判断は `docs/design-docs/` にカタログ化する
- 完了したプランは `docs/exec-plans/active/` から `completed/` に移動する

### やってはいけないこと
- `docs/` 以外の場所に設計判断を記録しない
- 境界でデータを検証せずに型を仮定しない
- 共有ユーティリティがある場合は独自ヘルパーを新規作成しない
