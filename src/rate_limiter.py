import time

RATE_LIMIT_SECONDS = 3

_last_request: dict[int, float] = {}


def is_allowed(user_id: int) -> bool:
    now = time.time()
    last = _last_request.get(user_id, 0.0)
    if now - last < RATE_LIMIT_SECONDS:
        return False
    _last_request[user_id] = now
    return True