import os
import google.generativeai as genai
import json
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
else:
    model = None
    print("Warning: GEMINI_API_KEY not found in environment variables.")

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
    Generates content using Google Gemini.
    content_type: 'question', 'fact', or 'formula'
    Returns: Dict or None
    """
    if not model:
        return None

    try:
        prompt = ""
        if content_type == "question":
            prompt = QUESTION_PROMPT
        elif content_type == "fact":
             prompt = FACT_PROMPT
        elif content_type == "formula":
             prompt = FORMULA_PROMPT
        else:
            return None

        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None

if __name__ == "__main__":
    # Test the service
    print("Testing AI Service...")
    print(get_ai_content("question"))
