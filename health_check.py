import os
import asyncio
import logging
import requests
import aiohttp
import json
from telegram import Bot
from groq import Groq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load env vars
load_dotenv(override=True)

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

logging.basicConfig(level=logging.ERROR)

# Configuration from env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
GOOGLE_SHEETS_JSON = os.getenv("GOOGLE_SHEETS_JSON", "service_account.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AntigravityNotes")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

async def check_telegram():
    print(f"{BOLD}--- Telegram Bot Check ---{RESET}")
    if not TELEGRAM_BOT_TOKEN:
        print(f"{RED}❌ TELEGRAM_BOT_TOKEN not found!{RESET}")
        return False
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"{GREEN}[OK] Connected: @{bot_info.username} ({bot_info.first_name}){RESET}")
        return True
    except Exception as e:
        print(f"{RED}[ERROR] Telegram Error: {e}{RESET}")
        return False

async def check_gemini():
    print(f"\n{BOLD}--- Google Gemini AI Check ---{RESET}")
    if not GEMINI_API_KEY:
        print(f"{YELLOW}[SKIP] GEMINI_API_KEY not found. (Skipping){RESET}")
        return False
    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts": [{"text": "Say 'Gemini is Online'"}]}]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(GEMINI_URL, headers=headers, json=data, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"{GREEN}[OK] Gemini: {text.strip()}{RESET}")
                    return True
                else:
                    print(f"{RED}[ERROR] Gemini Error: {response.status} - {await response.text()}{RESET}")
                    return False
    except Exception as e:
        print(f"{RED}[ERROR] Gemini Exception: {e}{RESET}")
        return False

async def check_groq():
    print(f"\n{BOLD}--- Groq AI Check ---{RESET}")
    if not GROQ_API_KEY:
        print(f"{YELLOW}[SKIP] GROQ_API_KEY not found. (Skipping){RESET}")
        return False
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Groq is Online'"}],
        )
        print(f"{GREEN}[OK] Groq: {completion.choices[0].message.content.strip()}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[ERROR] Groq Error: {e}{RESET}")
        return False

async def check_openrouter():
    print(f"\n{BOLD}--- OpenRouter Check ---{RESET}")
    if not OPENROUTER_API_KEY:
        print(f"{YELLOW}[SKIP] OPENROUTER_API_KEY not found. (Skipping){RESET}")
        return False
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            },
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": "Say 'OpenRouter Online'"}],
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"{GREEN}[OK] OpenRouter: {data['choices'][0]['message']['content'].strip()}{RESET}")
            return True
        else:
            print(f"{RED}[ERROR] OpenRouter Error: {response.status_code} - {response.text}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[ERROR] OpenRouter Exception: {e}{RESET}")
        return False

async def check_huggingface():
    print(f"\n{BOLD}--- HuggingFace Check ---{RESET}")
    if not HUGGINGFACE_API_KEY:
        print(f"{YELLOW}[SKIP] HUGGINGFACE_API_KEY not found. (Skipping){RESET}")
        return False
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"{GREEN}[OK] Connected as: {user_info.get('name', 'Unknown')}{RESET}")
            return True
        else:
            print(f"{RED}[ERROR] HF Error: {response.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[ERROR] HF Exception: {e}{RESET}")
        return False

async def check_google_sheets():
    print(f"\n{BOLD}--- Google Sheets Check ---{RESET}")
    if not os.path.exists(GOOGLE_SHEETS_JSON):
        print(f"{RED}[ERROR] Google Sheets JSON not found: {GOOGLE_SHEETS_JSON}{RESET}")
        return False
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_JSON, scope)
        client = gspread.authorize(creds)
        sh = client.open(GOOGLE_SHEET_NAME)
        print(f"{GREEN}[OK] Successfully opened Sheet: '{GOOGLE_SHEET_NAME}'{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[ERROR] Google Sheets Error: {e}{RESET}")
        return False

async def main():
    print(f"\n{BOLD}Starting API Health Check for Antigravity Bot...{RESET}\n")
    
    results = [
        await check_telegram(),
        await check_gemini(),
        await check_groq(),
        await check_openrouter(),
        await check_huggingface(),
        await check_google_sheets()
    ]
    
    print(f"\n{BOLD}--- Execution Summary ---{RESET}")
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Total Checks: {total}")
    print(f"Passed: {passed}")
    print(f"Failed/Skipped: {total - passed}")
    
    if passed == total:
        print(f"\n{GREEN}{BOLD}ALL SYSTEMS GO!{RESET}")
    else:
        print(f"\n{YELLOW}{BOLD}Some systems are offline or misconfigured.{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
