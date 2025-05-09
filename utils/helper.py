from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup
import os

async def trigger_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
    if update.effective_message:
        fake_query = CallbackQuery(
            id="fake",
            from_user=update.effective_user,
            chat_instance="fake_instance",
            message=update.effective_message,
            data=callback_data,
        )
        fake_query._bot = context.bot  # 🛠 Attach the bot manually (private but necessary)

        fake_update = Update(update.update_id, callback_query=fake_query)
        await context.application.process_update(fake_update)

WELCOME_IMAGE_PATH = os.path.join("resources", "welcome_image.png")

async def send_dashboard_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    body_text: str,
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "Markdown"
) -> None:
    # Try to delete the previous message (useful after callback queries)
    try:
        await update.callback_query.message.delete()
    except Exception:
        pass  # It's okay if there's nothing to delete

    full_caption = f"*BOT | DASHBOARD*\n\n{body_text}"

    with open(WELCOME_IMAGE_PATH, "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=full_caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )