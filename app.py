import os
import random
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")

app = Flask(__name__)
bot = Bot(token=TOKEN)

# Dispatcher без очереди, всё синхронно
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# --- Данные алфавита ---
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

# --- Хэндлеры ---
def start(update, context):
    update.message.reply_text(
        "Привет! 🇬🇷 Я помогу тебе выучить греческий алфавит.\n"
        "Напиши /next чтобы получить новую букву!"
    )

def next_letter(update, context):
    greek, name, latin, example = random.choice(GREEK_ALPHABET)
    update.message.reply_text(
        f"🔤 {greek}\n"
        f"📖 Название: {name}\n"
        f"💬 Произношение: {latin}\n"
        f"🔠 Пример: {example}"
    )

def echo(update, context):
    update.message.reply_text("Напиши /next чтобы получить букву 🇬🇷")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("next", next_letter))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# --- Webhook endpoint ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Greek bot is running!"

if __name__ == "__main__":
    # локальный запуск, Render всё равно использует gunicorn
    app.run(host="0.0.0.0", port=8080)