import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import Message

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def main():
    print("Запуск бота...")

    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    @dp.message()
    async def echo_handler(message: Message):
        await message.answer("Бот працює!")

    # Надіслати повідомлення в чат
    await bot.send_message(chat_id=CHAT_ID, text="Бот запущено!")

    # Запустити бота і залишити процес активним
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())import os
import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start_handler(message: types.Message):
    await message.answer("Бот запущено!")

async def main():
    print("Запуск бота...")
    await bot.send_message(chat_id=CHAT_ID, text="Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
