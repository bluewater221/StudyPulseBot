import random
from content import QUESTIONS, FACTS, FORMULAS

def generate_question():
    item = random.choice(QUESTIONS)
    text = f"🏗️ GATE Civil Question\n\n{item['question']}\n\n"
    for opt in item['options']:
        text += f"{opt}\n"
    text += "\nReply with A, B, C, or D. Answer will be revealed next hour."
    return text

def generate_fact():
    fact = random.choice(FACTS)
    text = f"📝 GATE Civil Key Note\n\n{fact}"
    return text

def generate_formula():
    item = random.choice(FORMULAS)
    text = f"📐 GATE Civil Formula\n\n{item['title']}\n{item['formula']}\n{item['explanation']}"
    return text

print("--- Question ---")
print(generate_question())
print("\n--- Fact ---")
print(generate_fact())
print("\n--- Formula ---")
print(generate_formula())
