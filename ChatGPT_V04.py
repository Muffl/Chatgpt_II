import openai
import tkinter as tk
from tkinter import scrolledtext

# Setze deinen OpenAI API-Schlüssel hier ein
openai.api_key = "DEIN_API_SCHLÜSSEL_HIER"
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein hilfsbereiter Assistent. Du sagst 'du' zu mir."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

def send_message():
    user_input = user_entry.get()
    if user_input.strip().lower() == "exit":
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
#root.iconbitmap("chatgpt_icon_48x48.ico") 

# Chat-Verlauf
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40, state='normal')
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Eingabefeld
user_entry = tk.Entry(root, width=100, fg="grey")
user_entry.insert(0, "Hier Prompt eingeben")
user_entry.bind("<FocusIn>", on_entry_click)
user_entry.bind("<FocusOut>", on_focus_out)
user_entry.grid(row=1, column=0, padx=10, pady=10)

# Senden-Button
send_button = tk.Button(root, text="Senden", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# GUI starten
root.mainloop()