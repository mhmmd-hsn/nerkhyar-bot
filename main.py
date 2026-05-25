from src.bot import client
from admin_web import app

if __name__ == "__main__":
    client.run()
    app.run(host="0.0.0.0", port=8080)