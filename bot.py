from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ETHERSCAN_API = "YOUR_ETHERSCAN_API_KEY"

def get_eth_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API}"
    res = requests.get(url).json()
    if res["status"] != "1":
        return None
    return int(res["result"]) / 10**18

def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    return requests.get(url).json()["ethereum"]["usd"]

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /eth WALLET_ADDRESS")
        return

    address = context.args[0]

    balance = get_eth_balance(address)
    if balance is None:
        await update.message.reply_text("❌ Invalid address or API error")
        return

    price = get_eth_price()
    usd_value = balance * price

    await update.message.reply_text(
        f"✅ ETH Wallet\n\n"
        f"Address: `{address}`\n"
        f"Balance: {balance:.4f} ETH\n"
        f"USD Value: ${usd_value:,.2f}",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("eth", eth))
app.run_polling()
