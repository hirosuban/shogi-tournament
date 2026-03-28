import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from .types import Tournament

logger = logging.getLogger(__name__)


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def _transaction(conn: sqlite3.Connection) -> Generator[None, None, None]:
    try:
        yield
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def migrate(db_path: Path) -> None:
    """Create tables if they don't exist (idempotent)."""
    conn = _connect(db_path)
    with _transaction(conn):
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tournaments (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT    NOT NULL,
                name        TEXT    NOT NULL,
                venue       TEXT    NOT NULL,
                prefecture  TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                source_url  TEXT    NOT NULL,
                UNIQUE (date, name, venue)
            );
        """)
    conn.close()
    logger.info("DB migration complete: %s", db_path)


def upsert_tournaments(db_path: Path, tournaments: list[Tournament]) -> int:
    """Insert tournaments, ignoring duplicates. Returns inserted count."""
    conn = _connect(db_path)
    count = 0
    with _transaction(conn):
        for t in tournaments:
            cur = conn.execute(
                """
                INSERT OR IGNORE INTO tournaments
                    (date, name, venue, prefecture, category, source_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    t.date.isoformat(),
                    t.name,
                    t.venue,
                    t.prefecture,
                    ",".join(t.categories),
                    t.source_url,
                ),
            )
            count += cur.rowcount
    conn.close()
    return count
