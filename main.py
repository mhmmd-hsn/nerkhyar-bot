from src.config import setup_logging
from src.bot import client

if __name__ == "__main__":
    setup_logging()
    client.run()