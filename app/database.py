import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DB_PATH = "/tmp/chatcoip/incendios_dummy.db"

DEMO_ROWS = [
    (1, "Los Ángeles", "Biobío", 18.4, "Controlado", "2025-01-12"),
    (2, "Nacimiento", "Biobío", 245.7, "Controlado", "2025-02-03"),
    (3, "Santa Juana", "Biobío", 82.1, "Controlado", "2025-02-17"),
    (4, "Concepción", "Biobío", 14.2, "Controlado", "2025-03-08"),
    (5, "Hualqui", "Biobío", 510.8, "Controlado", "2025-03-22"),
    (6, "Temuco", "La Araucanía", 37.6, "Controlado", "2025-01-29"),
    (7, "Angol", "La Araucanía", 193.5, "Controlado", "2025-02-11"),
    (8, "Collipulli", "La Araucanía", 64.0, "Controlado", "2025-02-26"),
    (9, "Victoria", "La Araucanía", 21.9, "Controlado", "2025-04-04"),
    (10, "Valdivia", "Los Ríos", 9.8, "Controlado", "2025-01-19"),
    (11, "Paillaco", "Los Ríos", 55.4, "Controlado", "2025-03-13"),
    (12, "Osorno", "Los Lagos", 31.2, "Controlado", "2025-02-07"),
    (13, "Puerto Montt", "Los Lagos", 12.7, "Controlado", "2025-04-18"),
    (14, "Talca", "Maule", 77.3, "Controlado", "2025-01-25"),
    (15, "Constitución", "Maule", 420.6, "Controlado", "2025-02-15"),
    (16, "Chillán", "Ñuble", 49.1, "Controlado", "2025-03-02"),
    (17, "Quillón", "Ñuble", 138.0, "Controlado", "2025-03-19"),
    (18, "Los Ángeles", "Biobío", 11.6, "Controlado", "2025-06-02"),
    (19, "Cabrero", "Biobío", 34.8, "Controlado", "2025-06-09"),
    (20, "Yumbel", "Biobío", 27.4, "Controlado", "2025-06-21"),
    (21, "Temuco", "La Araucanía", 16.2, "Controlado", "2025-06-05"),
    (22, "Angol", "La Araucanía", 41.7, "Controlado", "2025-06-16"),
    (23, "Talca", "Maule", 8.5, "Controlado", "2025-06-27"),
    (24, "Los Ángeles", "Biobío", 23.9, "Controlado", "2026-01-08"),
    (25, "Mulchén", "Biobío", 328.4, "Controlado", "2026-01-24"),
    (26, "Santa Bárbara", "Biobío", 71.0, "Controlado", "2026-02-09"),
    (27, "Temuco", "La Araucanía", 44.6, "Controlado", "2026-01-14"),
    (28, "Collipulli", "La Araucanía", 612.3, "Controlado", "2026-02-20"),
    (29, "Valdivia", "Los Ríos", 19.5, "Controlado", "2026-03-11"),
    (30, "Osorno", "Los Lagos", 26.8, "Controlado", "2026-03-26"),
    (31, "Talca", "Maule", 95.2, "Controlado", "2026-01-31"),
    (32, "Quillón", "Ñuble", 184.7, "Controlado", "2026-02-13"),
    (33, "Los Ángeles", "Biobío", 7.9, "Controlado", "2026-06-03"),
    (34, "Cañete", "Biobío", 29.3, "Controlado", "2026-06-10"),
    (35, "Lebu", "Biobío", 54.6, "Controlado", "2026-06-18"),
    (36, "Temuco", "La Araucanía", 13.1, "Controlado", "2026-06-07"),
    (37, "Victoria", "La Araucanía", 32.5, "Controlado", "2026-06-23"),
    (38, "Talca", "Maule", 6.4, "Controlado", "2026-06-29"),
    (39, "Nacimiento", "Biobío", 860.5, "No controlado", "2026-08-20"),
    (40, "Angol", "La Araucanía", 205.8, "No controlado", "2026-08-23"),
]


def _db_path() -> str:
    return os.getenv("SQLITE_PATH", DEFAULT_DB_PATH)


def ensure_demo_database() -> str:
    path = _db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS incendios (
                id INTEGER PRIMARY KEY,
                ubicacion TEXT NOT NULL,
                region TEXT NOT NULL,
                hectareas REAL NOT NULL,
                estado TEXT NOT NULL,
                fecha DATE NOT NULL
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM incendios").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO incendios (id, ubicacion, region, hectareas, estado, fecha) VALUES (?, ?, ?, ?, ?, ?)",
                DEMO_ROWS,
            )
            conn.commit()
    finally:
        conn.close()
    return path


def execute_query(sql: str):
    provider = os.getenv("DATABASE_PROVIDER", "sqlite").lower()
    if provider != "sqlite":
        raise RuntimeError("Esta versión demo usa SQLite. El adaptador permite cambiar de proveedor más adelante.")

    path = ensure_demo_database()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
