import time
import logging
import requests

from src.config import BOT_TOKEN, ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

ENDPOINTS = {
    "usd": "https://api.tgju.org/v1/market/indicator/summary-table-data/price_dollar_rl",
    "eur": "https://api.tgju.org/v1/market/indicator/summary-table-data/price_eur",
    "gold": "https://api.tgju.org/v1/market/indicator/summary-table-data/geram18",
    "coin": "https://api.tgju.org/v1/market/indicator/summary-table-data/sekee",
}

CACHE_TTL = 120

_cache: dict = {
    "data": None,
    "timestamp": 0.0,
}


def _is_cache_valid() -> bool:
    return _cache["data"] is not None and (time.time() - _cache["timestamp"]) < CACHE_TTL


_last_notification: float = 0.0
NOTIFICATION_COOLDOWN = 300

def _notify_admin(message: str):
    global _last_notification
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        return
    if time.time() - _last_notification < NOTIFICATION_COOLDOWN:
        return
    try:
        requests.post(
            f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_CHAT_ID, "text": f"⚠️ Admin Alert:\n{message}"},
            timeout=5
        )
        _last_notification = time.time()
    except Exception:
        pass


def fetch_single(url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            data = response.json()
            row = data["data"][0]
            return {
                "price": row[0],
                "change": row[4],
                "change_pct": row[5],
            }
        except KeyError as e:
            msg = f"API structure changed. Missing key: {e}. Response: {data}"
            logger.error(msg)
            _notify_admin(msg)
            return None
        except IndexError as e:
            msg = f"API structure changed. Index error: {e}"
            logger.error(msg)
            _notify_admin(msg)
            return None
        except requests.RequestException as e:
            logger.warning(f"Network error on attempt {attempt + 1}: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    logger.error(f"All {retries} attempts failed for {url}")
    return None


def fetch_prices() -> dict | None:
    if _is_cache_valid():
        logger.debug("Returning cached prices")
        return _cache["data"]

    logger.info("Cache expired or empty, fetching fresh prices")
    result = {}
    for key, url in ENDPOINTS.items():
        item = fetch_single(url)
        if item is None:
            logger.error(f"Failed to fetch {key}, returning last cached data if available")
            return _cache["data"]
        result[key] = item

    _cache["data"] = result
    _cache["timestamp"] = time.time()
    logger.info("Prices updated and cached successfully")
    return result