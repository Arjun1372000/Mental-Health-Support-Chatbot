# Mental Health Support Chatbot

An accessible, non-judgmental AI chatbot designed to provide emotional support and early intervention for mental health concerns.

## Features

- **Emotion Detection**: Advanced NLP to identify user emotions and sentiment
- **Intelligent Responses**: Context-aware, empathetic responses based on emotional state
- **Risk Assessment**: Identifies elevated mental health risks with crisis resources
- **Analytics Dashboard**: Track emotional patterns and mental health trends
- **Crisis Support**: Integrated crisis helpline information for emergencies
- **Privacy-First**: No raw text stored, only anonymized features
- **User-Friendly Interface**: Clean, modern web interface

## Quick Start

### Prerequisites
- Python 3.8+
- 4GB RAM (for ML models)
- Internet connection (for first-time model download)

### Installation

1. **Clone and navigate to the project**
   ```bash
   cd Mental-Health-Support-Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:5000`

## Configuration

### Environment Variables
Create a `.env` file (copy from `.env.example`):
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./mental_health_chatbot.db
```

See [CONFIG.md](CONFIG.md) for detailed configuration options.

## Architecture

```
Mental-Health-Support-Chatbot/
├── app/
│   ├── main.py           # Flask server & API routes
│   └── chatbot.py        # Core chatbot conversation logic
├── ml/
│   └── emotion_analysis.py   # ML-based emotion & sentiment analysis
├── db/
│   ├── database.py       # Database configuration (SQLite/PostgreSQL)
│   └── models.py         # SQLAlchemy database models
├── ui/
│   ├── index.html        # Web interface
│   ├── style.css         # UI styling
│   └── script.js         # Frontend logic
├── analytics/
│   ├── insights.py       # Analytics functions
│   └── load_data.py      # Data loading utilities
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
└── CONFIG.md            # Detailed configuration guide
```

## Technology Stack

### Backend
- **Framework**: Flask
- **Database**: SQLAlchemy + SQLite (default) or PostgreSQL
- **NLP**: Transformers, HuggingFace
- **ML Models**:
  - Emotion Detection: `minuva/MiniLMv2-goemotions-v2`
  - Sentiment Analysis: `distilbert-base-uncased-finetuned-sst-2-english`

### Frontend
- **HTML5** / **CSS3** / **Vanilla JavaScript**
- **Real-time chat** via REST API
- **Responsive design** for mobile & desktop

## API Endpoints

### Chat
```
POST /api/chat
Body: { "message": "string" }
Response: { "response": "string", "emotion": "string", "sentiment": float, "risk_level": "string" }
```

### History
```
GET /api/history
Response: { "success": boolean, "history": array }
```

### Reset
```
POST /api/reset
Response: { "success": boolean, "message": "string" }
```

### Insights
```
GET /api/insights
Response: { "success": boolean, "basic": object, "risk": object, "recent": object }
```

## Usage

1. **Start a conversation** - Share your feelings with the chatbot
2. **Receive feedback** - Get empathetic responses based on your emotional state
3. **View insights** - Check emotional trends and patterns
4. **Access resources** - Get crisis support information when needed

## Crisis Support Resources

**If you're in crisis, please reach out immediately:**

- **National Suicide Prevention Lifeline**: **988** (Call or Text)
- **Crisis Text Line**: Text **HOME** to **741741**
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/
- **Emergency Services**: **911** (US) or your local emergency number

## Privacy & Security

- ✅ No raw text stored - only analyzed features
- ✅ Conversations are encrypted in database
- ✅ Session-based user isolation
- ✅ No third-party data sharing
- ✅ GDPR-compliant architecture

### Environment Variables for Production
```env
FLASK_ENV=production
SECRET_KEY=<random-strong-key>
DATABASE_URL=postgresql://user:password@host:5432/dbname
```
## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Performance Tips

- **First run**: Model download (~500MB) may take a few minutes
- **Inference time**: ~2-3 seconds per message
- **Memory usage**: ~2-3GB after models load
- **Database**: SQLite suitable for <10k conversations; use PostgreSQL for production

## Troubleshooting

### Models not downloading
```bash
# Check internet connection
# Clear cache if needed
rm -rf ~/.cache/huggingface
```

### Database errors
```bash
# Initialize fresh database
python db/database.py
```

### Memory issues
- Use CPU-only inference: `export CUDA_VISIBLE_DEVICES=-1`
- Reduce batch size or use smaller models

See [CONFIG.md](CONFIG.md) for detailed troubleshooting.

## Acknowledgments

- **HuggingFace** - For pre-trained NLP models
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Mental health professionals** - For guidance and best practices

## Support

For questions or issues:
1. Check the [CONFIG.md](CONFIG.md) documentation
2. Review [QUICKSTART.md](QUICKSTART.md)
3. Open an issue on GitHub
4. Contact the development team

---

**Remember**: This chatbot is a supportive tool, not a replacement for professional mental health care. If you're struggling, please reach out to a qualified mental health professional.

❤️ Take care of yourself and others.
