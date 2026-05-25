from flask import Flask
from admin import list_users, total_users, active_users_24h, top_command

app = Flask(__name__)


@app.route("/")
def dashboard():
    try:
        users = list_users()
        cmd, count = top_command()
    except Exception:
        return "<h2>Database not available</h2>", 500

    rows = "".join(
        f"<tr><td>{u['user_id']}</td><td>{u['username'] or 'N/A'}</td><td>{u['first_seen'][:19]}</td><td>{u['last_seen'][:19]}</td></tr>"
        for u in users
    )

    return f"""
    <h2>Total Users: {total_users()}</h2>
    <h2>Active (24h): {active_users_24h()}</h2>
    <h2>Top Command: {cmd} ({count} times)</h2>
    <table border="1">
      <tr><th>ID</th><th>Username</th><th>First Seen</th><th>Last Seen</th></tr>
      {rows}
    </table>
    """


if __name__ == "__main__":
    app.run(port=8080)