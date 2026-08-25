import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()


def execute_query(sql: str):
    provider = os.getenv("DATABASE_PROVIDER", "sqlite").lower()
    if provider != "sqlite":
        raise RuntimeError("La POC 2026.08.25.1 usa SQLite. PostgreSQL se habilitará mediante el mismo adaptador.")
    path = os.getenv("SQLITE_PATH", "data/incendios_dummy.db")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
