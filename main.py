import os
import threading
import asyncio
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# --------------------
# TELEGRAM BOT (SAFE FOR THREAD)
# --------------------

async def telegram_main():
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton(
                    "🎮 Play Bingo",
                    web_app=WebAppInfo(
                        url="https://bingo-bot--romeshewa5.replit.app/webapp/index.html"
                    )
                )
            ]
        ]
        await update.message.reply_text(
            "Welcome to Bingo 🎉",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("🤖 Telegram bot running...")

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # keep the bot alive forever
    await asyncio.Event().wait()


def run_telegram():
    asyncio.run(telegram_main())


# start telegram bot in background thread
threading.Thread(target=run_telegram, daemon=True).start()

# --------------------
# FASTAPI (MAIN PROCESS)
# --------------------

if __name__ == "__main__":
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        log_level="info"
    )
