import os
import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("Бот працює!")

async def main():
    print("Запуск бота...")
    await bot.send_message(CHAT_ID, "Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
