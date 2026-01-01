import asyncio
import os
import random
import logging
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv
import ai_service
from content import QUESTIONS, FACTS, FORMULAS, MOTIVATIONAL_MESSAGES, STUDY_TIPS, EXERCISE_TIPS, HYGIENE_TIPS, GENERAL_HEALTH_TIPS, LANGUAGE_FALLBACKS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load env (actions will provide these)
load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Formatting helpers
def format_separator(char: str = "━", length: int = 20) -> str:
    return char * length

def get_topic_emoji(topic: str) -> str:
    """Get emoji for topic."""
    emojis = {
        "SM": "🏔️", "FM": "💧", "SA": "🏗️", "RCC": "🧱",
        "STEEL": "🔩", "GEO": "🗺️", "ENV": "🌿", "TRANS": "🛣️",
        "HYDRO": "🌊", "CONST": "📋"
    }
    return emojis.get(topic, "📚")

async def send_daily_content():
    """Send daily content to the channel."""
    if not TOKEN or not CHANNEL_ID:
        logger.error("Error: Credentials missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID.")
        return

    bot = Bot(token=TOKEN)
    current_hour = datetime.now().hour
    
    # --- Determine content type based on schedule ---
    # Morning (6-10): Motivation + Formula
    # Midday (11-14): Question
    # Afternoon (15-18): Fact
    # Evening (19-22): Question
    # Night (23-5): Tip
    
    try:
        if 6 <= current_hour <= 10:
            # Morning routine: Motivation, Formula, Exercise, Hygiene, Health
            await send_motivation(bot)
            await asyncio.sleep(2)
            await send_formula(bot)
            await asyncio.sleep(2)
            await send_exercise_tip(bot)
            await asyncio.sleep(2)
            await send_hygiene_tip(bot)
            await asyncio.sleep(2)
            await send_wellness_tip(bot)
        elif 11 <= current_hour <= 14:
            # Midday quiz
            await send_quiz(bot)
        elif 15 <= current_hour <= 18:
            # Afternoon fact
            await send_fact(bot)
        elif 19 <= current_hour <= 22:
            # Evening quiz
            await send_quiz(bot)
        else:
            # Night: Language lesson + tip
            await send_language_lesson(bot)
            await asyncio.sleep(2)
            await send_tip(bot)
            
    except Exception as e:
        logger.error(f"Error in send_daily_content: {e}", exc_info=True)

async def send_motivation(bot: Bot):
    """Send a motivational message."""
    try:
        message = random.choice(MOTIVATIONAL_MESSAGES)
        text = f"""
{format_separator()}
🌅 **Good Morning, GATE Aspirant!**
{format_separator()}

{message}

_Start your day with preparation!_ 💪
{format_separator()}
"""
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent motivation message")
    except Exception as e:
        logger.error(f"Failed to send motivation: {e}")

async def send_tip(bot: Bot):
    """Send a study tip."""
    try:
        tip = random.choice(STUDY_TIPS)
        text = f"""
{format_separator()}
💡 **GATE Prep Tip**
{format_separator()}

{tip}

_Apply this in your preparation!_ 📚
{format_separator()}
"""
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent study tip")
    except Exception as e:
        logger.error(f"Failed to send tip: {e}")

async def send_exercise_tip(bot: Bot):
    """Send a single exercise tip."""
    try:
        tip = random.choice(EXERCISE_TIPS)
        text = f"""
{format_separator()}
🏃 **Morning Exercise Tip**
{format_separator()}

{tip['name']}

{tip['desc']}

{format_separator()}
_Take a break and move!_ 💪
"""
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent exercise tip")
    except Exception as e:
        logger.error(f"Failed to send exercise tip: {e}")

async def send_hygiene_tip(bot: Bot):
    """Send a single hygiene tip."""
    try:
        tip = random.choice(HYGIENE_TIPS)
        text = f"""
{format_separator()}
🧼 **Hygiene Reminder**
{format_separator()}

{tip['name']}

{tip['desc']}

{format_separator()}
_Stay fresh, stay focused!_ ✨
"""
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent hygiene tip")
    except Exception as e:
        logger.error(f"Failed to send hygiene tip: {e}")

async def send_wellness_tip(bot: Bot):
    """Send a single wellness tip."""
    try:
        tip = random.choice(GENERAL_HEALTH_TIPS)
        text = f"""
{format_separator()}
🍎 **Daily Wellness Tip**
{format_separator()}

{tip['name']}

{tip['desc']}

{format_separator()}
_Your health matters!_ 🌟
"""
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent wellness tip")
    except Exception as e:
        logger.error(f"Failed to send wellness tip: {e}")

async def send_language_lesson(bot: Bot):
    """Send a micro-language lesson."""
    try:
        ai_content = await ai_service.get_ai_content("language")
        if ai_content:
            item = ai_content
        else:
            item = random.choice(LANGUAGE_FALLBACKS)
            
        text = f"""
{format_separator()}
🌐 **Daily Language Micro-Learning** ({item['language']})
{format_separator()}

🔤 **Word**: {item['word']}
🗣️ **Phonetic**: {item['phonetic']}
📖 **Meaning**: {item['meaning']}

📝 **Usage**: {item['usage']}
💡 **Tip**: {item['tip']}

{format_separator()}
_Learn one word every day!_ 🚀
{format_separator()}
"""
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent language lesson")
    except Exception as e:
        logger.error(f"Failed to send language lesson: {e}")

async def send_fact(bot: Bot):
    """Send a key fact/note."""
    try:
        ai_fact = await ai_service.get_ai_content("fact")
        
        if ai_fact:
            topic_code = ai_fact.get('topic', 'General')
            topic_name = ai_service.get_topic_name(topic_code)
            source = ai_fact.get('source', 'Civil Engineering Standards')
            visual = ai_fact.get('visual_hint', '')
            visual_text = f"\n🖼️ **Visual**: _{visual}_\n" if visual else ""
            
            text = f"""
{format_separator()}
📝 **GATE Civil Key Note**
{format_separator()}

{get_topic_emoji(topic_code)} **Topic**: {topic_name}

💡 {ai_fact['fact']}
{visual_text}
📚 **Source**: {source}

{format_separator()}
_Save this for revision!_ 📌
"""
        else:
            fact = random.choice(FACTS)
            text = f"""
{format_separator()}
📝 **GATE Civil Key Note**
{format_separator()}

💡 {fact}

{format_separator()}
"""
        
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent fact message")
        
    except Exception as e:
        logger.error(f"Failed to send fact: {e}")

async def send_formula(bot: Bot):
    """Send a formula."""
    try:
        ai_formula = await ai_service.get_ai_content("formula")
        
        if ai_formula:
            topic_code = ai_formula.get('topic', 'General')
            topic_name = ai_service.get_topic_name(topic_code)
            source = ai_formula.get('source', 'Engineers Reference')
            visual = ai_formula.get('visual_hint', '')
            visual_text = f"\n🖼️ **Visual**: _{visual}_\n" if visual else ""
            
            text = f"""
{format_separator()}
📐 **GATE Civil Formula**
{format_separator()}

{get_topic_emoji(topic_code)} **Topic**: {topic_name}

📌 **{ai_formula['title']}**

`{ai_formula['formula']}`

📖 {ai_formula['explanation']}
{visual_text}
📚 **Source**: {source}

{format_separator()}
_Memorize this formula!_ 🧠
"""
        else:
            item = random.choice(FORMULAS)
            topic_code = item.get('topic', 'General')
            text = f"""
{format_separator()}
📐 **GATE Civil Formula**
{format_separator()}

{get_topic_emoji(topic_code)} **{item['title']}**

`{item['formula']}`

📖 {item['explanation']}

{format_separator()}
"""
        
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
        logger.info("Sent formula message")
        
    except Exception as e:
        logger.error(f"Failed to send formula: {e}")

async def send_quiz(bot: Bot):
    """Send a quiz poll using native Telegram quiz."""
    try:
        # Try AI-generated question first
        ai_quiz = await ai_service.get_ai_content("question")
        
        if ai_quiz and 'correct_option_id' in ai_quiz and 'options' in ai_quiz:
            question = ai_quiz
            topic_code = question.get('topic', 'General')
            topic_name = ai_service.get_topic_name(topic_code)
            difficulty = question.get('difficulty', 'medium')
            
            # Validate options (Telegram requires 2-10 options)
            if len(question['options']) >= 2 and len(question['options']) <= 10:
                # Ensure question length is within Telegram limits (255 chars for poll question)
                poll_question = question['question']
                if len(poll_question) > 250:
                    poll_question = poll_question[:247] + "..."
                
                # Format question with topic and difficulty
                formatted_question = f"🏗️ [{topic_name}] {poll_question}"
                if len(formatted_question) > 255:
                    formatted_question = f"🏗️ {poll_question}"
                if len(formatted_question) > 255:
                    formatted_question = poll_question[:255]
                
                explanation = question.get('explanation', 'No explanation provided.')
                source = question.get('source', '')
                if source:
                    explanation += f"\n\nSource: {source}"
                
                if len(explanation) > 200:
                    explanation = explanation[:197] + "..."
                
                await bot.send_poll(
                    chat_id=CHANNEL_ID,
                    question=formatted_question,
                    options=question['options'],
                    type='quiz',
                    correct_option_id=question['correct_option_id'],
                    explanation=explanation,
                    is_anonymous=True
                )
                logger.info(f"Sent AI quiz: {topic_name} - {difficulty}")
                return
        
        # Fallback to local questions
        logger.warning("AI Quiz failed or invalid format. Using fallback.")
        
        # Use local question bank with quiz poll format
        local_questions = [q for q in QUESTIONS if q.get('answer') in ['A', 'B', 'C', 'D']]
        
        if local_questions:
            item = random.choice(local_questions)
            topic_code = item.get('topic', 'General')
            topic_name = ai_service.get_topic_name(topic_code)
            
            # Convert A/B/C/D to option index
            answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            correct_id = answer_map.get(item['answer'], 0)
            
            # Clean options (remove A), B), etc. prefixes if present)
            options = []
            for opt in item['options']:
                clean_opt = opt
                if opt.startswith(('A)', 'B)', 'C)', 'D)', 'A.', 'B.', 'C.', 'D.')):
                    clean_opt = opt[2:].strip()
                elif opt.startswith(('A ', 'B ', 'C ', 'D ')):
                    clean_opt = opt[2:].strip()
                options.append(clean_opt)
            
            poll_question = f"🏗️ [{topic_name}] {item['question']}"
            if len(poll_question) > 255:
                poll_question = item['question'][:255]
            
            await bot.send_poll(
                chat_id=CHANNEL_ID,
                question=poll_question,
                options=options,
                type='quiz',
                correct_option_id=correct_id,
                is_anonymous=True
            )
            logger.info(f"Sent fallback quiz: {topic_name}")
        else:
            # Ultimate fallback - just send text question
            item = random.choice(QUESTIONS)
            text = f"""
{format_separator()}
🏗️ **GATE Civil Question**
{format_separator()}

❓ {item['question']}

"""
            for opt in item['options']:
                text += f"{opt}\n"
            text += f"\n_Reply with your answer!_\n{format_separator()}"
            
            await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
            logger.info("Sent text-based question (fallback)")
            
    except Exception as e:
        logger.error(f"Failed to send quiz: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("Starting daily content posting...")
    asyncio.run(send_daily_content())
    logger.info("Daily content posting completed.")
