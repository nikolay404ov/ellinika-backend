"""Telegram bot application setup and lifecycle management."""

import asyncio
import threading

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.bot.handlers import start, handle_text
from app.config import Config


# Global state for bot loop management
loop = None
loop_started = False
loop_lock = threading.Lock()
bot_ready_event = None


def create_bot_application():
    """Create and configure Telegram bot application."""
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    return application


# Global bot application instance
application = create_bot_application()


async def bot_main():
    """Main bot coroutine - initializes and keeps bot running."""
    global bot_ready_event
    bot_ready_event = asyncio.Event()

    await application.initialize()
    await application.start()
    print("✅ Telegram bot initialized")

    bot_ready_event.set()  # Signal that bot is ready to process updates

    # Keep loop alive
    await asyncio.Event().wait()


def ensure_loop_running():
    """Ensure the async event loop is running in a separate thread."""
    global loop, loop_started
    with loop_lock:
        if loop_started:
            return

        loop_started = True
        loop = asyncio.new_event_loop()

        def runner():
            asyncio.set_event_loop(loop)
            print("⚙️ Telegram async loop running...")
            loop.run_until_complete(bot_main())

        threading.Thread(target=runner, daemon=True).start()


def get_loop():
    """Get the bot event loop."""
    return loop


def get_bot_ready_event():
    """Get the bot ready event."""
    return bot_ready_event

