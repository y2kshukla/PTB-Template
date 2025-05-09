import os
from telegram import Update
from telegram.ext import ContextTypes

ADMIN_IDS = set(map(int, os.getenv("ADMIN_IDS", "").split(",")))  # from .env

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def require_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return False
    return True
