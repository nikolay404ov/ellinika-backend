"""Telegram bot command handlers."""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from app.bot.database import get_random_word


def get_main_keyboard():
    """Create main menu keyboard."""
    keyboard = [
        [KeyboardButton("Карточки слов")],
        [KeyboardButton("В начало")]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите действие..."
    )


def get_cards_keyboard():
    """Create keyboard for word cards."""
    keyboard = [
        [KeyboardButton("Следующее слово"), KeyboardButton("Показать перевод")],
        [KeyboardButton("В начало")]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите действие..."
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu."""
    text = (
        "Привет! Я помогу тебе выучить греческие слова.\n\n"
        "Нажми кнопку ниже, чтобы начать изучение!"
    )
    
    await update.message.reply_text(
        text=text,
        reply_markup=get_main_keyboard()
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    print("/start from", update.effective_user.id)
    await show_main_menu(update, context)


async def show_word_card(update: Update, context: ContextTypes.DEFAULT_TYPE, show_translation=False):
    """Show a word card."""
    from app import app
    
    with app.app_context():
        word = get_random_word()
        
        if not word:
            await update.message.reply_text(
                "В базе данных пока нет слов. Добавьте слова для изучения!",
                reply_markup=get_main_keyboard()
            )
            return
        
        user_id = update.effective_user.id
        print("Word card shown to", user_id, "->", word.greek_word)
        
        if show_translation:
            text = (
                f"Греческое слово:\n"
                f"{word.greek_word}\n\n"
                f"Перевод:\n"
                f"{word.translation}"
            )
        else:
            text = (
                f"Греческое слово:\n"
                f"{word.greek_word}\n\n"
                f"Нажми 'Показать перевод', чтобы увидеть перевод!"
            )
        
        # Store word ID in context for showing translation
        context.user_data['current_word_id'] = word.id
        
        await update.message.reply_text(
            text=text,
            reply_markup=get_cards_keyboard()
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages and button presses. Only responds to button presses."""
    text = update.message.text
    user_id = update.effective_user.id
    
    # Only process button presses, ignore other text messages
    if text == "Карточки слов":
        print("Button pressed:", text, "from", user_id)
        await show_word_card(update, context, show_translation=False)
    elif text == "Следующее слово":
        print("Button pressed:", text, "from", user_id)
        await show_word_card(update, context, show_translation=False)
    elif text == "Показать перевод":
        print("Button pressed:", text, "from", user_id)
        # Get current word and show translation
        from app import app
        from app.bot.database import get_word_by_id
        
        word_id = context.user_data.get('current_word_id')
        if word_id:
            with app.app_context():
                word = get_word_by_id(word_id)
                if word:
                    text = (
                        f"Греческое слово:\n"
                        f"{word.greek_word}\n\n"
                        f"Перевод:\n"
                        f"{word.translation}"
                    )
                    await update.message.reply_text(
                        text=text,
                        reply_markup=get_cards_keyboard()
                    )
                else:
                    await show_word_card(update, context, show_translation=False)
        else:
            await show_word_card(update, context, show_translation=False)
    elif text == "В начало":
        print("Button pressed:", text, "from", user_id)
        await show_main_menu(update, context)
    # Ignore all other text messages - don't respond

