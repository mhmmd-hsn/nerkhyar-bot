from src.formatter import format_price, format_prices_message, format_single

class MockCurrency:
    def __init__(self, buy, sell):
        self.buy = buy
        self.sell = sell

class MockGold:
    def __init__(self, price):
        self._price = price

def make_data():
    return {
        "usd": MockCurrency(175800, 175900),
        "eur": MockCurrency(204000, 204200),
        "gold": MockGold(19204487.0),
        "coin": MockCurrency(186000000, 189000000),
    }

def test_format_price_normal():
    assert format_price(175800) == "۱۷۵،۸۰۰ تومان"

def test_format_price_zero():
    assert format_price(0) == "۰ تومان"

def test_format_price_invalid():
    assert format_price(None) == "نامشخص"

def test_format_prices_message_contains_labels():
    msg = format_prices_message(make_data())
    assert "دلار" in msg
    assert "یورو" in msg
    assert "طلا" in msg
    assert "سکه" in msg

def test_format_single_usd():
    result = format_single("usd", make_data())
    assert "دلار" in result
    assert "175,800" in result

def test_format_single_gold():
    result = format_single("gold", make_data())
    assert "طلا" in result
    assert "19,204,487" in result

def test_format_single_missing_key():
    result = format_single("btc", make_data())
    assert "نامشخص" in result or "در دسترس نیست" in result