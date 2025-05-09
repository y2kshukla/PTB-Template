from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

def with_middlewares(*middlewares):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            for middleware in middlewares:
                allowed = await middleware(update, context)
                if allowed is False:
                    return
            await func(update, context)
        return wrapper
    return decorator
