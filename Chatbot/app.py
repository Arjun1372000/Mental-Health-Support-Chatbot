import streamlit as st
from emotion_model import detect_emotion
from distress_scoring import get_distress_level
from response import generate_response
from mood_tracker import log_mood, get_mood_history

st.set_page_config(page_title="Mental Health Support Chatbot")

st.title("Mental Health Support Chatbot")   
st.caption("This chatbot provides emotional support and is not a medical professional.")

# --------------------
# Session State Setup
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0

if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = None

if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []

if "last_bot_action" not in st.session_state:
    st.session_state.last_bot_action = None

if "last_suggested_activity" not in st.session_state:
    st.session_state.last_suggested_activity = None

# --------------------
# Display Chat History
# --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------
# User Input
# --------------------
user_input = st.chat_input("How are you feeling today?")

if user_input:
    st.session_state.turn_count += 1

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --------------------
    # Handle short replies (context-aware)
    # --------------------
    short_yes = ["yes", "yeah", "yep", "sure", "okay", "ok"]

    if user_input.lower().strip() in short_yes:
        if st.session_state.last_bot_action == "offered_coping":
            bot_reply = (
                "Alright. Let’s try something gentle together.\n\n"
                "Take a slow breath in through your nose for 4 seconds…\n"
                "Hold it briefly, then slowly breathe out."
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": bot_reply}
            )
            with st.chat_message("assistant"):
                st.markdown(bot_reply)

            st.session_state.last_bot_action = "coping_flow"
            st.stop()

    # --------------------
    # AI Pipeline
    # --------------------
    emotion, emotion_score = detect_emotion(user_input)
    distress_level = get_distress_level(emotion, emotion_score)

    # Store emotion memory
    if emotion not in ["neutral", None]:
        st.session_state.last_emotion = emotion
        st.session_state.emotion_history.append(emotion)
        st.session_state.emotion_history = st.session_state.emotion_history[-5:]

    # Generate response (LLM-like logic is inside this function)
    response = generate_response(
        emotion=emotion,
        distress_level=distress_level,
        turn_count=st.session_state.turn_count,
        user_text=user_input,
        last_emotion=st.session_state.last_emotion,
        emotion_history=st.session_state.emotion_history,
        last_bot_action=st.session_state.last_bot_action
    )

    # Detect bot intent for next turn
    if "try" in response.lower() or "would you like" in response.lower():
        st.session_state.last_bot_action = "offered_coping"
        st.session_state.last_suggested_activity = "grounding"
    else:
        st.session_state.last_bot_action = "general_support"

    # Log mood
    log_mood(emotion, distress_level)

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    st.caption(f"Detected emotion: {emotion.replace('_', ' ').title()}")

# --------------------
# Mood History
# --------------------
with st.expander("📈 View Mood History"):
    history = get_mood_history()
    st.write(history)
