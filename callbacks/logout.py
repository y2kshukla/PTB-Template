callback_data = "logout"

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from callbacks.startover import handler as startover_handler  # Import the handler to call manually
import asyncio

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    sent_message = await query.message.chat.send_message("❌ You've Logged Out! Redirecting...")

    # Wait for 3 seconds
    await asyncio.sleep(3)

    # Delete the newly sent message
    try:
        await sent_message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

    # Manually trigger the startover callback
    await startover_handler(update, context)
