from src.formatter import to_toman, to_persian, strip_html, format_prices_message, format_single

def make_data():
    return {
        "usd": {"price": "1,792,100", "change": '<span class="low">16600</span>', "change_pct": '<span class="low">0.94%</span>'},
        "eur": {"price": "2,080,700", "change": '<span class="low">17400</span>', "change_pct": '<span class="low">0.84%</span>'},
        "gold": {"price": "191,498,000", "change": '<span class="high">5914000</span>', "change_pct": '<span class="high">3.19%</span>'},
        "coin": {"price": "1,909,850,000", "change": '<span class="low">40200000</span>', "change_pct": '<span class="low">2.13%</span>'},
    }

def test_to_persian_digits():
    assert to_persian("1234567890") == "۱۲۳۴۵۶۷۸۹۰"

def test_to_persian_mixed():
    assert to_persian("price: 100") == "price: ۱۰۰"

def test_strip_html_removes_tags():
    assert strip_html('<span class="low">16600</span>') == "16600"

def test_strip_html_plain_text():
    assert strip_html("hello") == "hello"

def test_to_toman_converts_correctly():
    assert to_toman("1,792,100") == "۱۷۹,۲۱۰ تومان"

def test_to_toman_large_number():
    assert to_toman("1,909,850,000") == "۱۹۰,۹۸۵,۰۰۰ تومان"

def test_to_toman_invalid_returns_unknown():
    assert to_toman(None) == "نامشخص"

def test_to_toman_empty_string():
    assert to_toman("") == "نامشخص"

def test_format_prices_message_contains_all_labels():
    msg = format_prices_message(make_data())
    assert "دلار" in msg
    assert "یورو" in msg
    assert "طلا" in msg
    assert "سکه" in msg

def test_format_prices_message_contains_prices():
    msg = format_prices_message(make_data())
    assert "تومان" in msg

def test_format_prices_message_contains_trend():
    msg = format_prices_message(make_data())
    assert "🔻" in msg or "🔺" in msg

def test_format_prices_message_contains_date():
    msg = format_prices_message(make_data())
    assert "🕐" in msg

def test_format_single_usd_contains_label():
    result = format_single("usd", make_data())
    assert "دلار" in result

def test_format_single_usd_contains_price():
    result = format_single("usd", make_data())
    assert "۱۷۹,۲۱۰" in result

def test_format_single_gold_shows_increase():
    result = format_single("gold", make_data())
    assert "🔺" in result

def test_format_single_usd_shows_decrease():
    result = format_single("usd", make_data())
    assert "🔻" in result

def test_format_single_missing_key():
    result = format_single("btc", make_data())
    assert "در دسترس نیست" in result