import logging
import os
from utils import load_dynamic_handlers, db
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    token = f"{os.getenv('BOT_TOKEN')}";
    print(token)
    if not token:
        raise ValueError("BOT_TOKEN is missing!")

    application = Application.builder().token(token).build()

    # === Load and register handlers === #
    for type_ in ["command", "callback", "message"]:
        folder = f"{type_}s"  # expects 'commands/', 'callbacks/', 'messages/'
        handlers = load_dynamic_handlers(application, folder, type_)

        for kind, key, handler in handlers:
            if kind == "command":
                logger.info(f"Registering command /{key}")
                application.add_handler(CommandHandler(key, handler))

            elif kind == "callback":
                logger.info(f"Registering callback handler for '{key}'")
                application.add_handler(CallbackQueryHandler(handler, pattern=f"^{key}$"))

            elif kind == "message":
                logger.info(f"Registering message handler with filters: {key}")
                application.add_handler(MessageHandler(key, handler))

    application.run_polling()

if __name__ == "__main__":
    main()
