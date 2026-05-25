import os
import pytest
from src import database

TEST_DB = "test.db"

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", TEST_DB)
    database.init_db()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_upsert_new_user():
    database.upsert_user(1, "testuser")
    with database.get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id = 1").fetchone()
    assert row is not None
    assert row["username"] == "testuser"


def test_upsert_updates_existing_user():
    database.upsert_user(1, "oldname")
    database.upsert_user(1, "newname")
    with database.get_connection() as conn:
        rows = conn.execute("SELECT * FROM users WHERE user_id = 1").fetchall()
    assert len(rows) == 1
    assert rows[0]["username"] == "newname"


def test_log_command():
    database.upsert_user(1, "testuser")
    database.log_command(1, "/price")
    with database.get_connection() as conn:
        row = conn.execute("SELECT * FROM commands WHERE user_id = 1").fetchone()
    assert row is not None
    assert row["command"] == "/price"