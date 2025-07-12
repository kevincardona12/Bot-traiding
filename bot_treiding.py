import os, asyncio, logging
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = os.getenv("RENDER_EXTERNAL_URL")  # webhook URL pública
PORT = int(os.getenv("PORT", 8000))

# Define comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot activo. Usa /señal.")

async def señal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aquí va tu lógica de señal (RSI, EMA, MACD)
    await update.message.reply_text("🟢 Ejemplo señal")

app_bot = ApplicationBuilder().token(TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("señal", señal))

# Flask para webhooks y health
app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "✅ OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), app_bot.bot)
    asyncio.create_task(app_bot.update_queue.put(update))
    return Response("OK", status=200)

async def run_bot():
    # inicia webhook
    await app_bot.bot.set_webhook(f"{URL}/webhook")
    await app_bot.initialize()
    await app_bot.start()
    # no se usa polling

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=PORT)
