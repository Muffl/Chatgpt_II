import os
import openai
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv

load_dotenv()


# Lese den API aus der .env Datei
openai.api_key = os.getenv("OPENAI_API_KEY")

# Definiere die Funktion, die mit der OpenAI API kommuniziert
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein hilfsbereiter Assistent. Du sagst 'du' zu mir."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"
    
# Definiere die Funktion, die aufgerufen wird, wenn der Benutzer auf den Senden-Button klickt
def send_message(event=None):  # `event` wird hinzugefügt, um die Funktion auch bei Enter zu nutzen
    user_input = user_entry.get()
    if user_input.lower() == "exit":
        root.destroy()
        return
    chat_history.insert(tk.END, f"Du: {user_input}\n")
    user_entry.delete(0, tk.END)
    answer = chat_with_gpt(user_input)
    chat_history.insert(tk.END, f"ChatGPT: {answer}\n\n")
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
root.iconbitmap("Icon.ico") 

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

break_button = tk.Button(root, text="Stop", command=root.quit)  # Button zum Beenden der Anwendung
break_button.grid(row=2, column=1, padx=10, pady=10)

# GUI starten
root.mainloop()