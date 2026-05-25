# نرخ‌یار — Bale Currency & Gold Price Bot

A Bale messenger bot that displays real-time prices for USD, EUR, 18K Gold, and Emami Coin, sourced live from [tgju](tgju.org). Includes inline keyboard navigation and a CLI/Web admin panel with user statistics.

---

## Features

- `/start` — Welcome message with inline keyboard
- `/price` — Live prices for all assets in one message
- Inline buttons to view each asset individually
- Per-asset refresh button
- Graceful error handling — bot never crashes on API failure
- SQLite-backed user tracking
- CLI and web admin panel with usage statistics

---

## Project Structure

```
nerkhyar-bot/
├── src/
│   ├── __init__.py
│   ├── api.py            # Price fetching from Bonbast with retry logic
│   ├── bot.py            # Bot event handlers
│   ├── config.py         # Environment variable loading
│   ├── database.py       # SQLite user and command tracking
│   └── formatter.py      # Message formatting helpers
├── tests/
│   ├── __init__.py
│   ├── test_formatter.py
│   └── test_database.py
├── admin.py              # CLI admin panel
├── admin_web.py          # Admin panel on a simple web page
├── main.py               # Entry point
├── .env                  # Secret tokens (you should add yours)
├── .gitignore
└── README.md
```

---

---

## Requirements

- Python 3.11 or higher
- A Bale bot token from `@BotFather` on Bale

---

## Installation

```bash
git clone https://github.com/your-username/nerkhyar-bot.git
cd nerkhyar-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_bale_bot_token_here
```

---

## Running the Bot

```bash
python main.py
```

---

## Admin Panel

CLI:
```bash
python admin.py
```

Web (runs on port 8080):
```bash
python admin_web.py
```

---

## Tests

```bash
pytest tests/ -v
```

Tests are fully self-contained. A temporary database is created and deleted after each run. No external API calls are made.

---

## Data Source

Prices are fetched live from [tgju.org](https://tgju.org). The bot retries up to 3 times on failure.