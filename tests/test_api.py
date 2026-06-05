import pytest
import requests
from unittest.mock import patch, MagicMock
from src.api import fetch_single, fetch_prices, _cache, _refresh_cache

MOCK_RESPONSE = {
    "data": [
        ["1,792,100", "x", "x", "x", '<span class="low">16600</span>', '<span class="low">0.94%</span>']
    ]
}


@pytest.fixture(autouse=True)
def reset_cache():
    _cache["data"] = None
    _cache["timestamp"] = 0.0
    yield


def make_mock_response(data: dict, status_code: int = 200):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = data
    mock.raise_for_status = MagicMock()
    return mock


def test_fetch_single_success():
    with patch("src.api.requests.get") as mock_get:
        mock_get.return_value = make_mock_response(MOCK_RESPONSE)
        result = fetch_single("https://fake-url.com")
        assert result is not None
        assert result["price"] == "1,792,100"
        assert result["change"] == '<span class="low">16600</span>'
        assert result["change_pct"] == '<span class="low">0.94%</span>'


def test_fetch_single_network_error():
    with patch("src.api.requests.get") as mock_get:
        mock_get.side_effect = Exception("Connection timeout")
        result = fetch_single("https://fake-url.com", retries=1)
        assert result is None


def test_fetch_single_api_structure_changed_key_error():
    with patch("src.api.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"wrong_key": []})
        result = fetch_single("https://fake-url.com", retries=1)
        assert result is None


def test_fetch_single_api_structure_changed_index_error():
    with patch("src.api.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"data": []})
        result = fetch_single("https://fake-url.com", retries=1)
        assert result is None


def test_fetch_single_retries_on_network_error():
    with patch("src.api.requests.get") as mock_get:
        mock_get.side_effect = [
            requests.RequestException("timeout"),
            requests.RequestException("timeout"),
            make_mock_response(MOCK_RESPONSE),
        ]
        result = fetch_single("https://fake-url.com", retries=3)
        assert result is not None
        assert mock_get.call_count == 3


def test_fetch_single_returns_none_after_all_retries_fail():
    with patch("src.api.requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("timeout")
        result = fetch_single("https://fake-url.com", retries=3)
        assert result is None
        assert mock_get.call_count == 3


def test_fetch_prices_returns_none_when_cache_empty():
    result = fetch_prices()
    assert result is None


def test_fetch_prices_returns_cache_when_valid():
    _cache["data"] = {"usd": {"price": "1,792,100", "change": "x", "change_pct": "x"}}
    _cache["timestamp"] = 99999999999.0
    with patch("src.api.requests.get") as mock_get:
        result = fetch_prices()
        mock_get.assert_not_called()
        assert result is not None
        assert result["is_stale"] is False


def test_fetch_prices_returns_stale_when_cache_expired():
    _cache["data"] = {"usd": {"price": "1,000", "change": "x", "change_pct": "x"}}
    _cache["timestamp"] = 0.0
    result = fetch_prices()
    assert result is not None
    assert result["is_stale"] is True


def test_fetch_prices_returns_none_when_cache_empty_and_fetch_fails():
    with patch("src.api.fetch_single") as mock_fetch:
        mock_fetch.return_value = None
        result = fetch_prices()
        assert result is None


def test_refresh_cache_success():
    with patch("src.api.fetch_single") as mock_fetch:
        mock_fetch.return_value = {"price": "1,792,100", "change": "x", "change_pct": "x"}
        _refresh_cache()
        assert _cache["data"] is not None
        assert "usd" in _cache["data"]
        assert "eur" in _cache["data"]
        assert "gold" in _cache["data"]
        assert "coin" in _cache["data"]


def test_refresh_cache_failure_keeps_old_cache():
    old_data = {"usd": {"price": "old", "change": "x", "change_pct": "x"}}
    _cache["data"] = old_data
    with patch("src.api.fetch_single") as mock_fetch:
        mock_fetch.return_value = None
        _refresh_cache()
        assert _cache["data"] == old_data


def test_notify_admin_respects_cooldown():
    with patch("src.api.requests.post") as mock_post:
        import src.api as api_module
        api_module._last_notification = 99999999999.0
        from src.api import _notify_admin
        _notify_admin("test message")
        mock_post.assert_not_called()


def test_notify_admin_sends_when_cooldown_passed():
    with patch("src.api.requests.post") as mock_post:
        import src.api as api_module
        api_module._last_notification = 0.0
        from src.api import _notify_admin
        _notify_admin("test message")
        mock_post.assert_called_once()