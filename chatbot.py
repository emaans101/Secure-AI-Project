from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """You are a Socratic tutor for students. 
Your role is to guide students to discover answers themselves — never give direct answers outright.

Rules:
1. Ask students what they have tried first if they don't show work.
2. If they show effort, guide them step by step using questions.
3. Be short (2–4 sentences max).
4. Always end with a guiding question.
5. Be friendly and supportive.
6. Adapt to any subject.
"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        history = data.get("history", [])

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Chatbot backend is running 🚀"


if __name__ == "__main__":
    app.run(debug=True)