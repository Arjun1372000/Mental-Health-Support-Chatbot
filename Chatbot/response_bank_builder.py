import json
from emotion_model import detect_emotion

with open("data/mental_health_intents.json", "r") as f:
    data = json.load(f)

intents = data["intents"]
all_responses = []

for intent in intents:
    for r in intent.get("responses", []):
        all_responses.append({
            "tag": intent["tag"],
            "text": r
        })

TAG_TO_EMOTION = {
    "greeting": "neutral",
    "morning": "neutral",
    "afternoon": "neutral",
    "evening": "neutral",
    "night": "neutral",
    "sad": "sadness",
    "depressed": "sadness",
    "anxiety": "anxiety",
    "stress": "anxiety",
    "lonely": "sadness"
}

def get_emotion(tag, text):
    if tag in TAG_TO_EMOTION:
        return TAG_TO_EMOTION[tag]
    emotion, _ = detect_emotion(text)
    return emotion

def detect_style(text):
    t = text.lower()

    if any(p in t for p in ["how are you", "glad to see", "great to see"]):
        return "validation"

    if any(p in t for p in ["what brings you", "how has your day", "what's going on"]):
        return "reflection"

    if any(p in t for p in ["try", "help", "would you like to"]):
        return "coping"

    return "encouragement"

response_bank = {}

for item in all_responses:
    text = item["text"]
    tag = item["tag"]

    emotion = get_emotion(tag, text)
    style = detect_style(text)

    response_bank.setdefault(emotion, {})
    response_bank[emotion].setdefault(style, [])
    response_bank[emotion][style].append(text)

for emotion in response_bank:
    for style in response_bank[emotion]:
        response_bank[emotion][style] = list(
            set(response_bank[emotion][style])
        )

with open("data/mental_health_response_bank.json", "w") as f:
    json.dump(response_bank, f, indent=2)
