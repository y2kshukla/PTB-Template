# Telegram Bot Template

This is a template for building Telegram bots using the `python-telegram-bot` library. It provides a modular structure for handling commands, callbacks, and messages, making it easy to extend and maintain.

## Features

- **Commands**: Define bot commands in the `commands/` folder. Each command is automatically loaded and registered with the bot.
- **Callbacks**: Define callback query handlers in the `callbacks/` folder. These are also automatically loaded and registered.
- **Messages**: Handle text messages dynamically using the `messages/` folder. A router is provided to manage message states.
- **Resources**: Store static files like images in the `resources/` folder. For example, the bot uses a welcome image stored here.
- **Auto-loading**: Commands and callbacks are automatically discovered and registered at runtime, reducing manual setup.

## Folder Structure

- `commands/`: Contains command handlers. Each file should define a `command` variable (the command name) and a `handler` function.
- `callbacks/`: Contains callback query handlers. Each file should define a `callback_data` variable (the callback identifier) and a `handler` function.
- `messages/`: Contains message handlers. The `router.py` file routes messages based on user state.
- `resources/`: Stores static files like images or other assets.
- `utils/`: Contains utility functions and middleware for authentication, database connections, and dynamic handler loading.
- `main.py`: The entry point of the bot. It initializes the bot, loads handlers, and starts polling.

## How It Works

1. **Auto-loading Handlers**:
   - The `utils/load_dynamic_handlers.py` script dynamically loads handlers from the `commands/` and `callbacks/` folders.
   - Each handler file must define the required attributes (`command` or `callback_data`) to be registered automatically.

2. **Message Routing**:
   - Messages are routed through the `messages/router.py` file.
   - The router determines the appropriate handler based on the user's state.

3. **Resources**:
   - Static assets like images are stored in the `resources/` folder.
   - For example, the bot uses a welcome image (`resources/welcome_image.png`) when sending dashboard messages.

## Getting Started

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt