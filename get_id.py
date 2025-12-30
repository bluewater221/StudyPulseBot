import logging
import os
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv(override=True)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"Debug: Using Token starting with {TOKEN[:10]}...")

async def get_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prints the Chat ID of any message received."""
    if update.channel_post:
        print(f"\n\n📢 CHANNEL NAME: {update.channel_post.chat.title}")
        print(f"🆔 CHANNEL ID: {update.channel_post.chat.id}\n")
        print("✅ Copy this ID and paste it into the chat with the agent.\n")
    elif update.message:
        print(f"\n\n💬 CHAT TYPE: {update.message.chat.type}")
        print(f"🆔 CHAT ID: {update.message.chat.id}\n")

def main() -> None:
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env")
        return

    print("🤖 Bot is listening... Please post a message in your 'Civil' channel now!")
    
    application = Application.builder().token(TOKEN).build()
    
    # Listen for channel posts and regular messages
    application.add_handler(MessageHandler(filters.ALL, get_channel_id))
    
    application.run_polling()

if __name__ == "__main__":
    main()
