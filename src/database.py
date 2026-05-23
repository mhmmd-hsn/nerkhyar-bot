import sqlite3
from datetime import datetime

DB_PATH = "data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_seen TEXT,
                last_seen TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                command TEXT,
                used_at TEXT
            )
        """)

def upsert_user(user_id: int, username: str):
    now = datetime.now().isoformat()
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE users SET last_seen = ?, username = ? WHERE user_id = ?",
                (now, username, user_id)
            )
        else:
            conn.execute(
                "INSERT INTO users (user_id, username, first_seen, last_seen) VALUES (?, ?, ?, ?)",
                (user_id, username, now, now)
            )

def log_command(user_id: int, command: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO commands (user_id, command, used_at) VALUES (?, ?, ?)",
            (user_id, command, datetime.now().isoformat())
        )