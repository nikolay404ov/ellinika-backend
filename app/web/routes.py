"""Flask web routes."""

import asyncio

from flask import request

from telegram import Update

from app.bot.setup import (
    application,
    ensure_loop_running,
    get_loop,
    get_bot_ready_event,
)
from app.config import Config


def register_routes(app):
    """Register all web routes."""
    
    @app.route(f"/{Config.TELEGRAM_TOKEN}", methods=["POST"])
    def webhook():
        """Handle Telegram webhook updates."""
        ensure_loop_running()

        data = request.get_json(force=True)
        print("Update from Telegram:", data)

        update = Update.de_json(data, application.bot)
        loop = get_loop()

        # Wait for bot initialization to complete
        bot_ready_event = get_bot_ready_event()
        if bot_ready_event is not None:
            asyncio.run_coroutine_threadsafe(bot_ready_event.wait(), loop).result()

        future = asyncio.run_coroutine_threadsafe(
            application.process_update(update),
            loop,
        )

        def _done(f: asyncio.Future):
            exc = f.exception()
            if exc:
                print("Error in process_update:", repr(exc))

        future.add_done_callback(_done)

        return "ok"

    @app.route("/")
    def index():
        """Health check endpoint."""
        return "Greek bot is running!"

