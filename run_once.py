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
load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

async def send_daily_content():
    if not TOKEN or not CHANNEL_ID:
        logger.error("Error: Credentials missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID.")
        return

    bot = Bot(token=TOKEN)
    
    # --- Part 1: Send Fact/Key Note ---
    try:
        fact_text = ""
        ai_fact = ai_service.get_ai_content("fact")
        if ai_fact:
            fact_text = f"📝 **GATE Civil Key Note**\n\n{ai_fact['fact']}"
        else:
            fact = random.choice(FACTS)
            fact_text = f"📝 **GATE Civil Key Note**\n\n{fact}"
            
        logger.info(f"Sending Fact to {CHANNEL_ID}...")
        await bot.send_message(chat_id=CHANNEL_ID, text=fact_text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Failed to send fact: {e}")

    # --- Part 2: Send Question (Quiz Poll) ---
    try:
        # Wait a bit so messages appear in order
        await asyncio.sleep(2)
        
        ai_quiz = ai_service.get_ai_content("question")
        
        if ai_quiz and 'correct_option_id' in ai_quiz:
            q = ai_quiz
            logger.info(f"Sending Quiz to {CHANNEL_ID}...")
            await bot.send_poll(
                chat_id=CHANNEL_ID,
                question=f"🏗️ {q['question']}",
                options=q['options'],
                type='quiz',
                correct_option_id=q['correct_option_id'],
                explanation=q.get('explanation', 'No explanation provided.'),
                is_anonymous=True
            )
        else:
            # Fallback to local text-based question if AI fails or returns bad format
            logger.warning("AI Quiz failed or format invalid. Falling back to local text question.")
            item = random.choice(QUESTIONS)
            text = f"🏗️ GATE Civil Question (Fallback)\n\n{item['question']}\n\n"
            for opt in item['options']:
                text += f"{opt}\n"
            text += "\n(Note: AI generation failed, so this is a static question.)"
            await bot.send_message(chat_id=CHANNEL_ID, text=text)

    except Exception as e:
        logger.error(f"Failed to send quiz: {e}")

if __name__ == "__main__":
    asyncio.run(send_daily_content())
