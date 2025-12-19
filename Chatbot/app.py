import streamlit as st
from emotion_model import detect_emotion
from distress_scoring import get_distress_level
from response import generate_response
from mood_tracker import log_mood, get_mood_history

# --------------------
# Page Config
# --------------------
st.set_page_config(
    page_title="Mānasika",
    # page_icon="💜",
    layout="centered"
)

st.markdown("""
<style>
/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* === OUTER APP BACKGROUND (DARK) === */
.stApp {
    background-color: #2E2B5F;
    color: #ECEBFF;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #2E2B5F;
    border-right: 1px solid #3D3A7A;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #ECEBFF;
}

/* === CHAT CONTAINER (LIGHT CARD) === */
.block-container {
    background-color: #ecebff6f;
    padding-top: 2rem;
    padding-bottom: 6rem;
    padding-left: 2rem;
    padding-right: 2rem;
    border-radius: 20px;
    max-width: 720px;
    margin-top: 2rem;
}

/* Title */
h1 {
    color: #6C63FF;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.3rem;
}

/* Caption */
.stCaption {
    text-align: center;
    color: #4B4B6A;
    margin-bottom: 1.8rem;
}

/* Chat spacing */
[data-testid="stChatMessage"] {
    margin-bottom: 0.6rem;
}

/* User bubble */
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background-color: #6C63FF;
    color: #FFFFFF;
    border-radius: 18px;
    padding: 12px 14px;
    margin-left: auto;
    max-width: 78%;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background-color: #dcd9ff3b;
    color: #1E1E2F;
    border-radius: 18px;
    padding: 12px 14px;
    margin-right: auto;
    max-width: 78%;
    border: 1px solid #C8C6F5;
}

/* Chat input */
textarea {
    background-color: #F1F0FF !important;
    color: #1E1E2F !important;
    border-radius: 16px !important;
    border: 1px solid #6C63FF !important;
    padding: 12px !important;
}

/* Send button */
button[kind="secondary"] {
    background-color: #6C63FF !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
}

/* Expander */
.st-expanderHeader {
    color: #6C63FF;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# Header
# --------------------
st.title("Mānasika")
st.caption("A calm space for emotional support • Not a medical professional")

# --------------------
# Sidebar
# --------------------
with st.sidebar:
    st.markdown("## 💜 Mānasika")
    st.write(
        "Mānasika is an AI-powered emotional support companion. "
        "It listens, reflects, and supports — without judgment."
    )
    st.divider()

    if st.button("🧹 Clear conversation"):
        st.session_state.messages = []
        st.session_state.turn_count = 0
        st.session_state.emotion_history = []
        st.session_state.last_emotion = None
        st.session_state.last_bot_action = None

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
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # --------------------
    # Short replies (context-aware)
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

    # Generate response
    with st.spinner("Thinking..."):
        response = generate_response(
            emotion=emotion,
            distress_level=distress_level,
            turn_count=st.session_state.turn_count,
            user_text=user_input,
            last_emotion=st.session_state.last_emotion,
            emotion_history=st.session_state.emotion_history,
            last_bot_action=st.session_state.last_bot_action
        )

    # Detect bot intent
    if "try" in response.lower() or "would you like" in response.lower():
        st.session_state.last_bot_action = "offered_coping"
    else:
        st.session_state.last_bot_action = "general_support"

    # Log mood
    log_mood(emotion, distress_level)

    # Show assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    with st.chat_message("assistant"):
        st.markdown(response)

    st.caption(f"Detected emotion: {emotion.replace('_', ' ').title()}")

# --------------------
# Mood History
# --------------------
with st.expander("📈 View Mood History"):
    history = get_mood_history()
    st.write(history)
