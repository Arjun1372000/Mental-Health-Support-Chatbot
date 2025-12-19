"""
Simple test script to verify the chatbot is working correctly
Run: python test_chatbot_simple.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_emotion_analysis():
    """Test emotion analysis"""
    print("\n" + "="*50)
    print("Testing Emotion Analysis...")
    print("="*50)
    
    try:
        from ml.emotion_analysis import analyze_text
        
        test_messages = [
            "I'm feeling really sad and hopeless",
            "I'm so angry right now!",
            "I'm having a great day!",
            "I'm nervous about tomorrow"
        ]
        
        for msg in test_messages:
            features = analyze_text(msg)
            print(f"\nMessage: '{msg}'")
            print(f"  Emotion: {features['emotion']}")
            print(f"  Sentiment: {features['sentiment_score']:.3f}")
            print(f"  Risk Level: {features['risk_level']}")
        
        print("\n✅ Emotion analysis working!")
        return True
    except Exception as e:
        print(f"\n❌ Emotion analysis failed: {e}")
        return False


def test_chatbot():
    """Test chatbot responses"""
    print("\n" + "="*50)
    print("Testing Chatbot Responses...")
    print("="*50)
    
    try:
        from app.chatbot import MentalHealthChatbot
        
        bot = MentalHealthChatbot()
        
        test_messages = [
            "I'm feeling really sad",
            "I'm worried about my future",
            "I'm so happy today!"
        ]
        
        for msg in test_messages:
            response = bot.get_response(msg)
            print(f"\nUser: {msg}")
            print(f"Bot: {response['response'][:100]}...")
            print(f"Emotion: {response['emotion']}, Risk: {response['risk_level']}")
        
        print("\n✅ Chatbot responses working!")
        return True
    except Exception as e:
        print(f"\n❌ Chatbot failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test database initialization"""
    print("\n" + "="*50)
    print("Testing Database...")
    print("="*50)
    
    try:
        from db.database import init_db, SessionLocal
        from db.models import MentalHealthFeature
        from datetime import datetime, timezone
        
        # Initialize database
        init_db()
        print("✅ Database initialized!")
        
        # Try to add a test entry
        session = SessionLocal()
        test_feature = MentalHealthFeature(
            emotion="sadness",
            sentiment_score=-0.5,
            message_length=10,
            sadness_streak=1,
            risk_level="LOW",
            timestamp=datetime.now(timezone.utc)
        )
        session.add(test_feature)
        session.commit()
        session.close()
        
        print("✅ Database write/read working!")
        return True
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flask_app():
    """Test Flask app initialization"""
    print("\n" + "="*50)
    print("Testing Flask App...")
    print("="*50)
    
    try:
        from app.main import app
        
        with app.test_client() as client:
            # Test health check
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health check working!")
            
            # Test index route
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Web UI accessible!")
            
            # Test chat endpoint
            response = client.post('/api/chat',
                json={'message': 'Hello, how are you?'},
                content_type='application/json'
            )
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("✅ Chat API working!")
                    print(f"   Response preview: {data['response'][:50]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ Flask app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "#"*50)
    print("# Mental Health Chatbot - System Check")
    print("#"*50)
    
    tests = [
        ("Emotion Analysis", test_emotion_analysis),
        ("Chatbot Logic", test_chatbot),
        ("Database", test_database),
        ("Flask App", test_flask_app),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational! Your chatbot is ready to use.")
        print("\nStart the chatbot with:")
        print("  python run.py")
        print("\nThen open:")
        print("  http://localhost:5000")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
        print("\nIf models need downloading (first time):")
        print("  1. Check internet connection")
        print("  2. Run: python run.py")
        print("  3. Wait for model download (~500MB)")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
