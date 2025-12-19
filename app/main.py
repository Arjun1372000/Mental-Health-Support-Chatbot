"""
Flask web application for Mental Health Support Chatbot
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from app.chatbot import MentalHealthChatbot
from db.database import SessionLocal
import os
import secrets

app = Flask(__name__, template_folder='../ui', static_folder='../ui/static')
CORS(app)

# Security
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Global chatbot instance (in production, use per-session)
chatbots = {}

def get_chatbot_for_session():
    """
    Get or create chatbot for this session
    """
    session_id = session.get('session_id')
    if not session_id:
        session_id = secrets.token_hex(16)
        session['session_id'] = session_id
    
    if session_id not in chatbots:
        try:
            db_session = SessionLocal()
            chatbots[session_id] = MentalHealthChatbot(db_session)
        except:
            # Fallback without database
            chatbots[session_id] = MentalHealthChatbot()
    
    return chatbots[session_id]

@app.route('/')
def index():
    """
    Serve the main chatbot UI
    """
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    """
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        chatbot = get_chatbot_for_session()
        response = chatbot.get_response(user_message)
        
        return jsonify({
            "success": True,
            "response": response["response"],
            "emotion": response["emotion"],
            "sentiment": response["sentiment_score"],
            "risk_level": response["risk_level"],
            "timestamp": response["timestamp"]
        })
    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your message. Please try again."
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get conversation history
    """
    try:
        chatbot = get_chatbot_for_session()
        history = chatbot.get_conversation_history()
        
        # Format for display (no features for security)
        formatted_history = [
            {
                "role": msg.get("role"),
                "message": msg.get("message")
            }
            for msg in history
        ]
        
        return jsonify({
            "success": True,
            "history": formatted_history
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """
    Reset conversation
    """
    try:
        chatbot = get_chatbot_for_session()
        chatbot.reset_conversation()
        return jsonify({"success": True, "message": "Conversation reset"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """
    Get analytics insights
    """
    try:
        from analytics.insights import basic_insights, risk_insights, recent_trend
        from analytics.load_data import load_features_df
        
        df = load_features_df()
        
        if df.empty:
            return jsonify({
                "success": True,
                "basic": {"total_days": 0, "avg_sentiment": 0, "most_common_emotion": "N/A", "max_sadness_streak": 0},
                "risk": {"risk_distribution": {}, "elevated_days": 0},
                "recent": {"avg_recent_sentiment": 0, "dominant_emotion_last_7_days": "N/A", "avg_sadness_streak_last_7_days": 0}
            })
        
        return jsonify({
            "success": True,
            "basic": basic_insights(df),
            "risk": risk_insights(df),
            "recent": recent_trend(df)
        })
    except Exception as e:
        print(f"Error getting insights: {e}")
        return jsonify({
            "success": False,
            "error": "Could not load insights"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
