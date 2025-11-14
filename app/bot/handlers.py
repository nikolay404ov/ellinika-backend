"""Telegram bot command handlers."""

import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.bot.data import GREEK_ALPHABET


def get_next_letter_keyboard():
    """Create inline keyboard with 'Next letter' button."""
    keyboard = [
        [InlineKeyboardButton("🔤 Следующая буква", callback_data="next_letter")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random Greek letter (used by both command and button handler)."""
    greek, name, latin, example = random.choice(GREEK_ALPHABET)
    user_id = update.effective_user.id
    print("▶️ Letter sent to", user_id, "->", greek)
    
    text = (
        f"🔤 {greek}\n"
        f"📖 Название: {name}\n"
        f"💬 Произношение: {latin}\n"
        f"🔠 Пример: {example}"
    )
    
    # Check if it's a callback query (button press) or message
    if update.callback_query:
        # Button press - edit existing message
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=get_next_letter_keyboard()
        )
    else:
        # Command or message - send new message
        await update.message.reply_text(
            text=text,
            reply_markup=get_next_letter_keyboard()
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    print("▶️ /start from", update.effective_user.id)
    await update.message.reply_text(
        "Привет! 🇬🇷 Я помогу тебе выучить греческий алфавит.\n"
        "Нажми кнопку ниже, чтобы получить букву!",
        reply_markup=get_next_letter_keyboard()
    )


async def next_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /next command - send random Greek letter."""
    await send_letter(update, context)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callback queries."""
    query = update.callback_query
    
    if query.data == "next_letter":
        await send_letter(update, context)
    else:
        await query.answer("Неизвестная команда")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages."""
    print("💬 text from", update.effective_user.id, ":", update.message.text)
    await update.message.reply_text(
        "Нажми кнопку ниже, чтобы получить букву 🇬🇷",
        reply_markup=get_next_letter_keyboard()
    )

