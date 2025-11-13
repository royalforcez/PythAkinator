from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# On garde la conversation en mémoire ici (reset possible)
conversation = [
    {
        "role": "system",
        "content": "Take on the role of a famous personality and mimic them. \
        Your goal is to make us guess who you are through the questions we ask you. Never says Congratulation unless if we find and ONLY then"
    }
]

# Tabelleau pour suivre le score
score = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global conversation
    global score
    data = request.get_json()
    user_message = data.get("message", "").strip()

# Gestion des commandes spéciales
    if user_message.lower() in ["quit", "exit", "stop"]:
        return jsonify({"reply": "🔴 Conversation ended.", "score": score})
    elif user_message.lower() == "reset":
        conversation = [
            {
                "role": "system",
                "content": "Take on the role of a famous personality and mimic them. \
                Your goal is to make us guess who you are through the questions we ask you. Never says Congratulation unless if we find and ONLY then"
            }
        ]
        score = 0
        return jsonify({"reply": "⚡ Conversation reset.", "score": score})

    # Ajouter le message de l’utilisateur
    conversation.append({"role": "user", "content": user_message})

    # Appeler Ollama
    response = ollama.chat(model="gemma3:12b", messages=conversation)

    # Récupérer la réponse
    ai_reply = response["message"]["content"]

    # Ajouter la réponse à la conversation
    conversation.append({"role": "assistant", "content": ai_reply})
    
    # Si l'IA félicite (ex: "Congratulation" / "Congratulations"), incrémenter le score
    if "congrat" in ai_reply.lower():
        score += 1

    return jsonify({"reply": ai_reply, "score": score})

@app.route("/score", methods=["GET"])
def get_score():
    return jsonify({"score": score})

if __name__ == "__main__":
    app.run(debug=True)
