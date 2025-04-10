import os
import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
from ctypes import windll

# Lese den API aus der .env Datei
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Fehler: OPENAI_API_KEY ist nicht gesetzt. Bitte überprüfe die .env-Datei.")
    exit(1)

# Globale Variable für das ausgewählte Modell
selected_model = "gpt-4o"  # Standardmodell

# Globale Liste für den Chatverlauf (Gedächtnis)
chat_memory = []  # Liste für den Chatverlauf
MAX_MEMORY_LENGTH = 10  # Maximal 10 Nachrichten im Gedächtnis

def set_model(model_name):
    """Funktion zur Auswahl des Modells."""
    global selected_model
    selected_model = model_name
    print(f"Modell geändert zu: {selected_model}")

# Definiere die Funktion, die mit der OpenAI API kommuniziert
def chat_with_gpt():
    try:
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=chat_memory,  # Sende den gesamten Chatverlauf
            max_tokens=2000,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content'].strip()
        else:
            return "Keine gültige Antwort von der API erhalten."
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

# Definiere die Funktion, die aufgerufen wird, wenn der Benutzer auf den Senden-Button klickt
def send_message(event=None):  # `event` wird hinzugefügt, um die Funktion auch bei Enter zu nutzen
    user_input = user_entry.get()
    if user_input.lower() == "exit":
        root.destroy()
        return

    # Benutzer-Eingabe in den Chatverlauf einfügen
    chat_history.insert(tk.END, f"Du: {user_input}\n")
    user_entry.delete(0, tk.END)

    # Benutzer-Nachricht zum Gedächtnis hinzufügen
    chat_memory.append({"role": "user", "content": user_input})

    # Gedächtnis begrenzen
    if len(chat_memory) > MAX_MEMORY_LENGTH:
        chat_memory.pop(0)  # Entferne die älteste Nachricht

    # Antwort von ChatGPT abrufen
    answer = chat_with_gpt()

    # Antwort in den Chatverlauf und ins Gedächtnis einfügen
    chat_history.insert(tk.END, f"ChatGPT: {answer}\n\n")
    chat_memory.append({"role": "assistant", "content": answer})

    chat_history.see(tk.END)

def on_entry_click(event):
    """Funktion, die den Placeholder-Text entfernt, wenn der Benutzer in das Eingabefeld klickt."""
    if user_entry.get() == "Hier Prompt eingeben":
        user_entry.delete(0, tk.END)
        user_entry.config(fg="black")

def on_focus_out(event):
    """Funktion, die den Placeholder-Text wieder hinzufügt, wenn das Eingabefeld leer ist."""
    if user_entry.get() == "":
        user_entry.insert(0, "Hier Prompt eingeben")
        user_entry.config(fg="grey")

# GUI erstellen
root = tk.Tk()
root.title("ChatGPT von Muffl")
# Icon hinzufügen
icon_path = "Icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
    if os.name == "nt":  # Nur auf Windows
        app_id = "ChatGPT.Muffl.App"  # Eine eindeutige App-ID
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
else:
    print("Warnung: Icon.ico nicht gefunden. Standard-Icon wird verwendet.")

# Menüleiste hinzufügen
menu_bar = tk.Menu(root)

# Datei-Menü
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Beenden", command=root.quit)
menu_bar.add_cascade(label="Datei", menu=file_menu)

# Model-Menü
model_menu = tk.Menu(menu_bar, tearoff=0)
model_menu.add_command(label="GPT-3.5", command=lambda: set_model("gpt-3.5-turbo"))
model_menu.add_command(label="GPT-4", command=lambda: set_model("gpt-4"))
model_menu.add_command(label="GPT-4o", command=lambda: set_model("gpt-4o"))
model_menu.add_command(label="4o-mini", command=lambda: set_model("gpt-4o-mini"))

menu_bar.add_cascade(label="Model", menu=model_menu)

# Parameter-Menü
parameter_menu = tk.Menu(menu_bar, tearoff=0)
parameter_menu.add_command(label="Max Tokens")
parameter_menu.add_command(label="Genauigkeit")
parameter_menu.add_command(label="Kreativität")

menu_bar.add_cascade(label="Parameter", menu=parameter_menu)

# Hilfe-Menü
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Über", command=lambda: messagebox.showinfo("Über", "ChatGPT von Muffl\nVersion 0.7"))
menu_bar.add_cascade(label="Hilfe", menu=help_menu)

# Menüleiste dem Fenster hinzufügen
root.config(menu=menu_bar)

# Chat-Verlauf
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40, state='normal')
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Eingabefeld
user_entry = tk.Entry(root, width=100, fg="grey")
user_entry.insert(0, "Hier Prompt eingeben")
user_entry.bind("<FocusIn>", on_entry_click)
user_entry.bind("<FocusOut>", on_focus_out)
user_entry.bind("<Return>", send_message)  # Enter-Taste mit `send_message` verknüpfen
user_entry.grid(row=1, column=0, padx=10, pady=10)

# Senden-Button
send_button = tk.Button(root, text="Senden", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Stop-Button
break_button = tk.Button(root, text="Stop", command=root.quit)  # Button zum Beenden der Anwendung
break_button.grid(row=2, column=1, padx=10, pady=10)

# GUI starten
root.mainloop()