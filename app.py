import os
import random
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# --- Настройки ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
app = Flask(__name__)

# --- Создаём глобальный event loop ---
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# --- Алфавит ---
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
    ("Ο ο", "όμικρον", "ómikron", "O"),
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

# --- Обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🇬🇷 Я помогу тебе выучить греческий алфавит.\n"
        "Напиши /next чтобы получить новую букву!"
    )

async def next_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greek, name, latin, example = random.choice(GREEK_ALPHABET)
    await update.message.reply_text(
        f"🔤 {greek}\n📖 Название: {name}\n💬 Произношение: {latin}\n🔠 Пример: {example}"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши /next чтобы получить букву 🇬🇷")

# --- Telegram Application ---
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("next", next_letter))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- Инициализация приложения ---
async def init_telegram_app():
    if not application.running:
        await application.initialize()
        await application.start()
        print("✅ Telegram Application initialized")

# --- Webhook ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📬 Update from Telegram:", data)
    update = Update.de_json(data, application.bot)

    async def process():
        await init_telegram_app()
        await application.process_update(update)

    # Используем глобальный loop
    loop.create_task(process())
    return "ok"

@app.route("/")
def index():
    return "Greek bot is running!"

if __name__ == "__main__":
    print("🚀 Starting Flask app...")
    app.run(host="0.0.0.0", port=8080)
