{\rtf1\fbidis\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil\fcharset0 Calibri;}{\f1\fnil\fcharset1 Segoe UI Symbol;}{\f2\fnil Calibri;}{\f3\fnil\fcharset1 Segoe UI Symbol;}{\f4\fnil\fcharset1 Segoe UI Emoji;}}
{\*\generator Riched20 10.0.19041}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\f0\fs22\lang9 import random\par
from telegram import (\par
    Update,\par
    InlineKeyboardButton,\par
    InlineKeyboardMarkup,\par
    ReplyKeyboardMarkup\par
)\par
from telegram.ext import (\par
    ApplicationBuilder,\par
    CommandHandler,\par
    CallbackQueryHandler,\par
    MessageHandler,\par
    ContextTypes,\par
    filters\par
)\par
\par
# ===============================\par
# CONFIG\par
# ===============================\par
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"\par
\par
# ===============================\par
# GAME STORAGE\par
# ===============================\par
games = \{\}  # chat_id -> game state\par
balances = \{\}  # user_id -> coins (demo only)\par
\par
# ===============================\par
# UI MENUS\par
# ===============================\par
def main_menu():\par
    return ReplyKeyboardMarkup(\par
        [\par
            ["\f1\u-10180?\u-8274?\f2  \f0 Play Now"],\par
            ["\f1\u-10179?\u-9040?\f2  \f0 Check Balance", "\f1\u-10179?\u-9000?\f2  \f0 Game Instruction"],\par
            ["\f1\u-10179?\u-9037?\f2  \f0 Deposit", "\f1\u-10179?\u-8994?\f2  \f0 Contact Us"]\par
        ],\par
        resize_keyboard=True\par
    )\par
\par
# ===============================\par
# BINGO HELPERS\par
# ===============================\par
def generate_card():\par
    card = []\par
    for col in range(5):\par
        nums = random.sample(range(col * 15 + 1, col * 15 + 16), 5)\par
        card.append(nums)\par
    card[2][2] = "FREE"\par
    return list(map(list, zip(*card)))\par
\par
def empty_marks():\par
    marks = [[False]*5 for _ in range(5)]\par
    marks[2][2] = True\par
    return marks\par
\par
def check_bingo(m):\par
    for row in m:\par
        if all(row):\par
            return True\par
    for col in zip(*m):\par
        if all(col):\par
            return True\par
    if all(m[i][i] for i in range(5)):\par
        return True\par
    if all(m[i][4-i] for i in range(5)):\par
        return True\par
    return False\par
\par
def build_keyboard(card, marks):\par
    keyboard = []\par
    for r in range(5):\par
        row = []\par
        for c in range(5):\par
            text = f"\f3\u9989?\f0\{card[r][c]\}" if marks[r][c] else str(card[r][c])\par
            row.append(InlineKeyboardButton(text, callback_data=f"mark_\{r\}_\{c\}"))\par
        keyboard.append(row)\par
    return InlineKeyboardMarkup(keyboard)\par
\par
# ===============================\par
# COMMANDS\par
# ===============================\par
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    user_id = update.effective_user.id\par
    balances.setdefault(user_id, 0)\par
\par
    await update.message.reply_text(\par
        "\f1\u-10180?\u-8311?\f2  \f0 *Welcome to Bingo Bot!*\\nPlay and have fun \f1\u-10180?\u-8273?\f0 ",\par
        parse_mode="Markdown",\par
        reply_markup=main_menu()\par
    )\par
\par
async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    chat_id = update.effective_chat.id\par
    games[chat_id] = \{\par
        "numbers": random.sample(range(1, 76), 75),\par
        "called": [],\par
        "players": \{\}\par
    \}\par
    await update.message.reply_text("\f1\u-10180?\u-8273?\f2  \f0 New Bingo game started!")\par
\par
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    chat_id = update.effective_chat.id\par
    user = update.effective_user\par
\par
    if chat_id not in games:\par
        await update.message.reply_text("\f3\u10060?\f2  \f0 No active game.")\par
        return\par
\par
    game = games[chat_id]\par
    if user.id in game["players"]:\par
        await update.message.reply_text("\f4\u8505?\u-497?\f2  \f0 You already joined.")\par
        return\par
\par
    game["players"][user.id] = \{\par
        "card": generate_card(),\par
        "marks": empty_marks()\par
    \}\par
\par
    await update.message.reply_text(\par
        f"\f3\u9989?\f2  \f0\{user.first_name\} joined Bingo!\\nUse /card to play."\par
    )\par
\par
async def card(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    chat_id = update.effective_chat.id\par
    user_id = update.effective_user.id\par
\par
    game = games.get(chat_id)\par
    if not game or user_id not in game["players"]:\par
        await update.message.reply_text("\f3\u10060?\f2  \f0 You are not in the game.")\par
        return\par
\par
    player = game["players"][user_id]\par
    await update.message.reply_text(\par
        "\f1\u-10180?\u-8289?\f2  \f0 *Your Bingo Card*",\par
        parse_mode="Markdown",\par
        reply_markup=build_keyboard(player["card"], player["marks"])\par
    )\par
\par
async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    chat_id = update.effective_chat.id\par
    game = games.get(chat_id)\par
\par
    if not game or not game["numbers"]:\par
        await update.message.reply_text("\f3\u10060?\f2  \f0 No numbers left.")\par
        return\par
\par
    num = game["numbers"].pop()\par
    game["called"].append(num)\par
    await update.message.reply_text(f"\f1\u-10179?\u-8926?\f2  \f0 *Number Called:* \{num\}", parse_mode="Markdown")\par
\par
# ===============================\par
# INLINE BUTTON HANDLER\par
# ===============================\par
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    query = update.callback_query\par
    await query.answer()\par
\par
    chat_id = query.message.chat.id\par
    user_id = query.from_user.id\par
    data = query.data\par
\par
    if data.startswith("mark_"):\par
        game = games.get(chat_id)\par
        if not game or user_id not in game["players"]:\par
            return\par
\par
        _, r, c = data.split("_")\par
        r, c = int(r), int(c)\par
\par
        player = game["players"][user_id]\par
        card = player["card"]\par
        marks = player["marks"]\par
\par
        if card[r][c] != "FREE" and card[r][c] not in game["called"]:\par
            await query.answer("\f3\u10060?\f2  \f0 Number not called yet", show_alert=True)\par
            return\par
\par
        marks[r][c] = True\par
\par
        if check_bingo(marks):\par
            await query.message.edit_text(\par
                f"\f1\u-10180?\u-8311?\f2  \f0 *BINGO!*\\nWinner: \{query.from_user.first_name\}",\par
                parse_mode="Markdown"\par
            )\par
            games.pop(chat_id)\par
            return\par
\par
        await query.message.edit_reply_markup(\par
            reply_markup=build_keyboard(card, marks)\par
        )\par
\par
    elif data == "deposit_sms":\par
        await query.message.reply_text(\par
            "\f1\u-10179?\u-8975?\f2  \f0 *Manual Deposit*\\n"\par
            "Send SMS to: XXXX\\n"\par
            "Then send transaction ID here.",\par
            parse_mode="Markdown"\par
        )\par
\par
# ===============================\par
# TEXT BUTTON HANDLER\par
# ===============================\par
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):\par
    text = update.message.text\par
    user_id = update.effective_user.id\par
\par
    if text == "\f1\u-10180?\u-8274?\f2  \f0 Play Now":\par
        await update.message.reply_text(\par
            "\f1\u-10180?\u-8274?\f2  \f0 *Bingo Commands*\\n"\par
            "/newgame \f2\endash  Start game\\n"\par
            "/join \endash  Join game\\n"\par
            "/call \endash  Call number\\n"\par
            "/card \endash  Show card",\par
            parse_mode="Markdown"\par
        )\par
\par
    elif text == "\f1\u-10179?\u-9040?\f2  \f0 Check Balance":\par
        await update.message.reply_text(\par
            f"\f1\u-10179?\u-9040?\f2  \f0 Your balance: \{balances.get(user_id, 0)\} coins"\par
        )\par
\par
    elif text == "\f1\u-10179?\u-9000?\f2  \f0 Game Instruction":\par
        await update.message.reply_text(\par
            "\f1\u-10179?\u-9000?\f2  \f0 *How to Play Bingo*\\n"\par
            "1. Start game\\n"\par
            "2. Join game\\n"\par
            "3. Mark numbers\\n"\par
            "4. Get BINGO!",\par
            parse_mode="Markdown"\par
        )\par
\par
    elif text == "\f1\u-10179?\u-9037?\f2  \f0 Deposit":\par
        await update.message.reply_text(\par
            "Choose your deposit method:",\par
            reply_markup=InlineKeyboardMarkup([\par
                [InlineKeyboardButton("\f1\u-10179?\u-8975?\f2  \f0 Manual (SMS)", callback_data="deposit_sms")]\par
            ])\par
        )\par
\par
    elif text == "\f1\u-10179?\u-8994?\f2  \f0 Contact Us":\par
        await update.message.reply_text("\f1\u-10179?\u-8994?\f2  \f0 Support: @YourSupportUsername")\par
\par
# ===============================\par
# SET SIDE MENU COMMANDS\par
# ===============================\par
async def set_commands(app):\par
    await app.bot.set_my_commands([\par
        ("start", "Start the bot"),\par
        ("newgame", "Start a Bingo game"),\par
        ("join", "Join Bingo"),\par
        ("call", "Call a number"),\par
        ("card", "Show Bingo card"),\par
    ])\par
\par
# ===============================\par
# START BOT\par
# ===============================\par
app = ApplicationBuilder().token(BOT_TOKEN).build()\par
app.post_init = set_commands\par
\par
app.add_handler(CommandHandler("start", start))\par
app.add_handler(CommandHandler("newgame", newgame))\par
app.add_handler(CommandHandler("join", join))\par
app.add_handler(CommandHandler("call", call))\par
app.add_handler(CommandHandler("card", card))\par
\par
app.add_handler(CallbackQueryHandler(inline_handler))\par
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))\par
\par
print("\f1\u-10178?\u-8938?\f2  \f0 Bingo Bot is running...")\par
app.run_polling()\par
}
 