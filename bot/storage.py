import sqlite3
from pathlib import Path


class Storage:
    """Хранит тех, кто запускал бота и кто получил файл (для статистики)."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "user_id INTEGER PRIMARY KEY, username TEXT, "
            "started_at TEXT DEFAULT CURRENT_TIMESTAMP, received_at TEXT)"
        )
        self._db.commit()

    def add_user(self, user_id: int, username: str | None) -> None:
        self._db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username),
        )
        self._db.commit()

    def mark_received(self, user_id: int) -> None:
        self._db.execute(
            "UPDATE users SET received_at = COALESCE(received_at, CURRENT_TIMESTAMP) "
            "WHERE user_id = ?",
            (user_id,),
        )
        self._db.commit()

    def stats(self) -> tuple[int, int]:
        started, received = self._db.execute(
            "SELECT COUNT(*), COUNT(received_at) FROM users"
        ).fetchone()
        return started, received
