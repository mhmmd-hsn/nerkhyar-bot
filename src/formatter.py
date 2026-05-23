import jdatetime


def to_persian_digits(text: str) -> str:
    mapping = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    return text.translate(mapping)

def format_price(value) -> str:
    if value is None:
        return "نامشخص"
    try:
        formatted = f"{int(value):,}"
        return to_persian_digits(formatted) + " تومان"
    except (ValueError, TypeError):
        return "نامشخص"

LABELS = {
    "usd": "🇺🇸 دلار",
    "eur": "🇪🇺 یورو",
    "gold": "🥇 طلای ۱۸ عیار (هر گرم)",
    "coin": "🪙 سکه امامی",
}

def format_prices_message(data: dict) -> str:
    now = to_persian_digits(jdatetime.datetime.now().strftime("%H:%M - %Y/%m/%d"))
    lines = [f"📊 قیمت‌های لحظه‌ای\n🕐 {now}\n"]

    usd = data.get("usd")
    eur = data.get("eur")
    gold = data.get("gold")
    coin = data.get("coin")

    if usd:
        lines.append(f"🇺🇸 دلار\nخرید: {format_price(usd.buy)}  |  فروش: {format_price(usd.sell)}")
    if eur:
        lines.append(f"🇪🇺 یورو\nخرید: {format_price(eur.buy)}  |  فروش: {format_price(eur.sell)}")
    if gold:
        lines.append(f"🥇 طلای ۱۸ عیار\n{format_price(gold._price)}")
    if coin:
        lines.append(f"🪙 سکه امامی\nخرید: {format_price(coin.buy)}  |  فروش: {format_price(coin.sell)}")

    return "\n\n".join(lines)

def format_single(key: str, data: dict) -> str:
    now = to_persian_digits(jdatetime.datetime.now().strftime("%H:%M - %Y/%m/%d"))
    item = data.get(key)
    label = LABELS.get(key, key)
    if item is None:
        return f"📊 {label}\n🕐 {now}\n\n❌ اطلاعات در دسترس نیست"
    if hasattr(item, 'buy'):
        return f"📊 {label}\n🕐 {now}\n\nخرید: {format_price(item.buy)}  |  فروش: {format_price(item.sell)}"
    return f"📊 {label}\n🕐 {now}\n{'─' * 28}\n{format_price(item._price)}"