from transformers import pipeline
import numpy as np
from datetime import datetime, timezone


emotion_pipe = pipeline(
    task="text-classification",
    model="minuva/MiniLMv2-goemotions-v2",
    top_k=None
)

sentiment_pipe = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_text(text: str):
    """
    Takes user text and returns ML-derived features
    """

    # Emotion
    emotions = emotion_pipe(text)[0]
    top_emotion = max(emotions, key=lambda x: x["score"])

    # Sentiment
    sentiment = sentiment_pipe(text)[0]
    sentiment_score = sentiment["score"]
    if sentiment["label"] == "NEGATIVE":
        sentiment_score *= -1

    # Simple risk heuristic (SAFE)
    risk_level = classify_risk(sentiment_score, top_emotion["label"])

    # Features for DB (NO RAW TEXT STORED)
    features = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "emotion": top_emotion["label"],
        "emotion_score": round(top_emotion["score"], 3),
        "sentiment_score": round(sentiment_score, 3),
        "message_length": len(text.split()),
        "risk_level": risk_level
    }

    return features 
# {'timestamp': '2025-12-18T22:50:01.150073+00:00', 'emotion': 'sadness', 'emotion_score': 0.941, 'sentiment_score': -0.998, 'message_length': 7, 'risk_level': 'ELEVATED'}


#RISK CLASSIFICATION (NOT PREDICTION)
def classify_risk(sentiment_score, emotion):
    """
    Returns LOW / MODERATE / ELEVATED
    """

    if sentiment_score < -0.6 and emotion in ["sadness", "fear", "anger"]:
        return "ELEVATED"

    if sentiment_score < -0.3:
        return "MODERATE"

    return "LOW"
