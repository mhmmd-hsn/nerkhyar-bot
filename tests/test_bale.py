import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.rate_limiter import is_allowed, _last_request


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    _last_request.clear()
    yield


def test_rate_limiter_allows_first_request():
    assert is_allowed(123456) is True


def test_rate_limiter_blocks_immediate_second_request():
    is_allowed(123456)
    assert is_allowed(123456) is False


def test_rate_limiter_allows_different_users():
    is_allowed(111111)
    assert is_allowed(222222) is True


def test_rate_limiter_allows_after_cooldown():
    import time
    from src import rate_limiter
    is_allowed(123456)
    _last_request[123456] = time.time() - 10
    assert is_allowed(123456) is True


@pytest.mark.asyncio
async def test_edit_helper_calls_edit_message():
    with patch("src.bot.client") as mock_client:
        mock_client.edit_message = AsyncMock()
        callback = MagicMock()
        callback.message.chat.id = 123
        callback.message.message_id = 456

        from src.bot import _edit
        await _edit(callback, "test message")

        mock_client.edit_message.assert_called_once_with(
            123, 456, "test message", components=None
        )