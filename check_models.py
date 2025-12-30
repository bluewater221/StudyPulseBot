import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(URL)
print(response.text)
