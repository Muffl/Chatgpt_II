🧠 ChatGPT von Muffl – Version 0.11

Ein lokal laufender Chat-Client für OpenAI's GPT-Modelle mit grafischer Benutzeroberfläche (Tkinter). Unterstützt GPT-3.5, GPT-4, GPT-4o und GPT-4o-mini.

🚀 Funktionen

Kommunikation mit OpenAI GPT-Modellen via openai.ChatCompletion.

Einstellbare Parameter direkt über die GUI:

Modellwahl (z. B. GPT-4)

Temperatur (0.0 – 2.0)

Token-Limit (100 – 4096)

Gedächtnislänge (1 – 20 letzte Nachrichten)

Neuer-Chat-Button zum Zurücksetzen des Verlaufs.

Intuitive Bedienung über ein einfaches Textfeld und Menüleisten.

Unterstützt .env-Datei zur sicheren API-Key-Verwaltung.

Benutzerfreundliche Hinweise und Fehlermeldungen.

⚙️ Voraussetzungen

Python 3.8+

Pakete: openai, tkinter, python-dotenv

Eine .env-Datei mit folgendem Eintrag:

OPENAI_API_KEY=dein_api_key

▶️ Start

python ChatGPT_V011.py

📁 Hinweise

Windows-Support mit individuellem App-Icon.

Das Icon muss Icon.ico heißen und im selben Verzeichnis liegen.

Taste Enter sendet den Prompt direkt ab.

🧠 Lizenz & Dank

© 2025 by Muffl – Für Lernzwecke, Spaß und Produktivität.
