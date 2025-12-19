"""
Core chatbot logic - handles conversation flow and responses
"""
from ml.emotion_analysis import analyze_text, classify_risk
from datetime import datetime, timezone
import random

# Mental health support responses based on emotion/risk level
RESPONSES = {
    "sadness": {
        "LOW": [
            "I hear you. It sounds like you're feeling sad. Remember that it's okay to feel this way. Would you like to talk more about what's on your mind?",
            "Thank you for sharing. Sadness is a natural emotion. I'm here to listen and support you.",
            "I understand. Sometimes we all feel down. What do you think might help you feel better?"
        ],
        "MODERATE": [
            "I'm concerned about what you're sharing. It sounds like you're going through a difficult time. Have you considered talking to a trusted friend or family member?",
            "Thank you for being open with me. These feelings are important. Please remember that professional help is available if you need it.",
            "It seems like you might benefit from additional support. Would you like to talk to someone professional?"
        ],
        "ELEVATED": [
            "I'm really glad you reached out. What you're experiencing sounds serious, and you deserve proper support. Please consider reaching out to a mental health professional or a crisis helpline.",
            "Your wellbeing is important. If you're in crisis, please contact: National Suicide Prevention Lifeline 988 or Crisis Text Line (text HOME to 741741)",
            "I care about your safety. If you're having thoughts of self-harm, please reach out to emergency services or a crisis line immediately."
        ]
    },
    "fear": {
        "LOW": [
            "It sounds like something is making you anxious or worried. That's understandable. What specifically is concerning you?",
            "Fear is a natural response. Would it help to talk through what's worrying you?"
        ],
        "MODERATE": [
            "I sense you're experiencing significant anxiety. This is a good time to practice grounding techniques or talk to someone you trust.",
            "What you're feeling is valid. Have you tried any coping strategies that have helped before?"
        ],
        "ELEVATED": [
            "I'm concerned about the level of anxiety you're experiencing. Please reach out to a mental health professional for immediate support.",
            "If you're in a panic state, please try grounding techniques or call a crisis helpline: 988 or Crisis Text Line (text HOME to 741741)"
        ]
    },
    "anger": {
        "LOW": [
            "I hear that you're feeling frustrated or upset. It's okay to feel angry sometimes. What triggered these feelings?",
            "Thank you for expressing your anger. That takes courage. Let's talk about what's bothering you."
        ],
        "MODERATE": [
            "It sounds like you're quite upset. Taking a break, breathing deeply, or physical activity might help. Would that work for you?",
            "Your feelings are valid, but I want to make sure you're taking care of yourself. Have you had time to cool down?"
        ],
        "ELEVATED": [
            "I'm concerned about the intensity of your anger. Please take a step back and practice some calming techniques. If you're at risk of hurting yourself or others, please reach out to emergency services.",
            "Your safety matters. If you need immediate help, please call 911 or reach out to a crisis line: 988"
        ]
    },
    "joy": [
        "That's wonderful! I'm so glad you're feeling happy. Please share what's bringing you joy!",
        "That's beautiful! It sounds like you're in a good place. What's making you feel so positive?"
    ],
    "neutral": [
        "Thank you for sharing. I'm here to listen and support you in any way I can.",
        "I appreciate you talking with me. How are you really feeling today?"
    ]
}

class MentalHealthChatbot:
    def __init__(self, db_session=None):
        self.db_session = db_session
        self.conversation_history = []
        self.user_id = None
        
    def get_response(self, user_message: str) -> dict:
        """
        Process user message and return chatbot response
        """
        # Analyze the message
        features = analyze_text(user_message)
        
        # Store in conversation history
        self.conversation_history.append({
            "role": "user",
            "message": user_message,
            "features": features
        })
        
        # Save to database if session available
        if self.db_session:
            self._save_features(features)
        
        # Get appropriate response
        emotion = features["emotion"].lower()
        risk_level = features["risk_level"]
        
        # Get response from templates
        response_text = self._select_response(emotion, risk_level)
        
        # Store assistant response
        self.conversation_history.append({
            "role": "assistant",
            "message": response_text
        })
        
        return {
            "response": response_text,
            "emotion": features["emotion"],
            "sentiment_score": features["sentiment_score"],
            "risk_level": features["risk_level"],
            "timestamp": features["timestamp"]
        }
    
    def _select_response(self, emotion: str, risk_level: str) -> str:
        """
        Select appropriate response based on emotion and risk level
        """
        # Map emotions to response keys
        emotion_map = {
            "sadness": "sadness",
            "fear": "fear",
            "anger": "anger",
            "joy": "joy",
            "surprise": "neutral",
            "disgust": "anger",
            "neutral": "neutral"
        }
        
        response_key = emotion_map.get(emotion, "neutral")
        
        if isinstance(RESPONSES[response_key], dict):
            responses = RESPONSES[response_key].get(risk_level, RESPONSES[response_key].get("LOW", []))
        else:
            responses = RESPONSES[response_key]
        
        return random.choice(responses) if responses else "I'm here to listen and support you."
    
    def _save_features(self, features: dict):
        """
        Save message features to database
        """
        try:
            from db.models import MentalHealthFeature
            from datetime import datetime
            
            feature = MentalHealthFeature(
                timestamp=datetime.fromisoformat(features["timestamp"]),
                emotion=features["emotion"],
                sentiment_score=features["sentiment_score"],
                message_length=features["message_length"],
                risk_level=features["risk_level"],
                sadness_streak=1  # TODO: Track streaks properly
            )
            self.db_session.add(feature)
            self.db_session.commit()
        except Exception as e:
            print(f"Error saving features: {e}")
    
    def get_conversation_history(self) -> list:
        """
        Return conversation history
        """
        return self.conversation_history
    
    def reset_conversation(self):
        """
        Start a new conversation
        """
        self.conversation_history = []
