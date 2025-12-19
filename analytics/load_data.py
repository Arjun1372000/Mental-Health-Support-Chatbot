import pandas as pd
from db.database import SessionLocal
from db.models import MentalHealthFeature

def load_features_df():
    session = SessionLocal()

    rows = session.query(MentalHealthFeature).all()

    data = [{
        "timestamp": r.timestamp,
        "emotion": r.emotion,
        "sentiment_score": r.sentiment_score,
        "message_length": r.message_length,
        "sadness_streak": r.sadness_streak,
        "risk_level": r.risk_level
    } for r in rows]

    session.close()

    df = pd.DataFrame(data)
    df = df.sort_values("timestamp")

    return df
