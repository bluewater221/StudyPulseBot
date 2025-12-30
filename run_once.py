import asyncio
import os
import random
import logging
from telegram import Bot
from dotenv import load_dotenv
import ai_service
from content import QUESTIONS, FACTS, FORMULAS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env (actions will provide these)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

async def send_daily_content():
    if not TOKEN or not CHANNEL_ID:
        logger.error("Error: Credentials missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID.")
        return

    bot = Bot(token=TOKEN)
    
    # 1. Choose Type
    msg_type = random.choice(["question", "fact", "formula"])
    message_text = ""

    # 2. Generate Content (Try AI first, fallback to local)
    try:
        if msg_type == "question":
            ai_content = ai_service.get_ai_content("question")
            if ai_content:
                item = ai_content
                text = f"🏗️ GATE Civil Question (AI Generated)\n\n{item['question']}\n\n"
                for opt in item['options']:
                    text += f"{opt}\n"
                text += f"\nReply with A, B, C, or D. Answer will be revealed next hour.\n\n(Debugging Answer: {item.get('answer')})"
                message_text = text
            else:
                item = random.choice(QUESTIONS)
                text = f"🏗️ GATE Civil Question\n\n{item['question']}\n\n"
                for opt in item['options']:
                    text += f"{opt}\n"
                text += "\nReply with A, B, C, or D. Answer will be revealed next hour."
                message_text = text

        elif msg_type == "fact":
            ai_content = ai_service.get_ai_content("fact")
            if ai_content:
                message_text = f"📝 GATE Civil Key Note (AI Generated)\n\n{ai_content['fact']}"
            else:
                fact = random.choice(FACTS)
                message_text = f"📝 GATE Civil Key Note\n\n{fact}"

        else: # formula
            ai_content = ai_service.get_ai_content("formula")
            if ai_content:
                item = ai_content
                message_text = f"📐 GATE Civil Formula (AI Generated)\n\n{item['title']}\n{item['formula']}\n{item['explanation']}"
            else:
                item = random.choice(FORMULAS)
                message_text = f"📐 GATE Civil Formula\n\n{item['title']}\n{item['formula']}\n{item['explanation']}"

        # 3. Send
        logger.info(f"Sending {msg_type} to {CHANNEL_ID}...")
        await bot.send_message(chat_id=CHANNEL_ID, text=message_text)
        logger.info("Message sent successfully.")

    except Exception as e:
        logger.error(f"Failed to send message: {e}")

if __name__ == "__main__":
    asyncio.run(send_daily_content())
