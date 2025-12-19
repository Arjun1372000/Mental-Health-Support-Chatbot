# mood_tracker.py
import datetime

mood_log = []

def log_mood(emotion, distress_level):
    mood_log.append({
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "emotion": emotion,
        "distress_level": distress_level
    })

def get_mood_history():
    return mood_log
