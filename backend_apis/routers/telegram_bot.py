# --- Telegram Bot Handlers ---
# backend_apis/routers/telegram_bot.py
import asyncio
import os
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update
import httpx
from dotenv import load_dotenv
import os
from pathlib import Path
from .ai_model import chat


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def clean_text(text: str) -> str:
    return text.replace("*", "").replace("#", "")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/tel_bot/chat",
                json={"message": user_text}
            )
            reply = response.json().get("response", clean_text(chat(user_text)))
        except Exception as e:
            reply = f"Error: {str(e)}"


    await update.message.reply_text(reply)

async def start_telegram_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run without trying to close the event loop
    await app.initialize()
    await app.start()
    print("✅ Telegram bot started and listening...")
    await app.updater.start_polling()
