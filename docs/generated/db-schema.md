# DB Schema

**自動生成ドキュメント** — 手動で編集しないでください。
スキーマが変更されたら自動的に更新されます。

---

> データベーススキーマが定義されたら、
> `scripts/generate-db-schema.md` 相当のスクリプトでこのファイルを自動生成してください。
>
> 例:
> ```
> ## テーブル: users
> | カラム | 型 | 制約 | 説明 |
> |---|---|---|---|
> | id | uuid | PK | ユーザーID |
> | email | text | UNIQUE, NOT NULL | メールアドレス |
> | created_at | timestamptz | NOT NULL | 作成日時 |
> ```
