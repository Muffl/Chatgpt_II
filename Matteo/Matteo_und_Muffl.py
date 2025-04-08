import os
from tkinter.font import BOLD
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
    exit()

# Globale Variable für das ausgewählte Modell
selected_model = "gpt-4o"  # Standardmodell

# Gobale Variable für Tokens
max_tokens = 2048  # Standardwert für Tokens

#Globale Variable für Temperatur
temperature = 0.7  # Standardwert für Temperatur


# Globale Liste für den Chatverlauf (Gedächtnis)
chat_memory = []  # Liste für den Chatverlauf
MAX_MEMORY_LENGTH = 10  # Maximal 10 Nachrichten im Gedächtnis

def set_model(model_name):
    """Funktion zur Auswahl des Modells."""
    global selected_model
    selected_model = model_name
    # print(f"Modell geändert zu: {selected_model}")

# Maximale Anzahl von Tokens einstellen
def set_max_tokens():
    """Öffnet ein Fenster, um die maximale Anzahl von Tokens einzustellen."""
    def save_tokens():
        try:
            global max_tokens
            new_value = int(token_entry.get())
            if 100 <= new_value <= 4096:  # Gültigkeitsbereich prüfen
                max_tokens = new_value
                messagebox.showinfo("Erfolg", f"Max Tokens wurde auf {max_tokens} gesetzt.")
                token_window.destroy()
                update_model_label()  # Aktualisiere das Label
            else:
                messagebox.showerror("Fehler", "Bitte einen Wert zwischen 100 und 4096 eingeben. Standardwert ist 2048.")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")
       
    # Neues Fenster erstellen
    token_window = tk.Toplevel(root)
    token_window.title("Max Tokens einstellen")
    token_window.geometry("300x150")
    token_window.resizable(False, False)

    # Label und Eingabefeld
    tk.Label(token_window, text="Max Tokens (100 - 4096):").pack(pady=10)
    token_entry = tk.Entry(token_window, width=10)
    token_entry.insert(0, str(max_tokens))  # Aktuellen Wert anzeigen
    token_entry.pack(pady=5)

    # Speichern-Button
    save_button = tk.Button(token_window, text="Speichern", command=save_tokens)
    save_button.pack(pady=10)

# Einstellen der Temperatur
def set_temperature():
    """Öffnet ein Fenster, um die Temperatur einzustellen."""
    def save_temperature():
        try:
            global temperature
            new_value = float(temp_entry.get())
            if 0.0 <= new_value <= 2.0:  # Gültigkeitsbereich prüfen
                temperature = new_value
                messagebox.showinfo("Erfolg", f"Temperatur wurde auf {temperature} gesetzt.")
                temp_window.destroy()
                update_model_label()  # Aktualisiere das Label
            else:
                messagebox.showerror("Fehler", "Bitte einen Wert zwischen 0.0 und 2.0 eingeben. Standardwert ist 0.7.")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

    # Neues Fenster erstellen
    temp_window = tk.Toplevel(root)
    temp_window.title("Temperatur einstellen")
    temp_window.geometry("300x150")
    temp_window.resizable(False, False)

    # Label und Eingabefeld
    tk.Label(temp_window, text="Temperatur (0.0 - 2.0):").pack(pady=10)
    temp_entry = tk.Entry(temp_window, width=10)
    temp_entry.insert(0, str(temperature))  # Aktuellen Wert anzeigen
    temp_entry.pack(pady=5)

    # Speichern-Button
    save_button = tk.Button(temp_window, text="Speichern", command=save_temperature)
    save_button.pack(pady=10)

# Einstellen der Gedächtnislänge
def set_memory_length():
    """Öffnet ein Fenster, um die maximale Anzahl von Nachrichten im Gedächtnis einzustellen."""
    def save_memory_length():
        try:
            global MAX_MEMORY_LENGTH
            new_value = int(memory_entry.get())
            if 1 <= new_value <= 20:  # Gültigkeitsbereich prüfen
                MAX_MEMORY_LENGTH = new_value
                messagebox.showinfo("Erfolg", f"Maximale Gedächtnislänge wurde auf {MAX_MEMORY_LENGTH} gesetzt.")
                memory_window.destroy()
                update_model_label()  # Aktualisiere das Label
            else:
                messagebox.showerror("Fehler", "Bitte einen Wert zwischen 1 und 20 eingeben. Standardwert ist 10.")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben.")

    # Neues Fenster erstellen
    memory_window = tk.Toplevel(root)
    memory_window.title("Gedächtnislänge einstellen")
    memory_window.geometry("300x150")
    memory_window.resizable(False, False)

    # Label und Eingabefeld
    tk.Label(memory_window, text="Maximale Gedächtnislänge (1 - 20):").pack(pady=10)
    memory_entry = tk.Entry(memory_window, width=10)
    memory_entry.insert(0, str(MAX_MEMORY_LENGTH))  # Aktuellen Wert anzeigen
    memory_entry.pack(pady=5)

    # Speichern-Button
    save_button = tk.Button(memory_window, text="Speichern", command=save_memory_length)
    save_button.pack(pady=10)


# Definiere die Funktion, die mit der OpenAI API kommuniziert
def chat_with_gpt():
    try:
        response = openai.ChatCompletion.create(
            model=selected_model,  # Das ausgewählte Modell
            messages=chat_memory,  # Sende den gesamten Chatverlauf
            max_tokens=max_tokens,  # Maximal 2048 Tokens für die Antwort
            temperature=temperature, # Temperatur für Kreativität
            top_p=1.0, 
            frequency_penalty=0.0, #
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
    chat_history.insert(tk.END, f"Matteo sagt:\n", "bold") # "Matteo sagt:" in fetter Schrift
    chat_history.insert(tk.END, f"{user_input}\n") # Antwort in normaler Schrift
    
    user_entry.delete(0, tk.END) #

    # Benutzer-Nachricht zum Gedächtnis hinzufügen
    chat_memory.append({"role": "user", "content": user_input})

    # Gedächtnis begrenzen
    if len(chat_memory) > MAX_MEMORY_LENGTH:
        chat_memory.pop(0)  # Entferne die älteste Nachricht

    # Antwort von ChatGPT abrufen
    answer = chat_with_gpt()

    # Antwort in den Chatverlauf und ins Gedächtnis einfügen
    '''
    chat_history.insert(tk.END, f"ChatGPT:\n {answer}\n\n") 
    chat_memory.append({"role": "assistant", "content": answer})
    '''
    chat_history.insert(tk.END, "Muffl antwortet:\n", "bold")  # "ChatGPT:" in fetter Schrift
    chat_history.insert(tk.END, f"{answer}\n\n")  # Antwort in normaler Schrift
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
        user_entry.config(fg="black")

def new_chat():
    """Startet einen neuen Chat, indem der Verlauf und das Gedächtnis zurückgesetzt werden."""
    global chat_memory
    chat_memory = []  # Gedächtnis leeren
    chat_history.delete(1.0, tk.END)  # Chatverlauf im GUI leeren
    chat_history.insert(tk.END, "Neuer Chat gestartet.\n\n")  # Hinweis im Chatverlauf

# GUI erstellen
root = tk.Tk()
root.title("Gespräch zwiwschen Matteo und Muffl")
root.geometry("840x820") # Fenstergröße
root.resizable(0, 0)  # Fenstergröße anpassbar

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
#parameter_menu.add_command(label="Max Tokens")
parameter_menu.add_command(label="Temperatur einstellen", command=set_temperature)
parameter_menu.add_command(label="Tokens einstellen", command=set_max_tokens)
parameter_menu.add_command(label="Gedächtnis einstellen", command=set_memory_length)

menu_bar.add_cascade(label="Parameter", menu=parameter_menu)

# Hilfe-Menü
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Über", command=lambda: messagebox.showinfo("Über", "ChatGPT von Muffl\nVersion 0.11\n(c) 2025 by Muffl"))
help_menu.add_command(label="Über Temperatur", command=lambda: messagebox.showinfo("Was bedeutet...", "Temperatur:\n\nSteuert die Kreativität und Zufälligkeit der Antworten des Modells.\n\
                                                                                     \nWertbereich 0.0 - 2.0\n\
                                                                                      Standardwert: 0.7\n\nJe höher der Wert, desto kreativer und unvorhersehbarer die Antworten."))
help_menu.add_command(label="Über Tokens", command=lambda: messagebox.showinfo("Was bedeutet...", "Tokens:\n\nWie lang soll eine Antwort ausfallen?\n\
                                                                                     \nWertbereich 100 - 4096\n\
                                                                                      Standardwert: 2048\n\nJe höher der Wert, desto länger die Antwort."))
help_menu.add_command(label="Über Gedächnis", command=lambda: messagebox.showinfo("Was bedeutet...", "Gedächnis:\n\nMaximale Antworten die im Chatverlauf berücksicht werden\n\
                                                                                     \nWertbereich 1 - 20\n\
                                                                                      Standardwert: 10\n\nJe höher der Wert, desto mehr Antworten werden berücksichtigt."))
menu_bar.add_cascade(label="Hilfe", menu=help_menu)

# Menüleiste dem Fenster hinzufügen
root.config(menu=menu_bar)

# Chat-Verlauf
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40, state='normal')
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Füge eine Text-Tag-Konfiguration für fette Schrift hinzu
chat_history.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))

# Eingabefeld
user_entry = tk.Entry(root, width=120, fg="grey")
#user_entry = tk.Text(root, height=2, width=100, fg="grey", wrap=tk.WORD)
user_entry.insert(0, "Hier Prompt eingeben")
user_entry.bind("<FocusIn>", on_entry_click)
user_entry.bind("<FocusOut>", on_focus_out)
user_entry.bind("<Return>", send_message)  # Enter-Taste mit `send_message` verknüpfen
user_entry.grid(row=1, column=0, padx=10, pady=10)

# Senden-Button
send_button = tk.Button(root, text="Senden", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Stop-Button
break_button = tk.Button(root, text="Ende", command=root.quit)  # Button zum Beenden der Anwendung
break_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Neuer Chat-Button
new_chat_button = tk.Button(root, text="Neuer Chat", command=new_chat)
new_chat_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Label für das verwendete Modell und Parameter
model_label = tk.Label(
    root,
    text=f"Verwendetes Modell: {selected_model}\nTemperatur: {temperature}, Tokens: {max_tokens}, Gedächtnis: {MAX_MEMORY_LENGTH}",
    anchor="w"
)
model_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
def update_model_label():
    """Aktualisiert das Label mit dem verwendeten Modell und den Parametern."""
    model_label.config(
        text=f"Verwendetes Modell: {selected_model}\n"
             f"Temperatur: {temperature}, Tokens: {max_tokens}, Gedächtnis: {MAX_MEMORY_LENGTH}"
    )

def set_model(model_name):
    """Funktion zur Auswahl des Modells."""
    global selected_model
    selected_model = model_name
    # print(f"Modell geändert zu: {selected_model}")
    update_model_label()

# GUI starten
root.mainloop()