from flask import Flask, request, jsonify
from response import generate_response
from emotion_model import detect_emotion
from distress_scoring import get_distress_level

app = Flask(__name__)

# In-memory session store (hackathon-safe)
sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id", "default")
    user_text = data.get("message", "").strip()

    if not user_text:
        return jsonify({"response": "Please say something so I can help."})

    # Initialize session memory
    if session_id not in sessions:
        sessions[session_id] = {
            "turn_count": 0,
            "last_emotion": None,
            "emotion_history": [],
            "last_bot_action": None
        }

    session = sessions[session_id]
    session["turn_count"] += 1

    # ---- Emotion pipeline ----
    emotion, score = detect_emotion(user_text)
    distress = get_distress_level(emotion, score)

    if emotion not in ["neutral", None]:
        session["last_emotion"] = emotion
        session["emotion_history"].append(emotion)
        session["emotion_history"] = session["emotion_history"][-5:]

    # ---- Generate response ----
    reply = generate_response(
        emotion=emotion,
        distress_level=distress,
        turn_count=session["turn_count"],
        user_text=user_text,
        last_emotion=session["last_emotion"],
        emotion_history=session["emotion_history"],
        last_bot_action=session["last_bot_action"]
    )

    # Update bot intent memory
    if "try" in reply.lower():
        session["last_bot_action"] = "offered_coping"
    else:
        session["last_bot_action"] = "general_support"

    return jsonify({
        "response": reply,
        "emotion": emotion,
        "distress_level": distress
    })

if __name__ == "__main__":
    # CRITICAL: allows other devices to connect
    app.run(host="0.0.0.0", port=5000, debug=False)
