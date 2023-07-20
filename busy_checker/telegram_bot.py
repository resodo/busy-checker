import os

import telegram

# Telegram Bot Token and Chat ID
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
if bot_token is None:
    raise ValueError("Environment variable 'TELEGRAM_BOT_TOKEN' is not set")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")
if chat_id is None:
    raise ValueError("Environment variable 'TELEGRAM_CHAT_ID' is not set")

# Create a Telegram bot instance
bot = telegram.Bot(token=bot_token)


# Send message to Telegram bot
async def send_message(message):
    await bot.send_message(chat_id=chat_id, text=message)
