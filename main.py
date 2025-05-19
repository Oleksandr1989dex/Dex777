import os
import time
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

def get_token_data():
    # Псевдодані для прикладу, заміни на реальні API-запити
    return {
        "token": "MOODENG",
        "spread": "7.23%",
        "mexc_link": "https://futures.mexc.com/exchange/MOODENG_USDT",
        "dex_link": "https://dexscreener.com/solana/22wrmytj8x2trvqen3fxxi2r4rn6jdhwomtpssmn8rud",
        "mexc_price": "0.310",
        "dex_price": "0.327",
        "deposit": "✅",
        "withdraw": "✅",
        "summary": "👍 - Profit"
    }

def send_update():
    data = get_token_data()
    message = (
        f"Token: {data['token']}\n"
        f"🟢Long-Spread: {data['spread']}\n"
        f"MEXC: {data['mexc_link']}\n"
        f"DEX: {data['dex_link']}\n"
        f"MEXC: {data['mexc_price']}\n"
        f"DEX: {data['dex_price']}\n"
        f"Deposit: {data['deposit']} Withdraw: {data['withdraw']}\n"
        f"{data['summary']}"
    )
    bot.send_message(CHAT_ID, message)

if __name__ == "__main__":
    print("Запуск бота...")
    while True:
        try:
            send_update()
            time.sleep(60)
        except Exception as e:
            print("Помилка:", e)
            time.sleep(10)
