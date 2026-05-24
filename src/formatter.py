import re
import jdatetime

LABELS = {
    "usd": "🇺🇸 دلار",
    "eur": "🇪🇺 یورو",
    "gold": "🥇 طلای ۱۸ عیار (هر گرم)",
    "coin": "🪙 سکه امامی",
}

def to_persian(text: str) -> str:
    mapping = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    return str(text).translate(mapping)

def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value).strip()

def to_toman(rial_str: str) -> str:
    try:
        if not rial_str:
            return "نامشخص"
        rial = int(rial_str.replace(",", ""))
        toman = rial // 10
        return to_persian(f"{toman:,}") + " تومان"
    except (ValueError, TypeError):
        return "نامشخص"

def format_prices_message(data: dict) -> str:
    now = to_persian(jdatetime.datetime.now().strftime("%H:%M - %Y/%m/%d"))
    lines = [f"📊 قیمت‌های لحظه‌ای\n🕐 {now}\n{'─' * 28}"]
    for key, label in LABELS.items():
        item = data.get(key)
        if item:
            price = to_toman(item["price"])
            change = to_persian(strip_html(item["change"]))
            pct = to_persian(strip_html(item["change_pct"]))
            trend = "🔻" if "low" in item["change"] else "🔺"
            lines.append(f"{label}\n{price}  {trend} {change} ({pct})")
    lines.append('─' * 28)
    return "\n\n".join(lines)

def format_single(key: str, data: dict) -> str:
    item = data.get(key)
    label = LABELS.get(key, key)
    now = to_persian(jdatetime.datetime.now().strftime("%H:%M - %Y/%m/%d"))
    if item is None:
        return f"{label}\n❌ اطلاعات در دسترس نیست"
    price = to_toman(item["price"])
    change = to_persian(strip_html(item["change"]))
    pct = to_persian(strip_html(item["change_pct"]))
    trend = "🔻" if "low" in item["change"] else "🔺"
    return f"📊 {label}\n🕐 {now}\n\n{price}\n{trend} {change} ({pct})"