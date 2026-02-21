"""Tests for app/bot/handlers.py."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from telegram import ReplyKeyboardMarkup


# ---------------------------------------------------------------------------
# Keyboard builders
# ---------------------------------------------------------------------------

class TestGetMainKeyboard:
    def test_returns_reply_keyboard_markup(self):
        from app.bot.handlers import get_main_keyboard
        kb = get_main_keyboard()
        assert isinstance(kb, ReplyKeyboardMarkup)

    def test_main_keyboard_has_two_rows(self):
        from app.bot.handlers import get_main_keyboard
        kb = get_main_keyboard()
        assert len(kb.keyboard) == 2

    def test_main_keyboard_button_labels(self):
        from app.bot.handlers import get_main_keyboard
        kb = get_main_keyboard()
        labels = [btn.text for row in kb.keyboard for btn in row]
        assert "Карточки слов" in labels
        assert "В начало" in labels

    def test_main_keyboard_is_persistent(self):
        from app.bot.handlers import get_main_keyboard
        kb = get_main_keyboard()
        assert kb.is_persistent is True

    def test_main_keyboard_is_resized(self):
        from app.bot.handlers import get_main_keyboard
        kb = get_main_keyboard()
        assert kb.resize_keyboard is True


class TestGetCardsKeyboard:
    def test_returns_reply_keyboard_markup(self):
        from app.bot.handlers import get_cards_keyboard
        kb = get_cards_keyboard()
        assert isinstance(kb, ReplyKeyboardMarkup)

    def test_cards_keyboard_has_two_rows(self):
        from app.bot.handlers import get_cards_keyboard
        kb = get_cards_keyboard()
        assert len(kb.keyboard) == 2

    def test_cards_keyboard_button_labels(self):
        from app.bot.handlers import get_cards_keyboard
        kb = get_cards_keyboard()
        labels = [btn.text for row in kb.keyboard for btn in row]
        assert "Следующее слово" in labels
        assert "Показать перевод" in labels
        assert "В начало" in labels

    def test_cards_keyboard_is_persistent(self):
        from app.bot.handlers import get_cards_keyboard
        kb = get_cards_keyboard()
        assert kb.is_persistent is True


# ---------------------------------------------------------------------------
# Async handlers helpers
# ---------------------------------------------------------------------------

def _make_update(text):
    """Build a minimal mock Update with a text message."""
    user = MagicMock()
    user.id = 42

    message = MagicMock()
    message.text = text
    message.reply_text = AsyncMock()

    update = MagicMock()
    update.message = message
    update.effective_user = user
    return update


def _make_context(word_id=None):
    context = MagicMock()
    context.user_data = {}
    if word_id is not None:
        context.user_data["current_word_id"] = word_id
    return context


# ---------------------------------------------------------------------------
# show_main_menu
# ---------------------------------------------------------------------------

class TestShowMainMenu:
    @pytest.mark.asyncio
    async def test_sends_welcome_text(self):
        from app.bot.handlers import show_main_menu
        update = _make_update("anything")
        context = _make_context()
        await show_main_menu(update, context)
        update.message.reply_text.assert_awaited_once()
        call_kwargs = update.message.reply_text.call_args
        sent_text = call_kwargs[1].get("text") or call_kwargs[0][0]
        assert "греческие слова" in sent_text.lower() or "привет" in sent_text.lower()

    @pytest.mark.asyncio
    async def test_sends_main_keyboard(self):
        from app.bot.handlers import show_main_menu, get_main_keyboard
        update = _make_update("anything")
        context = _make_context()
        await show_main_menu(update, context)
        call_kwargs = update.message.reply_text.call_args[1]
        markup = call_kwargs.get("reply_markup")
        assert isinstance(markup, ReplyKeyboardMarkup)


# ---------------------------------------------------------------------------
# start handler
# ---------------------------------------------------------------------------

class TestStartHandler:
    @pytest.mark.asyncio
    async def test_start_calls_show_main_menu(self):
        from app.bot.handlers import start
        update = _make_update("/start")
        context = _make_context()
        with patch("app.bot.handlers.show_main_menu", new_callable=AsyncMock) as mock_menu:
            await start(update, context)
            mock_menu.assert_awaited_once_with(update, context)


# ---------------------------------------------------------------------------
# handle_text routing
# ---------------------------------------------------------------------------

class TestHandleTextRouting:
    @pytest.mark.asyncio
    async def test_kartochki_slov_calls_show_word_card(self):
        from app.bot.handlers import handle_text
        update = _make_update("Карточки слов")
        context = _make_context()
        with patch("app.bot.handlers.show_word_card", new_callable=AsyncMock) as mock_card:
            await handle_text(update, context)
            mock_card.assert_awaited_once_with(update, context, show_translation=False)

    @pytest.mark.asyncio
    async def test_next_word_calls_show_word_card(self):
        from app.bot.handlers import handle_text
        update = _make_update("Следующее слово")
        context = _make_context()
        with patch("app.bot.handlers.show_word_card", new_callable=AsyncMock) as mock_card:
            await handle_text(update, context)
            mock_card.assert_awaited_once_with(update, context, show_translation=False)

    @pytest.mark.asyncio
    async def test_v_nachalo_calls_show_main_menu(self):
        from app.bot.handlers import handle_text
        update = _make_update("В начало")
        context = _make_context()
        with patch("app.bot.handlers.show_main_menu", new_callable=AsyncMock) as mock_menu:
            await handle_text(update, context)
            mock_menu.assert_awaited_once_with(update, context)

    @pytest.mark.asyncio
    async def test_unknown_text_is_ignored(self):
        from app.bot.handlers import handle_text
        update = _make_update("some random message")
        context = _make_context()
        await handle_text(update, context)
        update.message.reply_text.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_show_translation_with_known_word(self):
        """'Показать перевод' should reply with the stored word's translation."""
        from app.bot.handlers import handle_text
        from app.models import Word

        mock_word = MagicMock(spec=Word)
        mock_word.greek_word = "αγάπη"
        mock_word.translation = "любовь"

        update = _make_update("Показать перевод")
        context = _make_context(word_id=7)

        with patch("app.bot.handlers.app") as mock_app, \
             patch("app.bot.handlers.get_word_by_id", return_value=mock_word):
            mock_app.app_context.return_value.__enter__ = MagicMock(return_value=None)
            mock_app.app_context.return_value.__exit__ = MagicMock(return_value=False)
            await handle_text(update, context)

        update.message.reply_text.assert_awaited_once()
        sent_text = update.message.reply_text.call_args[1].get("text") or \
                    update.message.reply_text.call_args[0][0]
        assert "любовь" in sent_text

    @pytest.mark.asyncio
    async def test_show_translation_without_stored_word_id(self):
        """'Показать перевод' with no stored word_id falls back to show_word_card."""
        from app.bot.handlers import handle_text
        update = _make_update("Показать перевод")
        context = _make_context()  # no word_id stored

        with patch("app.bot.handlers.show_word_card", new_callable=AsyncMock) as mock_card:
            await handle_text(update, context)
            mock_card.assert_awaited_once_with(update, context, show_translation=False)
