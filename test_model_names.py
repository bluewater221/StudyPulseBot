import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

models = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-2.0-flash-exp",
    "gemini-pro",
    "gemini-1.5-pro"
]

for m in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": "Hello"}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Model: {m} | Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Model: {m} | Exception: {e}")
