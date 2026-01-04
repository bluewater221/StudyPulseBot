import os
import json
import aiohttp
import logging
import asyncio
import random
import re
from typing import Optional, Dict, Any
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY") # Primary
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # Backup
try:
    from groq import Groq
except ImportError:
    Groq = None

REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

if not API_KEY and not GROQ_API_KEY:
    logger.warning("⚠️ No valid API keys (GEMINI or GROQ) set - AI features will be disabled")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Topic definitions for GATE Civil Engineering
TOPICS = {
    "SM": "Soil Mechanics",
    "FM": "Fluid Mechanics", 
    "SA": "Structural Analysis",
    "RCC": "Reinforced Concrete Design",
    "STEEL": "Steel Structures",
    "GEO": "Geomatics / Surveying",
    "ENV": "Environmental Engineering",
    "TRANS": "Transportation Engineering",
    "HYDRO": "Hydrology & Irrigation",
    "CONST": "Construction Management & Engineering Economics"
}

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

def get_question_prompt(topic: Optional[str] = None, difficulty: str = "medium") -> str:
    """Generate a dynamic question prompt based on topic and difficulty."""
    topic_text = ""
    if topic and topic in TOPICS:
        topic_text = f"Focus specifically on: {TOPICS[topic]}."
    else:
        topic_text = "Topics can include: Soil Mechanics, Fluid Mechanics, Structural Analysis, Environmental Engineering, Transportation, Geomatics, RCC, Steel Structures."
    
    difficulty_text = {
        "easy": "Create a basic conceptual question suitable for beginners.",
        "medium": "Create a standard GATE-level question requiring good understanding.",
        "hard": "Create a challenging question similar to difficult GATE previous year questions."
    }.get(difficulty, "Create a standard GATE-level question.")
    
    return f"""
Generate a challenging multiple-choice question (MCQ) for the Civil Engineering GATE exam.
{topic_text}
{difficulty_text}
Ensure the question requires conceptual understanding or standard calculation.
The output format must be a JSON object with this exact structure:
{{
  "question": "The question text here (max 300 chars)",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_option_id": 0,
  "explanation": "A clear explanation of the solution (max 200 chars).",
  "topic": "Topic code like SM, FM, SA, RCC etc",
  "difficulty": "{difficulty}",
  "source": "Citation (e.g., IS 456, GATE 2021, NPTEL)",
  "visual_hint": "Description of a diagram or graph that would help visualize this (max 100 chars)"
}}
Note: correct_option_id must be an integer: 0 for 1st option, 1 for 2nd, etc.
"""

FACT_PROMPT = """
Generate a high-value "Key Note" or "One-Liner" for Civil Engineering GATE preparation.
It should be a key concept, important IS Code provision (IS 456, IS 800 etc), or a vital property of material.
Output JSON:
{
  "fact": "The text of the fact.",
  "topic": "Topic code like SM, FM, SA, RCC etc",
  "source": "Citation of IS code or textbook",
  "visual_hint": "Brief description of a relevant visual/diagram"
}
"""

FORMULA_PROMPT = """
Generate a key Civil Engineering formula often asked in GATE.
Output JSON:
{
  "title": "Name of the formula",
  "formula": "The mathematical expression (use plain text representation)",
  "explanation": "Brief explanation of specific terms and context.",
  "topic": "Topic code like SM, FM, SA, RCC etc",
  "source": "Relevant textbook or IS code section",
  "visual_hint": "Description of the variable geometry or graph for this formula"
}
"""

LANGUAGE_PROMPT = """
Generate a micro-learning language tip for one of these languages: Chinese (Mandarin), Marathi, Telugu, or Japanese.
The lesson should be very small and beginner-friendly (e.g., one word, one phrase, or one greeting per day).
Output JSON:
{
  "language": "Language Name (e.g., Japanese)",
  "word": "The word or phrase in original script",
  "phonetic": "How to pronounce it (e.g., Romaji, Pinyin)",
  "meaning": "English translation",
  "usage": "A simple example sentence",
  "tip": "A quick cultural or grammar tip related to this word",
  "topic": "LANG"
}
"""

def repair_json(text: str) -> str:
    """Attempt to repair common AI JSON formatting issues."""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    text = text.strip()
    
    # Handle truncated JSON (very basic)
    if text.startswith('{') and not text.endswith('}'):
        text += '}'
        
    return text

async def _make_api_request(prompt_text: str) -> Optional[Dict[str, Any]]:
    """Make API request with Gemini (Primary) and retry logic, falling back to Groq."""
    
    # 1. Try Gemini
    if API_KEY:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }
        
        async with aiohttp.ClientSession() as session:
            for attempt in range(MAX_RETRIES):
                try:
                    async with session.post(URL, headers=headers, json=data, timeout=REQUEST_TIMEOUT) as response:
                        if response.status == 200:
                            result = await response.json()
                            raw_text = result['candidates'][0]['content']['parts'][0]['text']
                            return json.loads(repair_json(raw_text))
                        elif response.status == 429:
                            logger.warning("Gemini Quota Exhausted (429). Failing over immediately...")
                            break  # Fail over to backups
                        
                        logger.warning(f"Gemini Attempt {attempt+1} failed ({response.status})")
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(2)
                            
                except Exception as e:
                    logger.error(f"Gemini connection error: {e}")
    
    # 2. Fallback to Groq
    if GROQ_API_KEY and Groq:
        logger.info("Falling back to Groq API...")
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_text + "\nReturn ONLY valid JSON."}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return json.loads(repair_json(completion.choices[0].message.content))
        except Exception as e:
            logger.error(f"Groq fallback failed: {e}")

    # 3. Fallback to OpenRouter (New)
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if OPENROUTER_API_KEY:
        logger.info("Falling back to OpenRouter API...")
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                 "HTTP-Referer": "https://github.com/antigravity", # Optional
            }
            data = {
                "model": "deepseek/deepseek-chat", # Affordable and good
                "messages": [{"role": "user", "content": prompt_text + "\nReturn ONLY valid JSON."}],
                "response_format": {"type": "json_object"}
            }
            async with aiohttp.ClientSession() as session:
                 async with session.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=REQUEST_TIMEOUT) as response:
                        if response.status == 200:
                            result = await response.json()
                            content = result['choices'][0]['message']['content']
                            return json.loads(repair_json(content))
                        else:
                            logger.error(f"OpenRouter failed with {response.status}")
                            
                            
        except Exception as e:
            logger.error(f"OpenRouter fallback failed: {e}")

    # 4. Fallback to HuggingFace (New)
    HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    if HF_API_KEY:
        logger.info("Falling back to HuggingFace API...")
        try:
            # Using meta-llama/Meta-Llama-3-8B-Instruct
            API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {
                "inputs": prompt_text + "\nReturn ONLY valid JSON.",
                "parameters": {"max_new_tokens": 512, "return_full_text": False}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result[0]['generated_text']
                        # Try to extract JSON from text if it's mixed
                        start_idx = content.find('{')
                        end_idx = content.rfind('}') + 1
                        if start_idx != -1 and end_idx != -1:
                            content = content[start_idx:end_idx]
                        return json.loads(content)
                    else:
                         logger.error(f"HuggingFace failed with {response.status}")

        except Exception as e:
            logger.error(f"HuggingFace fallback failed: {e}")

    logger.error(f"All AI attempts failed.")
    return None


# --- Caching Mechanism ---

CACHE_FILE = "ai_content_cache.json"

def load_cache() -> Dict[str, list]:
    """Load the local cache file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
    return {}

def save_cache(cache: Dict[str, list]):
    """Save to the local cache file."""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")

def add_to_cache(content_type: str, content: Dict[str, Any]):
    """Add new content to cache, avoiding duplicates."""
    cache = load_cache()
    if content_type not in cache:
        cache[content_type] = []
    
    # Avoid duplicates based on key fields
    is_duplicate = False
    for item in cache[content_type]:
        if content_type == "question" and item.get("question") == content.get("question"):
            is_duplicate = True
            break
        elif content_type == "fact" and item.get("fact") == content.get("fact"):
            is_duplicate = True
            break
        elif content_type == "formula" and item.get("title") == content.get("title"):
             is_duplicate = True
             break
        elif content_type == "language" and item.get("word") == content.get("word"):
             is_duplicate = True
             break
    
    if not is_duplicate:
        cache[content_type].append(content)
        # Limit cache size per type (optional, keep last 100)
        if len(cache[content_type]) > 100:
            cache[content_type] = cache[content_type][-100:]
        save_cache(cache)
        logger.info(f"Cached new {content_type}")

def get_from_cache(content_type: str) -> Optional[Dict[str, Any]]:
    """Retrieve random item from cache."""
    cache = load_cache()
    items = cache.get(content_type, [])
    if items:
        # Try to pick one that hasn't been used recently? 
        # For now, just random is better than static fallback
        return random.choice(items)
    return None

async def get_ai_content(content_type: str, topic: Optional[str] = None, difficulty: str = "medium") -> Optional[Dict[str, Any]]:
    """
    Generates content using Google Gemini via REST API.
    Retries with Cache if API fails.
    """
    if not API_KEY and not GROQ_API_KEY:
        logger.error("No AI credentials found. checking cache...")
        return get_from_cache(content_type)

    prompt_text = ""
    if content_type == "question":
        prompt_text = get_question_prompt(topic, difficulty)
    elif content_type == "fact":
        prompt_text = FACT_PROMPT
    elif content_type == "formula":
        prompt_text = FORMULA_PROMPT
    elif content_type == "language":
        prompt_text = LANGUAGE_PROMPT
    else:
        logger.error(f"Unknown content type: {content_type}")
        return None
    
    # Try API
    result = await _make_api_request(prompt_text)
    
    if result:
        # Save to cache for future
        add_to_cache(content_type, result)
        return result
    
    # Fallback to Cache
    logger.warning(f"AI API failed for {content_type}. Attempting to use cached content.")
    cached_item = get_from_cache(content_type)
    
    if cached_item:
        logger.info(f"Served {content_type} from local cache.")
        return cached_item
        
    return None

def get_available_topics() -> Dict[str, str]:
    """Return available topics for selection."""
    return TOPICS.copy()

def get_topic_name(code: str) -> str:
    """Get full topic name from code."""
    return TOPICS.get(code.upper(), "General")

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    print("Testing question generation...")
    result = asyncio.run(get_ai_content("question", topic="SM", difficulty="medium"))
    print(json.dumps(result, indent=2) if result else "Failed to generate")
