"""Telegram bot command handlers."""

import random

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.data import GREEK_ALPHABET


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    print("▶️ /start from", update.effective_user.id)
    await update.message.reply_text(
        "Привет! 🇬🇷 Я помогу тебе выучить греческий алфавит.\n"
        "Напиши /next чтобы получить новую букву!"
    )


async def next_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /next command - send random Greek letter."""
    greek, name, latin, example = random.choice(GREEK_ALPHABET)
    print("▶️ /next from", update.effective_user.id, "->", greek)
    await update.message.reply_text(
        f"🔤 {greek}\n"
        f"📖 Название: {name}\n"
        f"💬 Произношение: {latin}\n"
        f"🔠 Пример: {example}"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages."""
    print("💬 text from", update.effective_user.id, ":", update.message.text)
    await update.message.reply_text("Напиши /next чтобы получить букву 🇬🇷")

