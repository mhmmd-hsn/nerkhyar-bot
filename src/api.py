import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

ENDPOINTS = {
    "usd": "https://api.tgju.org/v1/market/indicator/summary-table-data/price_dollar_rl",
    "eur": "https://api.tgju.org/v1/market/indicator/summary-table-data/price_eur",
    "gold": "https://api.tgju.org/v1/market/indicator/summary-table-data/geram18",
    "coin": "https://api.tgju.org/v1/market/indicator/summary-table-data/sekee",
}

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
        except Exception:
            continue
    return None

def fetch_prices() -> dict | None:
    result = {}
    for key, url in ENDPOINTS.items():
        item = fetch_single(url)
        if item is None:
            return None
        result[key] = item
    return result