import json
import random
from collections import Counter
from local_llm import generate_local_llm

# ====================
# CONFIG
# ====================
USE_LOCAL_LLM = True

# --------------------
# Load Response Bank
# --------------------
with open("data/mental_health_response_bank.json", "r", encoding="utf-8") as f:
    RESPONSE_BANK = json.load(f)

# --------------------
# Response Style Rotation
# --------------------
def get_response_style(turn_count):
    styles = ["validation", "reflection", "coping"]
    return styles[(turn_count - 1) % len(styles)]

# --------------------
# LLM-like Reasoning Layer
# --------------------
def decide_response_focus(prompt_state):
    if prompt_state["last_bot_action"] == "offered_coping":
        return "continue_coping"

    if len(prompt_state["user_input"].split()) <= 3:
        return "use_context"

    if prompt_state["distress_level"] in ["moderate", "high"]:
        return "ground_and_support"

    if prompt_state["current_emotion"] in ["sadness", "emotional_exhaustion"]:
        return "validate_and_reflect"

    return "general_support"

# --------------------
# Build Prompt State (LLM-style)
# --------------------
def build_prompt_state(
    user_input,
    emotion,
    distress_level,
    last_emotion,
    emotion_history,
    turn_count,
    last_bot_action
):
    trend = None
    if len(emotion_history) >= 3:
        trend = Counter(emotion_history).most_common(1)[0][0]

    return {
        "user_input": user_input,
        "current_emotion": emotion,
        "distress_level": distress_level,
        "last_emotion": last_emotion,
        "emotion_trend": trend,
        "turn_count": turn_count,
        "last_bot_action": last_bot_action
    }

# --------------------
# Build LLM Prompt (Mental Health Tuned)
# --------------------
def build_llm_prompt(state):
    return f"""
You are a supportive, empathetic mental health assistant.
You are NOT a medical professional.
Do NOT diagnose or give medical advice.

User message:
{state['user_input']}

Detected emotion: {state['current_emotion']}
Distress level: {state['distress_level']}
Previous emotion: {state['last_emotion']}
Recent emotional trend: {state['emotion_trend']}
Conversation turn: {state['turn_count']}
Last assistant action: {state['last_bot_action']}

Guidelines:
- Acknowledge the user's feelings
- Be calm, kind, and non-judgmental
- Ask at most ONE gentle follow-up question
- Keep the response concise and human
"""

# --------------------
# Final Response Generator (Single Source of Truth)
# --------------------
def generate_response(
    emotion,
    distress_level,
    turn_count,
    user_text,
    last_emotion,
    emotion_history=None,
    last_bot_action=None
):
    prompt_state = build_prompt_state(
        user_text,
        emotion,
        distress_level,
        last_emotion,
        emotion_history or [],
        turn_count,
        last_bot_action
    )

    focus = decide_response_focus(prompt_state)

    # ---- LLM-powered generation ----
    if USE_LOCAL_LLM and focus in [
        "use_context",
        "continue_coping",
        "ground_and_support",
        "validate_and_reflect",
        "general_support"
    ]:
        try:
            prompt = build_llm_prompt(prompt_state)
            return generate_local_llm(prompt)
        except Exception:
            pass  # safe fallback

    # ---- Dataset-grounded response ----
    style = get_response_style(turn_count)
    emotion_block = RESPONSE_BANK.get(emotion, {})
    style_responses = emotion_block.get(style)

    if style_responses:
        return random.choice(style_responses)

    # ---- Final safe fallback ----
    return (
        "I'm here with you. "
        "Would you like to tell me a bit more about what's been going on?"
    )
