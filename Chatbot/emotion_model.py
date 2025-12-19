# emotion_model.py
from transformers import pipeline

# Load GoEmotions emotion classifier
emotion_classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=3
)

# Map GoEmotions labels to mental-health categories
EMOTION_MAP = {
    "sadness": "sadness",
    "grief": "sadness",
    "disappointment": "sadness",
    "fear": "anxiety",
    "nervousness": "anxiety",
    "anxiety": "anxiety",
    "anger": "frustration",
    "annoyance": "frustration",
    "neutral": "neutral",
    "joy": "positive",
    "optimism": "positive",
    "relief": "positive",
    "exhaustion": "emotional_exhaustion"
}

def detect_emotion(text):
    results = emotion_classifier(text)[0]

    for item in results:
        label = item["label"].lower()
        score = item["score"]

        if label in EMOTION_MAP:
            return EMOTION_MAP[label], score

    return "neutral", 0.5
