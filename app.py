from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Store conversation history
conversation_history = []

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    # Get user message
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        # Generate response from Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly assistant and help the user to understand gene, protein structue and metabolic activities."
                },
                *conversation_history
            ]
        )

        # Extract bot reply
        bot_reply = response.choices[0].message.content

        # Save assistant response
        conversation_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        # Return response
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Clear chat history
@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
    
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)    