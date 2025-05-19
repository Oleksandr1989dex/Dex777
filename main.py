import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Бот запущено. Очікуйте повідомлення кожну хвилину.")

async def send_periodic_message():
    await bot.wait_until_ready()
    while True:
        try:
            text = (
                "Token: MOODENG\n"
                "🟢Long-Spread: 5.01%\n"
                "MEXC: https://futures.mexc.com/exchange/MOODENG_USDT\n"
                "DEX: https://dexscreener.com/solana/22wrmytj8x2trvqen3fxxi2r4rn6jdhwomtpssmn8rud\n"
                "MEXC: 0.310605\n"
                "DEX: 0.327\n"
                "Deposit: ✅ Withdraw: ✅\n"
                "👍 - Profit"
            )
            await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print("Error sending message:", e)
        await asyncio.sleep(60)

async def on_startup(_):
    asyncio.create_task(send_periodic_message())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)