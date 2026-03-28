"""data/shogi.db の中身を確認するスクリプト。"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data/shogi.db")


def show(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row

    # テーブル一覧
    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
    ]
    print(f"tables: {tables}\n")

    # tournaments
    total, = conn.execute("SELECT COUNT(*) FROM tournaments").fetchone()
    print(f"=== tournaments  ({total} rows) ===")

    print("\n--- prefecture breakdown ---")
    for row in conn.execute(
        "SELECT prefecture, COUNT(*) AS cnt FROM tournaments GROUP BY prefecture ORDER BY cnt DESC"
    ):
        print(f"  {row['prefecture']}: {row['cnt']}")

    print("\n--- sample (10 rows) ---")
    for row in conn.execute(
        "SELECT date, prefecture, name, venue FROM tournaments ORDER BY date LIMIT 10"
    ):
        print(f"  {row['date']} [{row['prefecture']}] {row['name']} / {row['venue']}")



if __name__ == "__main__":
    if not DB_PATH.exists():
        print(f"DB not found: {DB_PATH}")
        raise SystemExit(1)
    conn = sqlite3.connect(DB_PATH)
    try:
        show(conn)
    finally:
        conn.close()
