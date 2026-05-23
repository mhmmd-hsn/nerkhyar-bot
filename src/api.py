import time
from bonbast.server import get_prices_from_api, get_token_from_main_page

def fetch_prices(retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            token = get_token_from_main_page()
            currencies, coins, golds = get_prices_from_api(token)

            currency_map = {c.code: c for c in currencies}
            coin_map = {c.code: c for c in coins}
            gold_map = {g.code: g for g in golds}

            return {
                "usd": currency_map.get("USD"),
                "eur": currency_map.get("EUR"),
                "gold": gold_map.get("gol18"),
                "coin": coin_map.get("emami1"),
            }
        except (Exception, SystemExit):
            if attempt < retries - 1:
                time.sleep(1)
    return None