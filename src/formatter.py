import re
import jdatetime

SEPARATOR = "─" * 28

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


def now_shamsi() -> str:
    return to_persian(jdatetime.datetime.now().strftime("%H:%M - %Y/%m/%d"))


def _format_item(item: dict) -> str:
    price = to_toman(item["price"])
    change = to_toman(strip_html(item["change"]))
    pct = to_persian(strip_html(item["change_pct"]))
    trend = "🔻" if "low" in item["change"] else "🔺"
    return f"{price}  {trend} تغییر نسبت به دیروز: {change} ({pct})"


def format_prices_message(data: dict) -> str:
    is_stale = data.get("is_stale", False)
    header = (
        f"⚠️ به دلیل خطا، دسترسی به قیمت‌های لحظه‌ای ممکن نیست.\n"
        f"قیمت‌های زیر آخرین اطلاعات موجود هستند و ممکن است قدیمی باشند.\n{SEPARATOR}"
        if is_stale
        else f"📊 قیمت‌های لحظه‌ای\n🕐 {now_shamsi()}\n{SEPARATOR}"
    )
    lines = [header]
    for key, label in LABELS.items():
        item = data["data"].get(key)
        if item:
            lines.append(f"{label}\n{_format_item(item)}")
    lines.append(SEPARATOR)
    return "\n\n".join(lines)


def format_single(key: str, data: dict) -> str:
    item = data["data"].get(key)
    label = LABELS.get(key, key)
    is_stale = data.get("is_stale", False)

    if item is None:
        return f"{label}\n❌ اطلاعات در دسترس نیست"

    time_line = "⚠️ قیمت قدیمی — دسترسی به قیمت لحظه‌ای ممکن نیست" if is_stale else f"🕐 {now_shamsi()}"

    return f"📊 {label}\n{time_line}\n\n{_format_item(item)}"