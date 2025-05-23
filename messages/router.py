# messages/router.py
from telegram import Update
from telegram.ext import ContextTypes, filters

filters = filters.TEXT & ~filters.COMMAND

from messages import sign_in  # import your handlers

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Route based on state
    if context.user_data.get("link_state"):
        await sign_in.handler(update, context)
    else:
        await update.message.reply_text("❓ Please use one of the menu options to begin.")
