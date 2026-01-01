import logging
import asyncio
import os
import random
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler
from content import QUESTIONS, FACTS, FORMULAS, EXERCISE_TIPS, HYGIENE_TIPS, GENERAL_HEALTH_TIPS, LANGUAGE_FALLBACKS
import ai_service
import sheets
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

# Simple in-memory user stats (for demo - use database in production)
user_stats: Dict[int, Dict[str, Any]] = {}

# Daily challenge tracking
daily_challenge: Dict[str, Any] = {
    "date": None,
    "question": None,
    "participants": {},  # user_id: {answered: bool, correct: bool, time_taken: float}
}

# Leaderboard data (weekly reset)
weekly_leaderboard: Dict[int, Dict[str, Any]] = {}  # user_id: {name, correct, total, score}

# --- Persistence ---

STATS_FILE = "user_stats.json"
LEADERBOARD_FILE = "leaderboard.json"

def save_data():
    """Save stats and leaderboard to disk."""
    try:
        with open(STATS_FILE, "w") as f:
            json.dump(user_stats, f, default=str)
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(weekly_leaderboard, f, default=str)
    except Exception as e:
        logger.error(f"Failed to save data: {e}")

def load_data():
    """Load stats and leaderboard from disk."""
    global user_stats, weekly_leaderboard
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r") as f:
                # Convert string keys back to int IDs
                data = json.load(f)
                user_stats = {int(k): v for k, v in data.items()}
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
                weekly_leaderboard = {int(k): v for k, v in data.items()}
    except Exception as e:
        logger.error(f"Failed to load data: {e}")

# Load initial data
load_data()

# --- Formatting Helpers ---

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

def get_difficulty_stars(difficulty: str) -> str:
    """Get star representation for difficulty."""
    stars = {"easy": "⭐", "medium": "⭐⭐", "hard": "⭐⭐⭐"}
    return stars.get(difficulty, "⭐⭐")

# --- User Stats ---

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get or create user stats."""
    if user_id not in user_stats:
        user_stats[user_id] = {
            "correct": 0,
            "incorrect": 0,
            "total": 0,
            "streak": 0,
            "last_answer_date": None,
            "preferred_topic": None,
            "weekly_correct": 0,
            "weekly_total": 0,
            "fastest_answer": None,  # seconds
            "daily_completed": None  # date of last daily challenge
        }
    return user_stats[user_id]

def update_leaderboard(user_id: int, username: str, is_correct: bool):
    """Update weekly leaderboard."""
    if user_id not in weekly_leaderboard:
        weekly_leaderboard[user_id] = {
            "name": username,
            "correct": 0,
            "total": 0,
            "score": 0
        }
    
    weekly_leaderboard[user_id]["total"] += 1
    if is_correct:
        weekly_leaderboard[user_id]["correct"] += 1
        weekly_leaderboard[user_id]["score"] += 10  # 10 points per correct answer
    weekly_leaderboard[user_id]["name"] = username  # Keep name updated
    save_data()

def get_leaderboard_text() -> str:
    """Generate leaderboard text."""
    if not weekly_leaderboard:
        return "No participants yet this week! Be the first to answer questions."
    
    # Sort by score, then by accuracy
    sorted_users = sorted(
        weekly_leaderboard.items(),
        key=lambda x: (x[1]["score"], x[1]["correct"] / max(x[1]["total"], 1)),
        reverse=True
    )[:10]  # Top 10
    
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    lines = []
    
    for i, (user_id, data) in enumerate(sorted_users):
        accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        lines.append(
            f"{medals[i]} **{data['name']}**\n"
            f"   📊 Score: {data['score']} | ✅ {data['correct']}/{data['total']} ({accuracy:.0f}%)"
        )
    
    return "\n\n".join(lines)

def update_user_stats(user_id: int, is_correct: bool):
    """Update user statistics after answering."""
    stats = get_user_stats(user_id)
    today = datetime.now().date()
    last_date = stats["last_answer_date"]
    
    # Handle string from JSON
    if isinstance(last_date, str):
        last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
    
    if is_correct:
        stats["correct"] += 1
        if last_date is None:
            stats["streak"] = 1
        elif last_date == today - timedelta(days=1):
            stats["streak"] += 1
        elif last_date < today - timedelta(days=1):
            stats["streak"] = 1
        # If it's today, keep current streak
    else:
        stats["incorrect"] += 1
        # Optionally reset streak on wrong answer? Let's keep it daily for now.
    
    stats["last_answer_date"] = today.strftime("%Y-%m-%d")
    save_data()

# --- Message Generators ---

async def generate_question(topic: Optional[str] = None, difficulty: str = "medium") -> tuple[str, Optional[dict]]:
    """Generate a formatted question message."""
    # Try AI first
    ai_content = await ai_service.get_ai_content("question", topic=topic, difficulty=difficulty)
    
    if ai_content:
        item = ai_content
        topic_code = item.get('topic', 'General')
        topic_name = ai_service.get_topic_name(topic_code)
        diff = item.get('difficulty', difficulty)
        
        source = item.get('source', 'GATE Preparation Resource')
        visual = item.get('visual_hint', '')
        visual_text = f"\n🖼️ **Visual**: _{visual}_\n" if visual else ""
        
        text = f"""
{format_separator()}
🏗️ **GATE Civil Engineering**
{format_separator()}

{get_topic_emoji(topic_code)} **Topic**: {topic_name}
{get_difficulty_stars(diff)} **Difficulty**: {diff.capitalize()}

❓ {item['question']}
{visual_text}
"""
        for i, opt in enumerate(item['options']):
            letter = chr(65 + i)  # A, B, C, D
            text += f"**{letter})** {opt}\n"
        
        text += f"\n📚 **Source**: {source}"
        text += f"\n\n⏱️ _Think carefully before answering!_\n{format_separator()}"
        return text, ai_content
    
    # Fallback to static content
    item = random.choice(QUESTIONS)
    topic_code = item.get('topic', 'General')
    topic_name = ai_service.get_topic_name(topic_code)
    diff = item.get('difficulty', 'medium')
    
    text = f"""
{format_separator()}
🏗️ **GATE Civil Question**
{format_separator()}

{get_topic_emoji(topic_code)} **Topic**: {topic_name}
{get_difficulty_stars(diff)} **Difficulty**: {diff.capitalize()}

❓ {item['question']}

"""
    for opt in item['options']:
        text += f"**{opt[:2]}** {opt[3:] if opt[2:3] == ')' else opt[2:].strip()}\n"
    
    text += f"\n⏱️ _Think carefully before answering!_\n{format_separator()}"
    
    # Map 'A', 'B', 'C', 'D' to 0, 1, 2, 3
    answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    return text, {
        "question": item['question'],
        "options": item['options'],
        "correct_option_id": answer_map.get(item['answer'], 0),
        "explanation": "Standard GATE concept. Consult textbooks for detailed derivation.",
        "topic": topic_code,
        "difficulty": diff
    }

async def generate_fact() -> str:
    """Generate a formatted fact message."""
    ai_content = await ai_service.get_ai_content("fact")
    
    if ai_content:
        topic_code = ai_content.get('topic', 'General')
        topic_name = ai_service.get_topic_name(topic_code)
        source = ai_content.get('source', 'Civil Engineering Standards')
        visual = ai_content.get('visual_hint', '')
        visual_text = f"\n🖼️ **Visual**: _{visual}_\n" if visual else ""
        
        return f"""
{format_separator()}
📝 **GATE Civil Key Note**
{format_separator()}

{get_topic_emoji(topic_code)} **Topic**: {topic_name}

💡 {ai_content['fact']}
{visual_text}
📚 **Source**: {source}

{format_separator()}
_Save this for revision!_ 📌
"""
    
    fact = random.choice(FACTS)
    return f"""
{format_separator()}
📝 **GATE Civil Key Note**
{format_separator()}

💡 {fact}

{format_separator()}
"""

def get_study_keyboard(next_type: str) -> InlineKeyboardMarkup:
    """Get keyboard for sequential study."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Got it! Next ➡️", callback_data=f"next_{next_type}")]
    ])

async def generate_formula() -> str:
    """Generate a formatted formula message."""
    ai_content = await ai_service.get_ai_content("formula")
    
    if ai_content:
        topic_code = ai_content.get('topic', 'General')
        topic_name = ai_service.get_topic_name(topic_code)
        source = ai_content.get('source', 'Engineers Reference')
        visual = ai_content.get('visual_hint', '')
        visual_text = f"\n🖼️ **Visual**: _{visual}_\n" if visual else ""
        
        return f"""
{format_separator()}
📐 **GATE Civil Formula**
{format_separator()}

{get_topic_emoji(topic_code)} **Topic**: {topic_name}

📌 **{ai_content['title']}**

`{ai_content['formula']}`

📖 {ai_content['explanation']}
{visual_text}
📚 **Source**: {source}

{format_separator()}
_Memorize this formula!_ 🧠
"""
    
    item = random.choice(FORMULAS)
    return f"""
{format_separator()}
📐 **GATE Civil Formula**
{format_separator()}

📌 **{item['title']}**

`{item['formula']}`

📖 {item['explanation']}

{format_separator()}
"""

# --- Inline Keyboards ---

def get_topic_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard for topic selection."""
    topics = ai_service.get_available_topics()
    keyboard = []
    row = []
    for i, (code, name) in enumerate(topics.items()):
        emoji = get_topic_emoji(code)
        row.append(InlineKeyboardButton(f"{emoji} {code}", callback_data=f"topic_{code}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🎲 Random Topic", callback_data="topic_random")])
    return InlineKeyboardMarkup(keyboard)

def get_difficulty_keyboard(topic: str = "random") -> InlineKeyboardMarkup:
    """Create inline keyboard for difficulty selection."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⭐ Easy", callback_data=f"diff_{topic}_easy"),
            InlineKeyboardButton("⭐⭐ Medium", callback_data=f"diff_{topic}_medium"),
            InlineKeyboardButton("⭐⭐⭐ Hard", callback_data=f"diff_{topic}_hard")
        ]
    ])

def get_answer_keyboard(question_id: str) -> InlineKeyboardMarkup:
    """Create inline keyboard for answering questions."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("A", callback_data=f"ans_{question_id}_0"),
            InlineKeyboardButton("B", callback_data=f"ans_{question_id}_1"),
            InlineKeyboardButton("C", callback_data=f"ans_{question_id}_2"),
            InlineKeyboardButton("D", callback_data=f"ans_{question_id}_3")
        ]
    ])

# --- Job ---

async def send_hourly_message(context: ContextTypes.DEFAULT_TYPE):
    """Sends a message every 1 hour."""
    job = context.job
    
    # Rotate content type for variety
    current_hour = datetime.now().hour
    if current_hour % 3 == 0:
        message_text = await generate_fact()
        parse_mode = "Markdown"
    elif current_hour % 3 == 1:
        message_text, _ = await generate_question()
        parse_mode = "Markdown"
    else:
        message_text = await generate_formula()
        parse_mode = "Markdown"

    chat_id = job.chat_id if job.chat_id else CHANNEL_ID

    if not chat_id:
        logger.error("No Chat ID provided for the job.")
        return

    try:
        await context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode=parse_mode)
        logger.info(f"Sent scheduled message to {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send scheduled message: {e}")

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message."""
    user = update.effective_user
    welcome_text = f"""
{format_separator()}
🏗️ **Welcome to GATE Civil Bot!**
{format_separator()}

Hello {user.first_name}! 👋

I'm your AI-powered Civil Engineering GATE preparation assistant.

**📚 Available Commands:**

/question - Get a practice MCQ
/topic - Choose a specific subject
/fact - Get a key concept note
/formula - Get an important formula
/stats - View your progress
/help - Show all commands

**🎯 Features:**
• AI-generated fresh questions
• 10 GATE subjects covered
• 3 difficulty levels
• Track your performance

{format_separator()}
_Let's crack GATE together!_ 💪
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed help."""
    help_text = f"""
{format_separator()}
📖 **GATE Civil Bot - Help**
{format_separator()}

**📝 Practice Commands:**
• `/question` - Random MCQ (medium difficulty)
• `/question easy` - Easy level question
• `/question hard` - Challenging question
• `/topic` - Choose subject & difficulty

**📚 Study Material:**
• `/fact` - Get a key concept/note
• `/formula` - Get an important formula
• `/exercise` - Movement tips for study breaks
• `/hygiene` - Personal hygiene reminders
• `/wellness` - General health advice
• `/language` - Learn a word in Chinese, Marathi, Telugu, or Japanese!

**📝 My Notes (Google Sheets):**
• `/addnote SM your note here` - Save a note for a topic
• `/mynotes` - View all your saved notes
• `/notefor SM` - Get notes for a specific topic

**📊 Progress:**
• `/stats` - Your performance stats

**🏆 Subjects Covered:**
SM - Soil Mechanics
FM - Fluid Mechanics
SA - Structural Analysis
RCC - Reinforced Concrete
STEEL - Steel Structures
GEO - Geomatics/Surveying
ENV - Environmental Engg.
TRANS - Transportation
HYDRO - Hydrology
CONST - Construction Mgmt.

{format_separator()}
_Powered by AI_ 🤖
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def exercise_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends an exercise tip."""
    tip = random.choice(EXERCISE_TIPS)
    text = f"""
{format_separator()}
🏃 **Exercise Tip**
{format_separator()}

{tip['name']}

{tip['desc']}

{format_separator()}
_Take a break and move!_ 💪
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def hygiene_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a hygiene tip."""
    tip = random.choice(HYGIENE_TIPS)
    text = f"""
{format_separator()}
🧼 **Hygiene Tip**
{format_separator()}

{tip['name']}

{tip['desc']}

{format_separator()}
_Stay fresh, stay focused!_ ✨
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def wellness_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a general health tip."""
    tip = random.choice(GENERAL_HEALTH_TIPS)
    text = f"""
{format_separator()}
🍎 **Wellness Tip**
{format_separator()}

{tip['name']}

{tip['desc']}

{format_separator()}
_Your health matters!_ 🌟
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a micro-language lesson."""
    ai_content = await ai_service.get_ai_content("language")
    
    if ai_content:
        item = ai_content
    else:
        item = random.choice(LANGUAGE_FALLBACKS)
    
    text = f"""
{format_separator()}
🌐 **Language Micro-Learning** ({item['language']})
{format_separator()}

🔤 **Word**: {item['word']}
🗣️ **Phonetic**: {item['phonetic']}
📖 **Meaning**: {item['meaning']}

📝 **Usage**: {item['usage']}
💡 **Tip**: {item['tip']}

{format_separator()}
_Consistency is key!_ 🗝️
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def topic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Let user select a topic."""
    await update.message.reply_text(
        "**🎯 Select a Topic:**\n\n_Choose your focus area:_",
        reply_markup=get_topic_keyboard(),
        parse_mode="Markdown"
    )

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a question on demand."""
    # Check for difficulty argument
    difficulty = "medium"
    if context.args and context.args[0].lower() in ["easy", "medium", "hard"]:
        difficulty = context.args[0].lower()
    
    await update.message.reply_text("🔄 _Generating question..._", parse_mode="Markdown")
    
    msg, question_data = await generate_question(difficulty=difficulty)
    
    if question_data and 'correct_option_id' in question_data:
        # Store question data for answer verification
        question_id = str(hash(question_data['question']))[:8]
        context.user_data[f"q_{question_id}"] = question_data
        
        await update.message.reply_text(
            msg,
            reply_markup=get_answer_keyboard(question_id),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(msg, parse_mode="Markdown")

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a fact on demand."""
    await update.message.reply_text("🔄 _Generating key note..._", parse_mode="Markdown")
    msg = await generate_fact()
    await update.message.reply_text(msg, reply_markup=get_study_keyboard("fact"), parse_mode="Markdown")

async def formula_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a formula on demand."""
    await update.message.reply_text("🔄 _Generating formula..._", parse_mode="Markdown")
    msg = await generate_formula()
    await update.message.reply_text(msg, reply_markup=get_study_keyboard("formula"), parse_mode="Markdown")

async def study_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a random study session (facts/formulas)."""
    next_type = random.choice(["fact", "formula"])
    await update.message.reply_text("🚀 _Starting your study session..._", parse_mode="Markdown")
    if next_type == "fact":
        msg = await generate_fact()
    else:
        msg = await generate_formula()
    await update.message.reply_text(msg, reply_markup=get_study_keyboard(next_type), parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's statistics."""
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    
    accuracy = 0
    if stats["total"] > 0:
        accuracy = (stats["correct"] / stats["total"]) * 100
    
    # Determine ranking emoji
    if accuracy >= 90:
        rank_emoji = "🏆"
        rank_text = "Excellent!"
    elif accuracy >= 75:
        rank_emoji = "🥈"
        rank_text = "Great work!"
    elif accuracy >= 60:
        rank_emoji = "🥉"
        rank_text = "Good progress!"
    else:
        rank_emoji = "📈"
        rank_text = "Keep practicing!"
    
    stats_text = f"""
{format_separator()}
📊 **Your GATE Prep Stats**
{format_separator()}

✅ Correct: **{stats['correct']}**
❌ Incorrect: **{stats['incorrect']}**
📝 Total Attempted: **{stats['total']}**

📈 Accuracy: **{accuracy:.1f}%**
🔥 Current Streak: **{stats['streak']} days**

{rank_emoji} **{rank_text}**

{format_separator()}
_Keep solving daily for best results!_ 💪
"""
    await update.message.reply_text(stats_text, parse_mode="Markdown")

# --- Callback Query Handler ---

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button presses."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("topic_"):
        # Topic selected
        topic = data.replace("topic_", "")
        if topic == "random":
            topic_name = "Random Topic"
        else:
            topic_name = ai_service.get_topic_name(topic)
        
        await query.edit_message_text(
            f"**Selected**: {get_topic_emoji(topic)} {topic_name}\n\n**Choose difficulty:**",
            reply_markup=get_difficulty_keyboard(topic),
            parse_mode="Markdown"
        )
    
    elif data.startswith("diff_"):
        # Difficulty selected
        parts = data.split("_")
        topic = parts[1] if parts[1] != "random" else None
        difficulty = parts[2]
        
        await query.edit_message_text("🔄 _Generating question..._", parse_mode="Markdown")
        
        msg, question_data = await generate_question(topic=topic, difficulty=difficulty)
        
        if question_data and 'correct_option_id' in question_data:
            question_id = str(hash(question_data['question']))[:8]
            context.user_data[f"q_{question_id}"] = question_data
            
            await query.message.reply_text(
                msg,
                reply_markup=get_answer_keyboard(question_id),
                parse_mode="Markdown"
            )
        else:
            await query.message.reply_text(msg, parse_mode="Markdown")
    
    elif data.startswith("ans_"):
        # Answer selected
        parts = data.split("_")
        question_id = parts[1]
        selected_option = int(parts[2])
        
        question_data = context.user_data.get(f"q_{question_id}")
        
        if question_data:
            correct_id = question_data.get('correct_option_id', 0)
            explanation = question_data.get('explanation', 'No explanation available.')
            
            user_id = update.effective_user.id
            is_correct = selected_option == correct_id
            update_user_stats(user_id, is_correct)
            
            source = question_data.get('source', '')
            source_text = f"\n\n📚 **Source**: {source}" if source else ""
            
            if is_correct:
                result_text = f"✅ **Correct!** Well done! 🎉\n\n📖 **Explanation:**\n{explanation}{source_text}"
            else:
                correct_letter = chr(65 + correct_id)
                result_text = f"❌ **Incorrect**\n\nThe correct answer was **{correct_letter}**\n\n📖 **Explanation:**\n{explanation}{source_text}"
            
            await query.edit_message_reply_markup(reply_markup=None)
            
            # Check if part of a quiz session
            session = context.user_data.get("quiz_session")
            if session:
                session["current"] += 1
                if is_correct: session["correct"] += 1
                
                if session["current"] < session["total"]:
                    await query.message.reply_text(result_text, parse_mode="Markdown")
                    # Send next question
                    await asyncio.sleep(1)
                    msg, new_q = await generate_question()
                    question_id = f"quiz_{user_id}_{session['current']}"
                    context.user_data[f"q_{question_id}"] = new_q
                    await query.message.reply_text(
                        f"**Question {session['current']+1}/{session['total']}**\n{msg}",
                        reply_markup=get_answer_keyboard(question_id),
                        parse_mode="Markdown"
                    )
                else:
                    duration = (datetime.now() - session["start_time"]).total_seconds()
                    final_text = f"{result_text}\n\n" + format_separator() + f"\n🏆 **Quiz Completed!**\n" + format_separator() + f"\n✅ Score: {session['correct']}/{session['total']}\n⏱️ Time: {duration:.1f}s\n" + format_separator()
                    await query.message.reply_text(final_text, parse_mode="Markdown")
                    context.user_data.pop("quiz_session")
            else:
                await query.message.reply_text(result_text, reply_markup=get_study_keyboard("question"), parse_mode="Markdown")
            
            # Update leaderboard
            update_leaderboard(user_id, update.effective_user.first_name, is_correct)
            
            # Clean up stored question
            context.user_data.pop(f"q_{question_id}", None)
        else:
            await query.message.reply_text("⚠️ Question expired. Please try a new question with /question")

    elif data.startswith("next_"):
        # Sequential learning flow
        next_type = data.replace("next_", "")
        
        # Randomize next type occasionally for variety
        if random.random() < 0.2:
            next_type = random.choice(["fact", "formula", "question"])
            
        await query.message.edit_reply_markup(reply_markup=None)
        
        if next_type == "fact":
            msg = await generate_fact()
            await query.message.reply_text(msg, reply_markup=get_study_keyboard("fact"), parse_mode="Markdown")
        elif next_type == "formula":
            msg = await generate_formula()
            await query.message.reply_text(msg, reply_markup=get_study_keyboard("formula"), parse_mode="Markdown")
        else:
            msg, q_data = await generate_question()
            question_id = str(hash(msg))[:8]
            context.user_data[f"q_{question_id}"] = q_data
            await query.message.reply_text(msg, reply_markup=get_answer_keyboard(question_id), parse_mode="Markdown")

async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the daily challenge question."""
    global daily_challenge
    today = datetime.now().date()
    user_id = update.effective_user.id
    
    # Check if user already completed today's challenge
    stats = get_user_stats(user_id)
    if stats.get("daily_completed") == today:
        await update.message.reply_text(
            f"{format_separator()}\n"
            f"🌟 **Daily Challenge**\n"
            f"{format_separator()}\n\n"
            f"You've already completed today's challenge! ✅\n\n"
            f"Come back tomorrow for a new challenge.\n"
            f"{format_separator()}",
            parse_mode="Markdown"
        )
        return
    
    # Generate new daily challenge if needed
    if daily_challenge["date"] != today:
        await update.message.reply_text("🔄 _Generating today's challenge..._", parse_mode="Markdown")
        
        # Generate a hard question for daily challenge
        msg, question_data = await generate_question(difficulty="hard")
        
        daily_challenge = {
            "date": today,
            "question": question_data,
            "message": msg,
            "participants": {},
            "start_time": datetime.now()
        }
    
    # Send the daily challenge
    question_data = daily_challenge["question"]
    if question_data and 'correct_option_id' in question_data:
        question_id = f"daily_{today.isoformat()}"
        context.user_data[f"q_{question_id}"] = question_data
        context.user_data[f"q_{question_id}_start"] = datetime.now()
        
        challenge_msg = f"""
{format_separator()}
🌟 **DAILY CHALLENGE** 🌟
{format_separator()}

⏱️ _Answer quickly for bonus points!_

{daily_challenge['message']}
"""
        await update.message.reply_text(
            challenge_msg,
            reply_markup=get_answer_keyboard(question_id),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ Failed to generate daily challenge. Please try /question instead.",
            parse_mode="Markdown"
        )

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the weekly leaderboard."""
    leaderboard_text = get_leaderboard_text()
    
    msg = f"""
{format_separator()}
🏆 **WEEKLY LEADERBOARD** 🏆
{format_separator()}

{leaderboard_text}

{format_separator()}
_Rankings reset every Monday!_ 📅
"""
    await update.message.reply_text(msg, parse_mode="Markdown")

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a quick 5-question quiz session."""
    user_id = update.effective_user.id
    
    # Initialize quiz session
    context.user_data["quiz_session"] = {
        "current": 0,
        "total": 5,
        "correct": 0,
        "start_time": datetime.now()
    }
    
    await update.message.reply_text(
        f"{format_separator()}\n"
        f"🎯 **Quick Quiz Mode** 🎯\n"
        f"{format_separator()}\n\n"
        f"Answer 5 questions as fast as you can!\n\n"
        f"**Question 1 of 5** coming up...\n"
        f"{format_separator()}",
        parse_mode="Markdown"
    )
    
    # Send first question
    await asyncio.sleep(1)
    msg, question_data = await generate_question(difficulty="medium")
    
    if question_data and 'correct_option_id' in question_data:
        question_id = f"quiz_{user_id}_0"
        context.user_data[f"q_{question_id}"] = question_data
        
        await update.message.reply_text(
            f"**Question 1/5**\n{msg}",
            reply_markup=get_answer_keyboard(question_id),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(msg, parse_mode="Markdown")

# --- Notes Commands ---

async def addnote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a personal note linked to a topic."""
    user = update.effective_user
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            f"""
{format_separator()}
📝 **Add Note - Usage**
{format_separator()}

`/addnote <TOPIC> <your note>`

**Example:**
`/addnote SM void ratio = e/(1+e)`

**Valid Topics:**
SM, FM, SA, RCC, STEEL, GEO, ENV, TRANS, HYDRO, CONST

{format_separator()}
""",
            parse_mode="Markdown"
        )
        return
    
    topic = context.args[0].upper()
    note = " ".join(context.args[1:])
    
    if not sheets.is_valid_topic(topic):
        await update.message.reply_text(
            f"❌ Invalid topic: `{topic}`\n\nValid topics: SM, FM, SA, RCC, STEEL, GEO, ENV, TRANS, HYDRO, CONST",
            parse_mode="Markdown"
        )
        return
    
    success = sheets.add_note(user.id, user.first_name, topic, note)
    
    if success:
        topic_name = sheets.get_topic_full_name(topic)
        await update.message.reply_text(
            f"""
{format_separator()}
✅ **Note Saved!**
{format_separator()}

📚 **Topic**: {topic_name} ({topic})
📝 **Note**: {note}

{format_separator()}
_Use /mynotes to see all your notes!_
""",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ Failed to save note. Please make sure Google Sheets is configured.",
            parse_mode="Markdown"
        )

async def mynotes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all user's notes."""
    user = update.effective_user
    notes = sheets.get_notes(user.id)
    
    if not notes:
        await update.message.reply_text(
            f"""
{format_separator()}
📝 **My Notes**
{format_separator()}

You haven't saved any notes yet!

Use `/addnote SM your note` to get started.

{format_separator()}
""",
            parse_mode="Markdown"
        )
        return
    
    # Group notes by topic
    notes_by_topic = {}
    for note in notes:
        topic = note['topic']
        if topic not in notes_by_topic:
            notes_by_topic[topic] = []
        notes_by_topic[topic].append(note['note'])
    
    text = f"""
{format_separator()}
📝 **My Notes** ({len(notes)} total)
{format_separator()}

"""
    for topic, topic_notes in notes_by_topic.items():
        topic_name = sheets.get_topic_full_name(topic)
        text += f"**{get_topic_emoji(topic)} {topic_name}** ({len(topic_notes)})\n"
        for i, n in enumerate(topic_notes[:3], 1):  # Show max 3 per topic
            text += f"  • {n[:50]}{'...' if len(n) > 50 else ''}\n"
        if len(topic_notes) > 3:
            text += f"  _...and {len(topic_notes) - 3} more_\n"
        text += "\n"
    
    text += f"""{format_separator()}
_Use /notefor <topic> for details_
"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def notefor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show notes for a specific topic."""
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text(
            "**Usage:** `/notefor SM`\n\nValid topics: SM, FM, SA, RCC, STEEL, GEO, ENV, TRANS, HYDRO, CONST",
            parse_mode="Markdown"
        )
        return
    
    topic = context.args[0].upper()
    
    if not sheets.is_valid_topic(topic):
        await update.message.reply_text(
            f"❌ Invalid topic: `{topic}`",
            parse_mode="Markdown"
        )
        return
    
    notes = sheets.get_notes(user.id, topic=topic)
    topic_name = sheets.get_topic_full_name(topic)
    
    if not notes:
        await update.message.reply_text(
            f"""
{format_separator()}
📝 **Notes for {topic_name}**
{format_separator()}

No notes found for this topic.

Add one: `/addnote {topic} your note here`

{format_separator()}
""",
            parse_mode="Markdown"
        )
        return
    
    text = f"""
{format_separator()}
{get_topic_emoji(topic)} **Notes for {topic_name}**
{format_separator()}

"""
    for i, note in enumerate(notes, 1):
        text += f"**{i}.** {note['note']}\n\n"
    
    text += f"{format_separator()}"
    await update.message.reply_text(text, parse_mode="Markdown")

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
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("topic", topic_command))
    application.add_handler(CommandHandler("question", question_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("formula", formula_command))
    application.add_handler(CommandHandler("exercise", exercise_command))
    application.add_handler(CommandHandler("hygiene", hygiene_command))
    application.add_handler(CommandHandler("wellness", wellness_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("daily", daily_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(CommandHandler("study", study_command))
    application.add_handler(CommandHandler("addnote", addnote_command))
    application.add_handler(CommandHandler("mynotes", mynotes_command))
    application.add_handler(CommandHandler("notefor", notefor_command))
    
    # Add Callback Query Handler for inline keyboards
    application.add_handler(CallbackQueryHandler(button_callback))

    # Schedule the job
    if CHANNEL_ID:
        job_queue.run_repeating(send_hourly_message, interval=3600, first=10, chat_id=CHANNEL_ID, name="hourly_gate_civil")
        print(f"Bot started. Scheduled to send messages to {CHANNEL_ID} every hour.")
    else:
        print("Warning: TELEGRAM_CHANNEL_ID not set. Hourly job disabled. You can still use commands like /question.")

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
