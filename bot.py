import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

user_energy = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_energy:
        user_energy[user_id] = 0

    keyboard = [
        [InlineKeyboardButton("? Клик", callback_data="click")],
        [InlineKeyboardButton("?? Профиль", callback_data="profile")]
    ]

    await update.message.reply_text(
        f"Добро пожаловать в Tap Energy!\n\n"
        f"? Твоя энергия: {user_energy[user_id]}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_energy:
        user_energy[user_id] = 0

    if query.data == "click":
        user_energy[user_id] += 1
        text = f"? Ты нажал!\n\nЭнергия: {user_energy[user_id]}"

    elif query.data == "profile":
        text = f"?? Профиль\n\n? Энергия: {user_energy[user_id]}"

    keyboard = [
        [InlineKeyboardButton("? Клик", callback_data="click")],
        [InlineKeyboardButton("?? Профиль", callback_data="profile")]
    ]

    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
