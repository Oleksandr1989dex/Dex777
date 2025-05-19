import time
import requests
import telebot

TOKEN = "6885132077:AAHPddxWZ8v6ZDWUzzqhhkgsvXQU1cyJQgs"
CHAT_ID = "6885132077"

bot = telebot.TeleBot(TOKEN)
last_prices = {}

def fetch_pairs():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/mexc"
        res = requests.get(url, timeout=10)
        return res.json().get("pairs", [])
    except Exception as e:
        print("Помилка отримання пар:", e)
        return []

def is_listed_on_binance(symbol):
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        res = requests.get(url, timeout=10)
        symbols = [s['symbol'] for s in res.json()["symbols"]]
        return f"{symbol}USDT" in symbols
    except:
        return False

def send_signal(data):
    message = (
        f"Token: {data['symbol']}\n"
        f"🟢Long-Spread: {data['spread']:.2f}%\n"
        f"MEXC: {data['mexc_url']}\n"
        f"DEX: {data['dex_url']}\n"
        f"MEXC: {data['mexc_price']}\n"
        f"DEX: {data['dex_price']}\n"
        f"Deposit: ✅ Withdraw: ✅\n"
        f"👍 - Profit"
    )
    bot.send_message(CHAT_ID, message)

def check_tokens():
    pairs = fetch_pairs()
    for p in pairs:
        try:
            symbol = p["baseToken"]["symbol"]
            mexc_price = float(p.get("priceNative", 0))
            dex_price = float(p.get("priceUsd", 0))
            if mexc_price == 0 or dex_price == 0:
                continue
            spread = abs(dex_price - mexc_price) / mexc_price * 100
            if spread < 7:
                continue
            if is_listed_on_binance(symbol):
                continue
            last_price = last_prices.get(symbol)
            if last_price != dex_price:
                send_signal({
                    "symbol": symbol,
                    "spread": spread,
                    "mexc_url": f"https://futures.mexc.com/exchange/{symbol}_USDT",
                    "dex_url": p["url"],
                    "mexc_price": mexc_price,
                    "dex_price": dex_price
                })
                last_prices[symbol] = dex_price
        except Exception as e:
            print("Помилка обробки токена:", e)

if __name__ == "__main__":
    print("Бот запущено...")
    while True:
        check_tokens()
        time.sleep(60)