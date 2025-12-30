import logging
import os
import random
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from content import QUESTIONS, FACTS, FORMULAS
import ai_service
from dotenv import load_dotenv

# Load env variables (Token, Channel ID)
load_dotenv(override=True)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Configuration ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID") 

# --- Message Generators ---

def generate_question():
    # Try AI first
    ai_content = ai_service.get_ai_content("question")
    if ai_content:
        item = ai_content
        text = f"🏗️ GATE Civil Question (AI Generated)\n\n{item['question']}\n\n"
        for opt in item['options']:
            text += f"{opt}\n"
        text += f"\nReply with A, B, C, or D. Answer will be revealed next hour.\n\n(Debugging Answer: {item.get('answer')})"
        return text
        
    item = random.choice(QUESTIONS)
    text = f"🏗️ GATE Civil Question\n\n{item['question']}\n\n"
    for opt in item['options']:
        text += f"{opt}\n"
    text += "\nReply with A, B, C, or D. Answer will be revealed next hour."
    return text

def generate_fact():
    # Try AI first
    ai_content = ai_service.get_ai_content("fact")
    if ai_content:
        text = f"📝 GATE Civil Key Note (AI Generated)\n\n{ai_content['fact']}"
        return text

    fact = random.choice(FACTS)
    text = f"📝 GATE Civil Key Note\n\n{fact}"
    return text

def generate_formula():
    # Try AI first
    ai_content = ai_service.get_ai_content("formula")
    if ai_content:
        item = ai_content
        text = f"📐 GATE Civil Formula (AI Generated)\n\n{item['title']}\n{item['formula']}\n{item['explanation']}"
        return text

    item = random.choice(FORMULAS)
    text = f"📐 GATE Civil Formula\n\n{item['title']}\n{item['formula']}\n{item['explanation']}"
    return text

# --- Job ---

async def send_hourly_message(context: ContextTypes.DEFAULT_TYPE):
    """Sends a message every 1 hour."""
    job = context.job
    
    # 1. Choose Type
    msg_type = random.choice(["question", "fact", "formula"])
    
    if msg_type == "question":
        message_text = generate_question()
    elif msg_type == "fact":
        message_text = generate_fact()
    else:
        message_text = generate_formula()

    # 2. Send Message
    # Note: job.chat_id is set when we run the job. 
    # If we want to send to a specific channel fixed in env, use that.
    chat_id = job.chat_id if job.chat_id else CHANNEL_ID

    if not chat_id:
        logger.error("No Chat ID provided for the job.")
        return

    await context.bot.send_message(chat_id=chat_id, text=message_text)
    logger.info(f"Sent message of type {msg_type} to {chat_id}")

# --- Main ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message."""
    welcome_text = (
        "🏗️ Welcome to the Civil Engineering GATE Bot!\n\n"
        "I can help you prepare with:\n"
        "/question - Get a random GATE MCQ\n"
        "/fact - Get a key Civil Engineering note\n"
        "/formula - Get an important formula\n\n"
        "I also post hourly updates if configured for a channel."
    )
    await update.message.reply_text(welcome_text)

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a question on demand."""
    msg = generate_question()
    await update.message.reply_text(msg)

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a fact on demand."""
    msg = generate_fact()
    await update.message.reply_text(msg)

async def formula_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a formula on demand."""
    msg = generate_formula()
    await update.message.reply_text(msg)

# --- Main ---

def main() -> None:
    """Run bot."""
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Get the JobQueue
    job_queue = application.job_queue

    # Add Command Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("question", question_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("formula", formula_command))

    # Schedule the job
    # We need a target verification chat_id. For now, assuming the user will run this 
    # and maybe pass a chat_id via some means or hardcode it for testing.
    # However, standard practice for channel bots is just to use the channel ID.
    
    if CHANNEL_ID:
        job_queue.run_repeating(send_hourly_message, interval=3600, first=1, chat_id=CHANNEL_ID, name="hourly_gate_civil")
        print(f"Bot started. Scheduled to send messages to {CHANNEL_ID} every hour.")
    else:
        print("Warning: TELEGRAM_CHANNEL_ID not set. Hourly job disabled. You can still use commands like /question.")

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
