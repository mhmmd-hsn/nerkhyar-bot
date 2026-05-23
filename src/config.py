import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")
NAVASAN_BASE_URL = "http://api.navasan.tech/latest/"