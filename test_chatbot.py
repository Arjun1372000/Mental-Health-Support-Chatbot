"""
Unit tests for the chatbot
"""
import pytest
from app.chatbot import MentalHealthChatbot, classify_risk
from ml.emotion_analysis import analyze_text


class TestEmotionAnalysis:
    """Test emotion analysis functions"""
    
    def test_analyze_text_returns_features(self):
        """Test that analyze_text returns required features"""
        text = "I feel so sad and hopeless"
        features = analyze_text(text)
        
        assert isinstance(features, dict)
        assert "emotion" in features
        assert "sentiment_score" in features
        assert "risk_level" in features
        assert "message_length" in features
        assert "timestamp" in features


class TestRiskClassification:
    """Test risk classification"""
    
    def test_elevated_risk(self):
        """Test elevated risk detection"""
        risk = classify_risk(-0.8, "sadness")
        assert risk == "ELEVATED"
    
    def test_moderate_risk(self):
        """Test moderate risk detection"""
        risk = classify_risk(-0.4, "sadness")
        assert risk == "MODERATE"
    
    def test_low_risk(self):
        """Test low risk detection"""
        risk = classify_risk(0.5, "joy")
        assert risk == "LOW"


class TestChatbot:
    """Test chatbot core functionality"""
    
    def test_chatbot_initialization(self):
        """Test chatbot can be initialized"""
        bot = MentalHealthChatbot()
        assert bot is not None
        assert len(bot.conversation_history) == 0
    
    def test_get_response_returns_dict(self):
        """Test that get_response returns valid response"""
        bot = MentalHealthChatbot()
        response = bot.get_response("I'm feeling sad")
        
        assert isinstance(response, dict)
        assert "response" in response
        assert "emotion" in response
        assert "sentiment_score" in response
        assert "risk_level" in response
    
    def test_conversation_history(self):
        """Test conversation history tracking"""
        bot = MentalHealthChatbot()
        bot.get_response("Hello")
        
        history = bot.get_conversation_history()
        assert len(history) >= 2  # User message + bot response
    
    def test_reset_conversation(self):
        """Test conversation reset"""
        bot = MentalHealthChatbot()
        bot.get_response("Hello")
        assert len(bot.conversation_history) > 0
        
        bot.reset_conversation()
        assert len(bot.conversation_history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
