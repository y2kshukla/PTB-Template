command = "reboot"

from telegram import Update
from telegram.ext import ContextTypes
from utils.middleware import with_middlewares
from utils.auth import require_admin

@with_middlewares(require_admin)
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #TODO: Remove this command later on, it's only for testing Middlewares
    await update.message.reply_text("✅ Rebooting system... (not really 😄 Please remove this later on!)")
