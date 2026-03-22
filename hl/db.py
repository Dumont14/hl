"""HL Database — SQLite persistence layer."""

import sqlite3
from datetime import datetime
from pathlib import Path
from hl.config import DB_PATH


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist. Safe to run multiple times."""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS decisions (
            id          TEXT PRIMARY KEY,
            content     TEXT NOT NULL,
            type        TEXT NOT NULL DEFAULT 'approach',
            status      TEXT NOT NULL DEFAULT 'pending',
            reason      TEXT,
            created_at  TEXT NOT NULL,
            session_id  TEXT NOT NULL,
            revoked_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS snapshots (
            id          TEXT PRIMARY KEY,
            summary     TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            session_id  TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def insert_decision(id, content, type, session_id, reason="", status="confirmed"):
    conn = get_conn()
    conn.execute(
        """INSERT OR REPLACE INTO decisions
           (id, content, type, status, reason, created_at, session_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (id, content, type, status, reason, datetime.now().isoformat(), session_id),
    )
    conn.commit()
    conn.close()


def list_decisions(status="confirmed") -> list[sqlite3.Row]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM decisions WHERE status = ? ORDER BY created_at ASC",
        (status,),
    ).fetchall()
    conn.close()
    return rows


def get_recent_decisions(limit=10) -> list[sqlite3.Row]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM decisions WHERE status = 'confirmed' ORDER BY created_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows


def db_exists() -> bool:
    return Path(DB_PATH).exists()
