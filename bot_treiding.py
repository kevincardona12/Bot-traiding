from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

# 🔐 TOKEN de tu bot (reemplázalo con el tuyo)
TOKEN = "8076387869:AAEZus_gajoNq2Rof4947w0m2tacpIb6Xds"

# 💬 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy tu bot de señales de trading.\n\n"
        "Usa /ayuda para ver los comandos disponibles."
    )

# 💬 Comando /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Comandos disponibles:\n"
        "/oro – Precio del oro\n"
        "/señal – Señal técnica (compra/venta)\n"
        "/btc – Precio de Bitcoin\n"
        "/eurusd – Precio EUR/USD\n"
        "/ayuda – Ver esta lista"
    )

# 📈 Comando /oro
async def oro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("XAUUSD=X", period="1d", interval="15m")
    last = data["Close"].iloc[-1]
    await update.message.reply_text(f"🟡 Oro (XAU/USD): {round(last, 2)} USD")

# 📉 Comando /btc
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("BTC-USD", period="1d", interval="15m")
    last = data["Close"].iloc[-1]
    await update.message.reply_text(f"₿ Bitcoin (BTC/USD): {round(last, 2)} USD")

# 💱 Comando /eurusd
async def eurusd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = yf.download("EURUSD=X", period="1d", interval="15m")
    last = data["Close"].iloc[-1]
    await update.message.reply_text(f"💶 EUR/USD: {round(last, 4)}")

# 🔍 Comando /señal
async def señal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df = yf.download("XAUUSD=X", period="5d", interval="15m")
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()

    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    exp1 = df["Close"].ewm(span=12, adjust=False).mean()
    exp2 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    last = df.iloc[-1]
    signal = "⚪ NEUTRAL"

    if last["EMA20"] > last["EMA50"] and last["RSI"] < 70 and last["MACD"] > last["Signal
