import sqlite3
from pathlib import Path

from picture_matcher.types import ImageCandidate


def open_database(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY,
            source_path TEXT NOT NULL,
            similar_path TEXT NOT NULL,
            similarity REAL NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'moved', 'ignored'))
        )
    """)
    return connection


def replace_candidates(connection: sqlite3.Connection, candidates: tuple[ImageCandidate, ...]) -> None:
    with connection:
        connection.execute("DELETE FROM candidates")
        connection.executemany(
            "INSERT INTO candidates(source_path, similar_path, similarity, status) VALUES (?, ?, ?, ?)",
            [(str(item.source), str(item.similar), item.similarity, item.status) for item in candidates],
        )
