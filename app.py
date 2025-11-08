import os
import random
import asyncio
import threading

from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ====== CONFIG ======
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is not set")

app = Flask(__name__)

# ====== DATA ======
GREEK_ALPHABET = [
    ("Α α", "άλφα", "alfa", "A"),
    ("Β β", "βήτα", "víta", "B"),
    ("Γ γ", "γάμμα", "gámma", "G"),
    ("Δ δ", "δέλτα", "délta", "D"),
    ("Ε ε", "έψιλον", "épsilon", "E"),
    ("Ζ ζ", "ζήτα", "zíta", "Z"),
    ("Η η", "ήτα", "íta", "Ē"),
    ("Θ θ", "θήτα", "thíta", "Th"),
    ("Ι ι", "ιώτα", "ióta", "I"),
    ("Κ κ", "κάππα", "káppa", "K"),
    ("Λ λ", "λάμδα", "lámda", "L"),
    ("Μ μ", "μυ", "mi", "M"),
    ("Ν ν", "νυ", "ni", "N"),
    ("Ξ ξ", "ξι", "xi", "X"),
    ("Ο ο", "όμικрон", "ómikron", "O"),
    ("Π π", "πι", "pi", "P"),
    ("Ρ ρ", "ρο", "ro", "R"),
    ("Σ σ/ς", "σίγμα", "sígma", "S"),
    ("Τ τ", "ταυ", "taf", "T"),
    ("Υ υ", "ύψιλον", "ýpsilon", "Y/U"),
    ("Φ φ", "φι", "fi", "F"),
    ("Χ χ", "χι", "hi", "Kh"),
    ("Ψ ψ", "ψι", "psi", "Ps"),
    ("Ω ω", "ωμέγα", "oméga", "Ō"),
]

# ====== HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("▶️ /start from", update.effective_user.id)
    await update.message.reply_text(
        "Привет! 🇬🇷 Я помогу тебе выучить греческий алфавит.\n"
        "Напиши /next чтобы получить новую букву!"
    )

async def next_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greek, name, latin, example = random.choice(GREEK_ALPHABET)
    print("▶️ /next from", update.effective_user.id, "->", greek)
    await update.message.reply_text(
        f"🔤 {greek}\n"
        f"📖 Название: {name}\n"
        f"💬 Произношение: {latin}\n"
        f"🔠 Пример: {example}"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("💬 text from", update.effective_user.id, ":", update.message.text)
    await update.message.reply_text("Напиши /next чтобы получить букву 🇬🇷")

# ====== APPLICATION ======
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("next", next_letter))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ====== LOOP MANAGEMENT ======
loop = None
loop_started = False
loop_lock = threading.Lock()

async def bot_main():
    await application.initialize()
    await application.start()
    print("✅ Telegram bot initialized")
    # держим loop живым
    await asyncio.Event().wait()

def ensure_loop_running():
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

# ====== WEBHOOK ======
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    # запускаем loop при первом запросе (внутри воркера gunicorn)
    ensure_loop_running()

    data = request.get_json(force=True)
    print("📬 Update from Telegram:", data)

    update = Update.de_json(data, application.bot)

    future = asyncio.run_coroutine_threadsafe(
        application.process_update(update),
        loop,
    )

    # логируем возможные ошибки из хэндлеров
    def _done(f: asyncio.Future):
        exc = f.exception()
        if exc:
            print("❌ Error in process_update:", repr(exc))

    future.add_done_callback(_done)

    return "ok"

@app.route("/")
def index():
    return "Greek bot is running!"

