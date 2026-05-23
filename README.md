# 📊 نرخ‌یار — Bale Currency & Gold Price Bot

A Bale messenger bot that displays real-time prices for **USD**, **EUR**, **18K Gold**, and **Emami Coin**, sourced live from Bonbast. Includes inline keyboard navigation and a CLI admin panel with user statistics.

---

## Features

- `/start` — Welcome message with inline keyboard
- `/price` — Live prices for all assets in one message
- Inline buttons to view each asset individually
- Refresh button that updates the message in-place (no new message sent)
- Graceful error handling — bot never crashes on API failure, always notifies the user
- SQLite-backed user tracking with zero configuration
- CLI admin panel with usage statistics

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
├── main.py               # Entry point
├── .env                  # Secret tokens (never committed)
├── .gitignore
└── README.md
```

---

## Requirements

- Python 3.11 or higher
- A Bale bot token (obtained from `@BotFather` on Bale)
- **No active VPN** — Bonbast blocks non-Iranian IP addresses

---

## Installation

```bash
git clone https://github.com/your-username/nerkhyar-bot.git
cd nerkhyar-bot

python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate

pip install python-bale-bot bonbast python-dotenv pytest
```

---

## Configuration

Create a `.env` file in the project root with the following content:

```env
BOT_TOKEN=your_bale_bot_token_here
```

> ⚠️ Never commit your `.env` file. It is already excluded via `.gitignore`.

---

## Running the Bot

```bash
source .venv/bin/activate
python main.py
```

Expected output:

```
nerkhyarbot is running...
```

Open Bale, find your bot, and send `/start` to verify it responds.

---

## Admin Panel

Run in a separate terminal while the bot is active:

```bash
python admin.py
```

Output example:

```
========================================
  Total users     : 5
  Active (24h)    : 3
  Top command     : /price (42 times)
========================================
  ID           Username             First Seen             Last Seen
--------------------------------------------------------------------------------
  830913345    N/A                  2026-05-23T20:23:43    2026-05-23T20:51:29
========================================
```

---

## Running Tests

```bash
pytest tests/ -v
```

Tests are fully self-contained. A temporary database is created and automatically deleted after each test run. No external API calls are made.

---

## Data Source

Prices are fetched live from [Bonbast](https://bonbast.com) using the [`bonbast`](https://github.com/SamadiPour/bonbast) Python package. The bot retries up to 3 times on transient failures. If all retries fail, the user receives a clear error message in Persian. No hardcoded prices are used anywhere in the codebase.

---

## Troubleshooting

**SSL certificate error on macOS:**

```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

**Bot gets no response from Bonbast:**
Make sure no VPN is active. Bonbast blocks non-Iranian IP addresses.

**Bot starts but commands do nothing:**
Confirm your `BOT_TOKEN` in `.env` is correct and the bot is active on Bale.

---

## Deployment (Linux Server)

For a persistent deployment on a VPS:

```bash
# Install dependencies
pip install python-bale-bot bonbast python-dotenv

# Run with nohup
nohup python main.py > bot.log 2>&1 &
```

For a more robust setup, create a systemd service:

```ini
[Unit]
Description=Nerkhyar Bale Bot
After=network.target

[Service]
WorkingDirectory=/path/to/nerkhyar-bot
ExecStart=/path/to/.venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nerkhyar
sudo systemctl start nerkhyar
```