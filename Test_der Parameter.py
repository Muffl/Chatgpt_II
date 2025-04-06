import openai
from dotenv import load_dotenv
import os

# Lese den API-Schlüssel aus der .env-Datei
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Fehler: OPENAI_API_KEY ist nicht gesetzt. Bitte überprüfe die .env-Datei.")
    exit(1)

def test_temperature_and_tokens(prompt, temperature, max_tokens):
    """Testet die OpenAI-API mit verschiedenen Parametern."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Chat-Modell
            messages=[{"role": "user", "content": prompt}],  # Chat-Format
            temperature=temperature,
            max_tokens=max_tokens
        )
        print(f"Prompt: {prompt}\nResponse:\n{response['choices'][0]['message']['content'].strip()}\n")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Testfälle definieren
test_cases = [
    {"prompt": "Erkläre das Konzept der Evolution.", "temperature": 0.2, "max_tokens": 50},
    {"prompt": "Erkläre das Konzept der Evolution.", "temperature": 0.8, "max_tokens": 150},
    {"prompt": "Was ist künstliche Intelligenz?", "temperature": 0.5, "max_tokens": 100}
]

# Tests durchführen
for case in test_cases:
    print(f"Testing with Temperature={case['temperature']} and Max Tokens={case['max_tokens']}")
    test_temperature_and_tokens(case["prompt"], case["temperature"], case["max_tokens"])
    print("-" * 50)