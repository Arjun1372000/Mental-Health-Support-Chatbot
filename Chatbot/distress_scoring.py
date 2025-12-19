# distress_scoring.py

def get_distress_level(emotion, score):
    if emotion in ["sadness", "anxiety", "emotional_exhaustion"]:
        if score > 0.75:
            return "moderate"
        elif score > 0.9:
            return "high"
    return "low"
