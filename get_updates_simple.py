import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv(override=True)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    print("Checking updates...")
    updates = await bot.get_updates()
    for u in updates:
        if u.channel_post:
            print(f"CHANNEL: {u.channel_post.chat.title} | ID: {u.channel_post.chat.id}")
        elif u.message:
            print(f"CHAT: {u.message.chat.type} | ID: {u.message.chat.id}")

if __name__ == "__main__":
    asyncio.run(main())
