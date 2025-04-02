import openai

# Setze deinen OpenAI API-Schlüssel hier ein
openai.api_key = 'Hier API Key einfügen'

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein hilfsbereiter Assistent. Du sagst 'du' zu mir."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

if __name__ == "__main__":
    # Endlosschleife für den Chat
    print("Willkommen zum Chat mit ChatGPT! Tippe 'exit', um das Programm zu beenden.")
    while True:
        user_input = input("Gib deine Frage ein: ")
        if user_input.lower() == "exit":
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        answer = chat_with_gpt(user_input)
        print("ChatGPT antwortet:")
        print(answer)