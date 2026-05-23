from flask import Flask
from admin import list_users, total_users, active_users_24h, top_command


app = Flask(__name__)

@app.route("/")
def dashboard():
    users = list_users()
    cmd, count = top_command()
    
    rows = "".join(
        f"<tr><td>{u[0]}</td><td>{u[1] or 'N/A'}</td><td>{u[2][:19]}</td><td>{u[3][:19]}</td></tr>"
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