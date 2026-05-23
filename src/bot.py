from bale import Bot, Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from src.config import BOT_TOKEN
from src.api import fetch_prices
from src.formatter import format_prices_message, format_single
from src.database import init_db, upsert_user, log_command

client = Bot(token=BOT_TOKEN)


def build_start_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🇺🇸 دلار", callback_data="price_usd"))
    markup.add(InlineKeyboardButton("🇪🇺 یورو", callback_data="price_eur"), row=2)
    markup.add(InlineKeyboardButton("🥇 طلا", callback_data="price_gold"), row=3)
    markup.add(InlineKeyboardButton("🪙 سکه", callback_data="price_coin"), row=4)
    markup.add(InlineKeyboardButton("📊 مشاهده همه", callback_data="refresh"), row=5)
    return markup


def build_keyboard(current: str = None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    if current is None:
        markup.add(InlineKeyboardButton("🇺🇸 دلار", callback_data="price_usd"))
        markup.add(InlineKeyboardButton("🇪🇺 یورو", callback_data="price_eur"), row=2)
        markup.add(InlineKeyboardButton("🥇 طلا", callback_data="price_gold"), row=3)
        markup.add(InlineKeyboardButton("🪙 سکه", callback_data="price_coin"), row=4)
        markup.add(InlineKeyboardButton("🔄 به‌روزرسانی", callback_data="refresh"), row=5)
    else:
        buttons = {
            "usd": "🇺🇸 دلار",
            "eur": "🇪🇺 یورو",
            "gold": "🥇 طلا",
            "coin": "🪙 سکه",
        }
        row = 1
        for key, label in buttons.items():
            if key != current:
                markup.add(InlineKeyboardButton(label, callback_data=f"price_{key}"), row=row)
                row += 1
        markup.add(InlineKeyboardButton("🔄 به‌روزرسانی", callback_data=f"refresh_{current}"), row=row)
        markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data="refresh"), row=row + 1)

    return markup


async def _edit(callback: CallbackQuery, text: str, keyboard: InlineKeyboardMarkup = None):
    await client.edit_message(
        callback.message.chat.id,
        callback.message.message_id,
        text,
        components=keyboard
    )


@client.event
async def on_ready():
    print(f"{client.user.username} is running...")
    init_db()


@client.event
async def on_message(message: Message):
    if message.content == "/start":
        upsert_user(message.from_user.id, message.from_user.username or "")
        log_command(message.from_user.id, "/start")
        await message.reply(
            "سلام! 👋\nبا این ربات می‌تونی قیمت لحظه‌ای ارز و طلا رو ببینی.\n\n"
            "از دستور /price استفاده کن یا روی دکمه‌ها بزن.",
            components=build_start_keyboard()
        )

    elif message.content == "/price":
        upsert_user(message.from_user.id, message.from_user.username or "")
        log_command(message.from_user.id, "/price")
        loading = await message.reply("⏳ در حال دریافت قیمت‌ها...")
        data = fetch_prices()
        if data is None:
            await client.edit_message(
                loading.chat.id,
                loading.message_id,
                "⚠️ دریافت قیمت‌ها با خطا مواجه شد. لطفاً دوباره تلاش کن."
            )
            return
        await client.edit_message(
            loading.chat.id,
            loading.message_id,
            format_prices_message(data),
            components=build_keyboard()
        )


@client.event
async def on_callback(callback: CallbackQuery):
    upsert_user(callback.from_user.id, callback.from_user.username or "")

    if callback.data == "refresh":
        log_command(callback.from_user.id, "refresh")
        await _edit(callback, "⏳ در حال دریافت قیمت‌ها...")
        data = fetch_prices()
        if data is None:
            await _edit(callback, "⚠️ دریافت قیمت‌ها با خطا مواجه شد. لطفاً دوباره تلاش کن.")
            return
        await _edit(callback, format_prices_message(data), build_keyboard())

    elif callback.data.startswith("refresh_"):
        key = callback.data.replace("refresh_", "")
        log_command(callback.from_user.id, f"refresh_{key}")
        await _edit(callback, "⏳ در حال دریافت قیمت‌ها...")
        data = fetch_prices()
        if data is None:
            await _edit(callback, "⚠️ دریافت قیمت‌ها با خطا مواجه شد. لطفاً دوباره تلاش کن.")
            return
        await _edit(callback, format_single(key, data), build_keyboard(current=key))

    elif callback.data.startswith("price_"):
        key = callback.data.replace("price_", "")
        log_command(callback.from_user.id, f"inline_{key}")
        await _edit(callback, "⏳ در حال دریافت قیمت‌ها...")
        data = fetch_prices()
        if data is None:
            await _edit(callback, "⚠️ دریافت قیمت‌ها با خطا مواجه شد. لطفاً دوباره تلاش کن.")
            return
        await _edit(callback, format_single(key, data), build_keyboard(current=key))


def main():
    client.run()