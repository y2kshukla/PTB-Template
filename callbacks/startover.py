from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils import helper

callback_data = "startover"

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_layout = [
        [InlineKeyboardButton("Test", callback_data="startover" )],
        [
            InlineKeyboardButton("Test 1", callback_data="topup"),
            InlineKeyboardButton("Test 2", callback_data="history"),
        ],
        [InlineKeyboardButton("❌ Logout", callback_data="logout" )]
    ]

    # Send the image with a caption
    await helper.send_dashboard_photo(
        update,
        context,
        body_text=f"👋 Welcome back!\n\n You are logged in.",
        reply_markup=InlineKeyboardMarkup(keyboard_layout),
        parse_mode="Markdown"
    )

