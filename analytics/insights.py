# from analytics.load_data import load_features_df
import pandas as pd

def basic_insights(df):
    return {
        "total_days": len(df),
        "avg_sentiment": round(df["sentiment_score"].mean(), 3),
        "most_common_emotion": df["emotion"].mode()[0],
        "max_sadness_streak": int(df["sadness_streak"].max())
    }

def risk_insights(df):
    return {
        "risk_distribution": df["risk_level"].value_counts().to_dict(),
        "elevated_days": int((df["risk_level"] == "ELEVATED").sum())
    }

def recent_trend(df, window=7):
    recent = df.tail(window)
    return {
        "avg_recent_sentiment": round(recent["sentiment_score"].mean(), 3),
        "dominant_emotion_last_7_days": recent["emotion"].mode()[0],
        "avg_sadness_streak_last_7_days": round(recent["sadness_streak"].mean(), 2)
    }

if __name__ == "__main__":
    df = pd.read_csv(r"mental_health_features.csv")  # Replace with load_features_df() in real use

    print("BASIC INSIGHTS")
    print(basic_insights(df))

    print("\nRISK INSIGHTS")
    print(risk_insights(df))

    print("\nRECENT TREND")
    print(recent_trend(df))
