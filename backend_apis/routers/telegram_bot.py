# backend_apis/routers/telegram_bot.py

import os
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update
from dotenv import load_dotenv
from pathlib import Path
import httpx
from .ai_model import chat

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Build the Telegram app once to reuse in FastAPI
telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


def clean_text(text: str) -> str:
    return text.replace("*", "").replace("#", "")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://insurelink.onrender.com/chat/tel_bot",
                json={"message": user_text}
            )
            data = response.json()
            reply = data.get("response") or "⚠️ No reply from server."
        except Exception as e:
            reply = f"❌ Error: {str(e)}"

    await update.message.reply_text(reply)



# Register handler
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


async def configure_webhook():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    print("✅ Telegram webhook configured")
