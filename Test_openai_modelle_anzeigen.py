import openai
import os

# Stelle sicher, dass dein API-Schlüssel gesetzt ist
from dotenv import load_dotenv

load_dotenv()


# Lese den API aus der .env Datei
openai.api_key = os.getenv("OPENAI_API_KEY")

# Liste alle verfügbaren Modelle auf
models = openai.Model.list()

# Gib die Modellnamen aus
for model in models['data']:
    print(model['id'])