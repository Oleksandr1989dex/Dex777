import time
import requests
import telebot

TOKEN = "6885132077:AAHPddxWZ8v6ZDWUzzqhhkgsvXQU1cyJQgs"
CHAT_ID = "6885132077"

bot = telebot.TeleBot(TOKEN)
last_prices = {}

def fetch_tokens():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/mexc"
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("pairs", [])
    except Exception as e:
        print("Помилка запиту:", e)
    return []

def is_on_binance(symbol):
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        res = requests.get(url)
        data = res.json()
        symbols = [s['symbol'] for s in data['symbols']]
        return symbol + "USDT" in symbols
    except:
        return False

def check_and_send():
    tokens = fetch_tokens()
    for t in tokens:
        try:
            symbol = t["baseToken"]["symbol"]
            dex_price = float(t["priceUsd"])
            mexc_price = float(t["priceNative"])
            spread = abs(dex_price - mexc_price) / mexc_price * 100

            if spread > 7 and not is_on_binance(symbol):
                last = last_prices.get(symbol)
                if last != dex_price:
                    msg = (
                        "Token: " + symbol + "\n" +
                        "🟢Long-Spread: {:.2f}%\n".format(spread) +
                        "MEXC: https://futures.mexc.com/exchange/" + symbol + "_USDT\n" +
                        "DEX: " + t['url'] + "\n" +
                        "MEXC: " + str(mexc_price) + "\n" +
                        "DEX: " + str(dex_price) + "\n" +
                        "Deposit: ✅ Withdraw: ✅\n" +
                        "👍 - Profit"
                    )
                    bot.send_message(CHAT_ID, msg)
                    last_prices[symbol] = dex_price
        except Exception as e:
            print("Помилка обробки токена:", e)

if __name__ == "__main__":
    print("Бот запущено...")
    while True:
        check_and_send()
        time.sleep(60)