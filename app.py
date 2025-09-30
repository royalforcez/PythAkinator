from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# On garde la conversation en mémoire ici (reset possible)
conversation = [
    {
        "role": "system",
        "content": "Take on the role of a famous personality and mimic them. \
        Your goal is to make us guess who you are through the questions we ask you."
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global conversation
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # Gestion des commandes spéciales
    if user_message.lower() in ["quit", "exit", "stop"]:
        return jsonify({"reply": "🔴 Conversation ended."})
    elif user_message.lower() == "reset":
        conversation = [
            {
                "role": "system",
                "content": "Take on the role of a famous personality and mimic them. \
                Your goal is to make us guess who you are through the questions we ask you."
            }
        ]
        return jsonify({"reply": "⚡ Conversation reset."})

    # Ajouter le message de l’utilisateur
    conversation.append({"role": "user", "content": user_message})

    # Appeler Ollama
    response = ollama.chat(model="gemma3:12b", messages=conversation)

    # Récupérer la réponse
    ai_reply = response["message"]["content"]

    # Ajouter la réponse à la conversation
    conversation.append({"role": "assistant", "content": ai_reply})

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
