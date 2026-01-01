import os
import json
import aiohttp
import logging
import asyncio
from typing import Optional, Dict, Any
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

if not API_KEY:
    logger.warning("⚠️ GEMINI_API_KEY not set - AI features will be disabled")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

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

async def _make_api_request(prompt_text: str) -> Optional[Dict[str, Any]]:
    """Make API request with retry logic and timeout handling."""
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }
    last_error = None
    async with aiohttp.ClientSession() as session:
        for attempt in range(MAX_RETRIES):
            try:
                async with session.post(
                    URL, 
                    headers=headers, 
                    json=data, 
                    timeout=REQUEST_TIMEOUT
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        raw_text = result['candidates'][0]['content']['parts'][0]['text']
                        return json.loads(raw_text)
                    elif response.status == 429:
                        logger.warning(f"Rate limited, waiting {RETRY_DELAY * (attempt + 2)}s...")
                        await asyncio.sleep(RETRY_DELAY * (attempt + 2))
                    else:
                        resp_text = await response.text()
                        logger.error(f"Gemini API Error: {response.status} - {resp_text[:200]}")
                        return None
                        
            except asyncio.TimeoutError:
                last_error = "Request timed out"
                logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES}: Request timed out")
            except aiohttp.ClientError as e:
                last_error = f"Connection error: {e}"
                logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES}: Connection error")
            except json.JSONDecodeError as e:
                last_error = f"JSON parse error: {e}"
                logger.error(f"Failed to parse AI response: {e}")
                return None
            except KeyError as e:
                last_error = f"Unexpected response format: {e}"
                logger.error(f"Unexpected API response format: {e}")
                return None
            except Exception as e:
                last_error = str(e)
                logger.error(f"Unexpected error: {e}", exc_info=True)
                return None
            
            # Wait before retry
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
    
    logger.error(f"All {MAX_RETRIES} attempts failed. Last error: {last_error}")
    return None

async def get_ai_content(content_type: str, topic: Optional[str] = None, difficulty: str = "medium") -> Optional[Dict[str, Any]]:
    """
    Generates content using Google Gemini via REST API.
    
    Args:
        content_type: 'question', 'fact', or 'formula'
        topic: Optional topic code (SM, FM, SA, etc.)
        difficulty: 'easy', 'medium', or 'hard' (for questions only)
    
    Returns:
        Dict with generated content or None on failure
    """
    if not API_KEY:
        logger.error("GEMINI_API_KEY not found.")
        return None

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
    
    return await _make_api_request(prompt_text)

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
