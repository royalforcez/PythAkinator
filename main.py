import ollama

# Fonction pour réinitialiser la conversation
def init_messages():
    return [
        {
            'role': 'system',
            'content': 'Take on the role of a famous personality and mimic them. Your goal is to make us guess who you are through the questions we ask you.',
        }
    ]

# On initialise la conversation
messages = init_messages()

print("🤖 AI Akinator started! Ask your questions (type 'quit' to exit, or 'reset' to restart).")

while True:
    # Input utilisateur
    user_input = input("You: ")
    
    if user_input.lower() in ["quit", "exit", "stop"]:
        print("👋 Ending game.")
        break
    elif user_input.lower() == "reset":
        messages = init_messages()  # ✅ on appelle la fonction qui recrée la base
        print("🔄 New game started! The AI has picked a new personality.")
        continue

    # Ajouter la question de l'utilisateur
    messages.append({'role': 'user', 'content': user_input})

    # Appel au modèle avec l'historique complet
    response = ollama.chat(model='gemma3:12b', messages=messages)

    # Récupérer la réponse du modèle
    reply = response['message']['content']
    print(f"AI: {reply}")

    # Ajouter la réponse du modèle à l'historique
    messages.append({'role': 'assistant', 'content': reply})
