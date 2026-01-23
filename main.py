import os
import asyncio
from telegram.ext import Application, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import uvicorn
from backend import app as fastapi_app

BOT_TOKEN = os.getenv("BOT_TOKEN")


# -------- TELEGRAM BOT --------
async def start(update, context):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🎮 Play Bingo",
            web_app=WebAppInfo(url="https://bingo-webapp.onrender.com")
        )]
    ])
    await update.message.reply_text(
        "Welcome to Bingo 🎉\nTap below to play:",
        reply_markup=keyboard
    )


async def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start()
    await application.bot.initialize()
    await application.updater.start_polling()
    await application.wait_until_closed()


# -------- MAIN ENTRY --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=port
    )
