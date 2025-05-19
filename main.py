import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

TELEGRAM_TOKEN = "6885132077:AAH..."
CHAT_ID = "123456789"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="Бот успішно запущений.")
    while True:
        # Тут буде логіка перевірки токенів з DEX Screener
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
