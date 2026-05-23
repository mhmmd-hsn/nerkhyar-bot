from src.database import get_connection
from datetime import datetime, timedelta

def total_users():
    with get_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

def active_users_24h():
    cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
    with get_connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM users WHERE last_seen >= ?", (cutoff,)
        ).fetchone()[0]

def top_command():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT command, COUNT(*) as cnt FROM commands GROUP BY command ORDER BY cnt DESC LIMIT 1"
        ).fetchone()
        return result if result else ("none", 0)

def list_users():
    with get_connection() as conn:
        return conn.execute(
            "SELECT user_id, username, first_seen, last_seen FROM users ORDER BY last_seen DESC"
        ).fetchall()

def print_stats():
    print("=" * 40)
    print(f"  Total users     : {total_users()}")
    print(f"  Active (24h)    : {active_users_24h()}")
    cmd, count = top_command()
    print(f"  Top command     : {cmd} ({count} times)")
    print("=" * 40)
    print(f"  {'ID':<12} {'Username':<20} {'First Seen':<22} {'Last Seen'}")
    print("-" * 80)
    for user_id, username, first_seen, last_seen in list_users():
        print(f"  {user_id:<12} {username or 'N/A':<20} {first_seen[:19]:<22} {last_seen[:19]}")
    print("=" * 40)

if __name__ == "__main__":
    print_stats()