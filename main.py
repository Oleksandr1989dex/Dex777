
import os
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN Р°Р±Рѕ CHAT_ID РЅРµ Р·Р°РґР°РЅРѕ Сѓ СЃРµСЂРµРґРѕРІРёС‰С–!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Р‘РѕС‚ РїСЂР°С†СЋС”!")

async def fetch_tokens():
    url = "https://api.dexscreener.com/latest/dex/pairs/mexc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tokens = data.get("pairs", [])
        result = []
        for t in tokens:
            try:
                dex_price = float(t["priceUsd"])
                mexc_price = float(t.get("market", {}).get("price", 0))
                spread = abs(dex_price - mexc_price) / dex_price * 100
                if spread >= 7:
                    result.append({
                        "symbol": t["baseToken"]["symbol"],
                        "dex_price": dex_price,
                        "mexc_price": mexc_price,
                        "spread": spread,
                        "dex_url": t["url"],
                        "mexc_url": f"https://futures.mexc.com/exchange/{t['baseToken']['symbol']}_USDT"
                    })
            except Exception:
                continue
        return result
    return []

async def check_tokens():
    while True:
        try:
            tokens = await fetch_tokens()
            for token in tokens:
                msg = (
                    f"Token: <b>{token['symbol']}</b> рџџў\n"
                    f"Long-Spread: <b>{token['spread']:.2f}%</b>\n"
                    f"MEXC: <a href='{token['mexc_url']}'>link</a>\n"
                    f"DEX: <a href='{token['dex_url']}'>link</a>\n"
                    f"MEXC: <b>{token['mexc_price']}</b>\n"
                    f"DEX: <b>{token['dex_price']}</b>\n"
                    f"Deposit: вњ… Withdraw: вњ…\n"
                    f"рџ‘Ќ - Profit"
                )
                await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"РџРѕРјРёР»РєР° РїРµСЂРµРІС–СЂРєРё С‚РѕРєРµРЅС–РІ: {e}")
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(check_tokens())
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())# Головний файл бота
print('Запуск бота...')
