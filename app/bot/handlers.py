"""Telegram bot command handlers."""

import random

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from app.bot.data import GREEK_ALPHABET


def get_reply_keyboard():
    """Create reply keyboard that stays at the bottom of the chat."""
    keyboard = [
        [KeyboardButton("🔤 Следующая буква"), KeyboardButton("🏠 В начало")]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        persistent=True,
        input_field_placeholder="Выберите действие..."
    )


async def send_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random Greek letter."""
    greek, name, latin, example = random.choice(GREEK_ALPHABET)
    user_id = update.effective_user.id
    print("▶️ Letter sent to", user_id, "->", greek)
    
    text = (
        f"🔤 {greek}\n"
        f"📖 Название: {name}\n"
        f"💬 Произношение: {latin}\n"
        f"🔠 Пример: {example}"
    )
    
    await update.message.reply_text(
        text=text,
        reply_markup=get_reply_keyboard()
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu."""
    text = (
        "Привет! 🇬🇷 Я помогу тебе выучить греческий алфавит.\n"
        "Нажми кнопку ниже, чтобы получить букву!"
    )
    
    await update.message.reply_text(
        text=text,
        reply_markup=get_reply_keyboard()
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    print("▶️ /start from", update.effective_user.id)
    await show_main_menu(update, context)


async def next_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /next command - send random Greek letter."""
    await send_letter(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages and button presses."""
    text = update.message.text
    user_id = update.effective_user.id
    print("💬 text from", user_id, ":", text)
    
    if text == "🔤 Следующая буква":
        await send_letter(update, context)
    elif text == "🏠 В начало":
        await show_main_menu(update, context)
    else:
        # Unknown text - show menu
        await update.message.reply_text(
            "Нажми кнопку ниже, чтобы получить букву 🇬🇷",
            reply_markup=get_reply_keyboard()
        )

