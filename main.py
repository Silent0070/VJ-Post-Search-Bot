import os
from flask import Flask, request
from pyrogram import Client
from pyrogram.types import Update
import asyncio

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, bot)
    asyncio.get_event_loop().create_task(bot.process_update(update))
    return "ok"

async def main():
    await bot.start()
    await bot.set_webhook(f"https://YOUR-RENDER-URL.onrender.com/{BOT_TOKEN}")
    print("Webhook set successfully")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    app.run(host="0.0.0.0", port=PORT)
