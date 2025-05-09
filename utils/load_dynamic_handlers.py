import pathlib
import importlib.util
import logging
from telegram.ext import MessageHandler, filters
from messages.router import handler as message_router_handler

logger = logging.getLogger(__name__)

def load_dynamic_handlers(application, folder: str, type_: str = "command"):
    handlers = []
    base_path = pathlib.Path(folder)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router_handler))

    # Walk through all files in the folder and subfolders
    for file in base_path.rglob("*.py"):
        if file.name.startswith("__"):
            continue  # Skip __init__.py and similar

        # Handle module import path correctly for nested directories
        relative_path = file.relative_to(base_path)  # Get the relative path to the base folder
        module_name = f"{folder.replace('/', '.')}.{relative_path.with_suffix('').__str__().replace('/', '.')}"
        
        spec = importlib.util.spec_from_file_location(module_name, file.resolve())
        if not spec or not spec.loader:
            logger.warning(f"Could not load {module_name}")
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "handler"):
            if type_ == "command" and hasattr(module, "command"):
                handlers.append(("command", module.command, module.handler))
            elif type_ == "callback" and hasattr(module, "callback_data"):
                handlers.append(("callback", module.callback_data, module.handler))
            else:
                logger.warning(f"{file.name} is missing required attributes for type '{type_}'.")
        else:
            logger.warning(f"{file.name} does not define a 'handler' function.")

    return handlers
