import os
import json
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

QUESTION_PROMPT = """
Generate a challenging multiple-choice question (MCQ) for the Civil Engineering GATE exam.
Topics can include: Soil Mechanics, Fluid Mechanics, Structural Analysis, Environmental Engineering, Transportation, Geomatics, RCC, Steel Structures.
Ensure the question requires conceptual understanding or standard calculation.
The output format must be a JSON object with this exact structure:
{
  "question": "The question text here (max 300 chars)",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_option_id": 0,
  "explanation": "A clear explanation of the solution (max 200 chars)."
}
Note: correct_option_id must be an integer: 0 for 1st option, 1 for 2nd, etc.
"""

FACT_PROMPT = """
Generate a high-value "Key Note" or "One-Liner" for Civil Engineering GATE preparation.
It should be a key concept, important IS Code provision (IS 456, IS 800 etc), or a vital property of material.
Output JSON:
{
  "fact": "The text of the fact."
}
"""

FORMULA_PROMPT = """
Generate a key Civil Engineering formula often asked in GATE.
Output JSON:
{
  "title": "Name of the formula",
  "formula": "The mathematical expression (use plain text representation)",
  "explanation": "Brief explanation of specific terms and context."
}
"""

def get_ai_content(content_type):
    """
    Generates content using Google Gemini via REST API.
    content_type: 'question', 'fact', or 'formula'
    Returns: Dict or None
    """
    if not API_KEY:
        logger.error("GEMINI_API_KEY not found.")
        return None

    try:
        prompt_text = ""
        if content_type == "question":
            prompt_text = QUESTION_PROMPT
        elif content_type == "fact":
             prompt_text = FACT_PROMPT
        elif content_type == "formula":
             prompt_text = FORMULA_PROMPT
        else:
            return None

        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }

        response = requests.post(URL, headers=headers, json=data)
        
        if response.status_code != 200:
            logger.error(f"Gemini API Error: {response.status_code} - {response.text}")
            return None
            
        result = response.json()
        # Parse response
        # Structure: result['candidates'][0]['content']['parts'][0]['text']
        raw_text = result['candidates'][0]['content']['parts'][0]['text']
        return json.loads(raw_text)

    except Exception as e:
        logger.error(f"AI Generation Error: {e}")
        return None

if __name__ == "__main__":
    # Test
    print(get_ai_content("question"))

