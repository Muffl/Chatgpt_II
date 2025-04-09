import os
from tkinter.font import BOLD
import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from dotenv import load_dotenv
from ctypes import windll

# -------------------- Initialisierung --------------------

# Lese den API-Key aus der .env Datei
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Fehler: OPENAI_API_KEY ist nicht gesetzt. Bitte überprüfe die .env-Datei.")
    exit()

# Globale Variablen
selected_model = "gpt-4o"  # Standardmodell
max_tokens = 2048  # Standardwert für Tokens
temperature = 0.7  # Standardwert für Temperatur
chat_memory = []  # Liste für den Chatverlauf
MAX_MEMORY_LENGTH = 10  # Maximal 10 Nachrichten im Gedächtnis

# -------------------- Funktionen für Parameter --------------------

def set_model(model_name):
    """Funktion zur Auswahl des Modells."""
    global selected_model
    selected_model = model_name
    update_model_label()

def set_max_tokens():
    """Öffnet ein Fenster, um die maximale Anzahl von Tokens einzustellen."""
    def save_tokens():
        try:
            global max_tokens
            new_value = int(token_entry.get())
            if 100 <= new_value <= 4096:
                max_tokens = new_value
                messagebox.showinfo("Erfolg", f"Max Tokens wurde auf {max_tokens} gesetzt.")
                token_window.destroy()
                update_model_label()
            else:
                messagebox.showerror("Fehler", "Bitte einen Wert zwischen 100 und 4096 eingeben.")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

    token_window = tk.Toplevel(root)
    token_window.title("Max Tokens einstellen")
    token_window.geometry("300x150")
    token_window.resizable(False, False)
    tk.Label(token_window, text="Max Tokens (100 - 4096):").pack(pady=10)
    token_entry = tk.Entry(token_window, width=10)
    token_entry.insert(0, str(max_tokens))
    token_entry.pack(pady=5)
    tk.Button(token_window, text="Speichern", command=save_tokens).pack(pady=10)

def set_temperature():
    """Öffnet ein Fenster, um die Temperatur einzustellen."""
    def save_temperature():
        try:
            global temperature
            new_value = float(temp_entry.get())
            if 0.0 <= new_value <= 2.0:
                temperature = new_value
                messagebox.showinfo("Erfolg", f"Temperatur wurde auf {temperature} gesetzt.")
                temp_window.destroy()
                update_model_label()
            else:
                messagebox.showerror("Fehler", "Bitte einen Wert zwischen 0.0 und 2.0 eingeben.")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

    temp_window = tk.Toplevel(root)
    temp_window.title("Temperatur einstellen")
    temp_window.geometry("300x150")
    temp_window.resizable(False, False)
    tk.Label(temp_window, text="Temperatur (0.0 - 2.0):").pack(pady=10)
    temp_entry = tk.Entry(temp_window, width=10)
    temp_entry.insert(0, str(temperature))
    temp_entry.pack(pady=5)
    tk.Button(temp_window, text="Speichern", command=save_temperature).pack(pady=10)

def set_memory_length():
    """Öffnet ein Fenster, um die maximale Anzahl von Nachrichten im Gedächtnis einzustellen."""
    def save_memory_length():
        try:
            global MAX_MEMORY_LENGTH
            new_value = int(memory_entry.get())
            if 1 <= new_value <= 20:
                MAX_MEMORY_LENGTH = new_value
                messagebox.showinfo("Erfolg", f"Maximale Gedächtnislänge wurde auf {MAX_MEMORY_LENGTH} gesetzt.")
                memory_window.destroy()
                update_model_label()
            else:
                messagebox.showerror("Fehler", "Bitte einen Wert zwischen 1 und 20 eingeben.")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

    memory_window = tk.Toplevel(root)
    memory_window.title("Gedächtnislänge einstellen")
    memory_window.geometry("300x150")
    memory_window.resizable(False, False)
    tk.Label(memory_window, text="Maximale Gedächtnislänge (1 - 20):").pack(pady=10)
    memory_entry = tk.Entry(memory_window, width=10)
    memory_entry.insert(0, str(MAX_MEMORY_LENGTH))
    memory_entry.pack(pady=5)
    tk.Button(memory_window, text="Speichern", command=save_memory_length).pack(pady=10)

def reset_parameters():
    """Setzt alle Parameter auf die Standardwerte zurück."""
    global max_tokens, temperature, MAX_MEMORY_LENGTH
    max_tokens = 2048
    temperature = 0.7
    MAX_MEMORY_LENGTH = 10
    update_model_label()
    messagebox.showinfo("Erfolg", "Alle Parameter wurden auf die Standardwerte zurückgesetzt.")

# -------------------- Funktionen für Chat-Interaktion --------------------

def chat_with_gpt():
    """Kommuniziert mit der OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=chat_memory,
            max_tokens=max_tokens,
            temperature=temperature,
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

def send_message(event=None):
    """Sendet eine Nachricht und zeigt die Antwort im Chatverlauf an."""
    user_input = user_entry.get()
    if user_input.lower() == "exit":
        root.destroy()
        return

    # Zeige den Benutzerinput im Chatverlauf
    chat_history.insert(tk.END, f"Du:\n", "bold")
    chat_history.insert(tk.END, f"{user_input}\n")
    
    # Setze den Eingabetext auf "Bitte warten ... Ich denke" und deaktiviere die Eingabe
    user_entry.delete(0, tk.END)
    user_entry.insert(0, "Bitte warten ... Ich denke")
    user_entry.config(state="disabled")
    root.update()  # Aktualisiere die GUI, damit der Text angezeigt wird

    # Füge die Benutzernachricht zum Chatverlauf hinzu
    chat_memory.append({"role": "user", "content": user_input})
    if len(chat_memory) > MAX_MEMORY_LENGTH:
        chat_memory.pop(0)

    # Hole die Antwort von ChatGPT
    answer = chat_with_gpt()

    # Zeige die Antwort im Chatverlauf
    chat_history.insert(tk.END, "ChatGPT:\n", "bold")
    chat_history.insert(tk.END, f"{answer}\n\n")
    chat_memory.append({"role": "assistant", "content": answer})
    chat_history.see(tk.END)

    # Aktiviere die Eingabe wieder und lösche den Text
    user_entry.config(state="normal")
    user_entry.delete(0, tk.END)
    chat_history.see(tk.END)

def new_chat():
    """Startet einen neuen Chat."""
    global chat_memory
    chat_memory = []
    chat_history.delete(1.0, tk.END)
    chat_history.insert(tk.END, "Neuer Chat gestartet.\n\n")

def save_chat_history():
    """Speichert den aktuellen Chatverlauf in einer Datei."""
    file_path = tk.filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(chat_history.get("1.0", tk.END).strip())
            messagebox.showinfo("Erfolg", "Chatverlauf wurde erfolgreich gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")

# -------------------- Funktionen für GUI --------------------

def toggle_darkmode():
    """Schaltet den Darkmode ein oder aus."""
    dark_bg = "#2E2E2E"
    dark_fg = "#FFFFFF"
    light_bg = "#F0F0F0"
    light_fg = "#000000"

    if root["bg"] == dark_bg:
        root.config(bg=light_bg)
        chat_history.config(bg=light_bg, fg=light_fg, insertbackground=light_fg)
        user_entry.config(bg=light_bg, fg="grey", insertbackground=light_fg)
        model_label.config(bg=light_bg, fg=light_fg)
        send_button.config(bg=light_bg, fg=light_fg)
        break_button.config(bg=light_bg, fg=light_fg)
        new_chat_button.config(bg=light_bg, fg=light_fg)
    else:
        root.config(bg=dark_bg)
        chat_history.config(bg=dark_bg, fg=dark_fg, insertbackground=dark_fg)
        user_entry.config(bg=dark_bg, fg=dark_fg, insertbackground=dark_fg)
        model_label.config(bg=dark_bg, fg=dark_fg)
        send_button.config(bg=dark_bg, fg=dark_fg)
        break_button.config(bg=dark_bg, fg=dark_fg)
        new_chat_button.config(bg=dark_bg, fg=dark_fg)

def update_model_label():
    """Aktualisiert das Label mit dem verwendeten Modell und den Parametern."""
    model_label.config(
        text=f"Verwendetes Modell: {selected_model}\n"
             f"Temperatur: {temperature}, Tokens: {max_tokens}, Gedächtnis: {MAX_MEMORY_LENGTH}"
    )

# -------------------- GUI Aufbau --------------------

root = tk.Tk()
root.title("ChatGPT von Muffl")
root.geometry("840x820")
root.resizable(0, 0)

icon_path = "Icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
    if os.name == "nt":
        app_id = "ChatGPT.Muffl.App"
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Chatverlauf speichern", command=save_chat_history)
file_menu.add_command(label="Beenden", command=root.quit)
menu_bar.add_cascade(label="Datei", menu=file_menu)

model_menu = tk.Menu(menu_bar, tearoff=0)
model_menu.add_command(label="GPT-3.5", command=lambda: set_model("gpt-3.5-turbo"))
model_menu.add_command(label="GPT-4", command=lambda: set_model("gpt-4"))
model_menu.add_command(label="GPT-4o", command=lambda: set_model("gpt-4o"))
model_menu.add_command(label="4o-mini", command=lambda: set_model("gpt-4o-mini"))
menu_bar.add_cascade(label="Model", menu=model_menu)

parameter_menu = tk.Menu(menu_bar, tearoff=0)
parameter_menu.add_command(label="Temperatur einstellen", command=set_temperature)
parameter_menu.add_command(label="Tokens einstellen", command=set_max_tokens)
parameter_menu.add_command(label="Gedächtnis einstellen", command=set_memory_length)
parameter_menu.add_command(label="Alle Parameter auf Standard setzen", command=reset_parameters)
parameter_menu.add_command(label="Darkmode ein/aus", command=toggle_darkmode)
menu_bar.add_cascade(label="Parameter", menu=parameter_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Über", command=lambda: messagebox.showinfo("Über", "ChatGPT von Muffl\nVersion V0.13\n(c) 2025 by Muffl"))
help_menu.add_command(label="Über Temperatur", command=lambda: messagebox.showinfo("Was bedeutet...", "Temperatur:\n\nSteuert die Kreativität und Zufälligkeit der Antworten des Modells.\n\nWertbereich 0.0 - 2.0\nStandardwert: 0.7"))
help_menu.add_command(label="Über Tokens", command=lambda: messagebox.showinfo("Was bedeutet...", "Tokens:\n\nWie lang soll eine Antwort ausfallen?\n\nWertbereich 100 - 4096\nStandardwert: 2048"))
help_menu.add_command(label="Über Gedächtnis", command=lambda: messagebox.showinfo("Was bedeutet...", "Gedächtnis:\n\nMaximale Antworten, die im Chatverlauf berücksichtigt werden.\n\nWertbereich 1 - 20\nStandardwert: 10"))
menu_bar.add_cascade(label="Hilfe", menu=help_menu)

root.config(menu=menu_bar)

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40, state='normal')
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
chat_history.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))

user_entry = tk.Entry(root, width=120, fg="black")
user_entry.insert(0, "Hier Prompt eingeben")
user_entry.bind("<FocusIn>", lambda event: user_entry.delete(0, tk.END) if user_entry.get() == "Hier Prompt eingeben" else None)
user_entry.bind("<FocusOut>", lambda event: user_entry.insert(0, "Hier Prompt eingeben") if user_entry.get() == "" else None)
user_entry.bind("<Return>", send_message)
user_entry.grid(row=1, column=0, padx=10, pady=10)

send_button = tk.Button(root, text="Senden", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

break_button = tk.Button(root, text="Ende", command=root.quit)
break_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

new_chat_button = tk.Button(root, text="Neuer Chat", command=new_chat)
new_chat_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

model_label = tk.Label(
    root,
    text=f"Verwendetes Modell: {selected_model}\nTemperatur: {temperature}, Tokens: {max_tokens}, Gedächtnis: {MAX_MEMORY_LENGTH}",
    anchor="w"
)
model_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# -------------------- Start der GUI --------------------

root.mainloop()