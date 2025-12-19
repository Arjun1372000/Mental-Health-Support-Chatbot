# Quick Start Guide for Mental Health Support Chatbot

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

The chatbot will start on `http://localhost:5000`

## Features

✨ **Emotion Detection**: Uses HuggingFace models to analyze user emotions and sentiment
💬 **Intelligent Responses**: Provides contextual, empathetic responses based on emotional state
⚠️ **Risk Assessment**: Identifies elevated mental health risks and provides crisis resources
📊 **Analytics**: Tracks emotional patterns and provides insights over time
🎯 **Non-judgmental Support**: Safe, supportive environment for users to express themselves

## System Requirements

- Python 3.8+
- 4GB RAM (for ML models)
- Internet connection (for first model download)

## Database

By default, the application uses SQLite (no setup needed). To use PostgreSQL:

```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/mental_health_db
```

## Crisis Resources

If you or someone you know is in crisis:

- **National Suicide Prevention Lifeline**: 988 (Call or Text)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

## Architecture

```
├── app/
│   ├── main.py          # Flask application & routes
│   └── chatbot.py       # Core chatbot logic
├── ml/
│   └── emotion_analysis.py  # Emotion & sentiment analysis
├── db/
│   ├── database.py      # Database configuration
│   └── models.py        # SQLAlchemy models
├── ui/
│   ├── index.html       # Main UI
│   ├── style.css        # Styling
│   └── script.js        # Frontend JavaScript
└── analytics/
    ├── insights.py      # Analytics functions
    └── load_data.py     # Data loading utilities
```

## Development

For development with auto-reload:
```bash
python run.py
```

View the application at: http://localhost:5000

## Notes

- First run will download ML models (~500MB)
- Conversations are stored securely in the database
- Raw text is not stored, only analyzed features
- No data is sent to external services
