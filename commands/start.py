command = "start"
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import helper, db

async def send_start_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard_layout = [
        [InlineKeyboardButton("Test", callback_data="startover" )],
        [
            InlineKeyboardButton("Test 1", callback_data="topup"),
            InlineKeyboardButton("Test 2", callback_data="history"),
        ],
        [InlineKeyboardButton("❌ Logout", callback_data="logout" )]
    ]

    user = update.effective_user
    username = user.username
    user_id = user.id

    user_exists = await db.check_user_exists(user_id)

    if not user_exists:
        await db.add_user(user_id, username)

        # Send the image with a caption
        await helper.send_dashboard_photo(
            update,
            context,
            body_text=f"👋 Welcome *{username}*!",
            reply_markup=InlineKeyboardMarkup(keyboard_layout),
            parse_mode="Markdown"
        )
    else:
        await helper.send_dashboard_photo(
            update,
            context,
            body_text=f"👋 Welcome Back, *{username}*!",
            reply_markup=InlineKeyboardMarkup(keyboard_layout),
            parse_mode="Markdown"
        )

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_start_message(update, context)