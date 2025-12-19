from flask import Flask, render_template, request, jsonify
from datetime import datetime
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
import random

from database import init_db, get_mood_history, save_mood as db_save_mood

# -------------------------
# App Setup
# -------------------------
app = Flask(__name__)
init_db()

# -------------------------
# Emotion Detection (FAST)
# -------------------------
sia = SentimentIntensityAnalyzer()

def detect_emotion(text):
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.4:
        return "positive", round(score, 2)
    elif score <= -0.4:
        return "negative", round(score, 2)
    else:
        return "neutral", round(score, 2)

# -------------------------
# Chatbot Model (LOCAL)
# -------------------------
chatbot = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=180,
    temperature=0.85,
    top_p=0.95
)

# -------------------------
# Memory
# -------------------------
chat_logs = []

# -------------------------
# Chatbot Response Logic
# -------------------------
def generate_llm_response(user_text, emotion):
    prompt = (
        "You are a compassionate mental health support chatbot.\n"
        "You listen, acknowledge feelings, and respond naturally like a human.\n"
        "Do not give medical advice.\n\n"
        f"User: {user_text}\n"
        "Assistant:"
    )

    try:
        result = chatbot(prompt)[0]["generated_text"]
        reply = result.split("Assistant:")[-1].strip()

        if len(reply) < 15:
            raise Exception("Too short")

        return reply

    except Exception:
        fallback = {
            "negative": (
                "That sounds really difficult, and it makes sense that it would feel heavy. "
                "You don’t have to explain everything perfectly — I’m listening."
            ),
            "positive": (
                "It’s nice to hear that. Moments like that can be meaningful, even if they feel small."
            ),
            "neutral": (
                "I’m here with you. Take your time — whatever you want to share is okay."
            )
        }
        return fallback.get(emotion, fallback["neutral"])

# -------------------------
# Routes
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save_mood", methods=["POST"])
def save_mood():
    data = request.json
    mood = data.get("mood")
    db_save_mood(mood)
    return jsonify({"status": "saved"})

@app.route("/ai_chat", methods=["POST"])
def ai_chat():
    data = request.json
    message = data.get("message", "")

    # SAFETY LAYER
    crisis_words = ["suicide", "kill myself", "end my life", "self harm"]
    if any(w in message.lower() for w in crisis_words):
        return jsonify({
            "emotion": "distress",
            "confidence": 1.0,
            "reply": (
                "I’m really sorry you’re feeling this way. "
                "You don’t have to go through this alone.\n\n"
                "If you’re in India, please contact AASRA: 91-22-27546669."
            )
        })

    emotion, confidence = detect_emotion(message)
    reply = generate_llm_response(message, emotion)

    # Memory illusion
    if len(chat_logs) >= 3:
        reply += " From what you’ve been sharing, this seems to be something that’s been sitting with you."

    chat_logs.append({
        "text": message,
        "emotion": emotion,
        "confidence": confidence,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return jsonify({
        "emotion": emotion,
        "confidence": confidence,
        "reply": reply
    })

@app.route("/mood_data")
def mood_data():
    history = get_mood_history()
    return jsonify([
        {"mood": mood, "time": time}
        for mood, time in history[::-1]
    ])

@app.route("/stats_view")
def stats_view():
    return render_template("stats.html")

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
