from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from callbacks.startover import handler as startover_handler  # Import the handler to call manually
from utils import helper

AWAITING_USERNAME = "awaiting_username"
AWAITING_PASSWORD = "awaiting_password"

cancel_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("❌ Cancel", callback_data="startover")]
])

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    state = context.user_data.get("link_state")

    if state == AWAITING_USERNAME:
        context.user_data["link_username"] = text
        username = context.user_data.get("link_username")
        context.user_data["link_state"] = AWAITING_PASSWORD
        await update.message.reply_text(
            "TestBot | LOGIN\n\n"
            f"1️⃣ Username: {username}\n\n"
            "2️⃣ Password: \n\n"
            "💬 Please input your password now",
            reply_markup=cancel_keyboard,
            parse_mode="Markdown"
        )

    elif state == AWAITING_PASSWORD:
        context.user_data["link_password"] = text
        username = context.user_data.get("link_username")
        password = context.user_data.get("link_password")

        user_id = update.effective_user.id  # <-- GET USER ID HERE

        for key in ["link_state", "link_username", "link_password"]:
            context.user_data.pop(key, None)

    else:
        await update.message.reply_text(
            "❓ Please start by clicking 'Link Account'.",
            reply_markup=cancel_keyboard
        )
