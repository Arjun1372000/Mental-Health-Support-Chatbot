# Configuration Guide

## Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///./mental_health_chatbot.db
# For PostgreSQL: postgresql://user:password@localhost:5432/mental_health_db

# ML Models
TRANSFORMERS_CACHE=/path/to/cache  # Optional: custom model cache location
HF_TOKEN=your-huggingface-token  # Only needed for gated models
```

## Flask Configuration

The application uses the following Flask configuration:

- **Debug Mode**: Enabled in development
- **CORS**: Enabled for all origins
- **Session Management**: Secure session handling with secret key
- **Port**: 5000 (configurable)

## Database Configuration

### SQLite (Default)
- File-based, no setup required
- Perfect for development and small deployments
- Location: `./mental_health_chatbot.db`

### PostgreSQL
- For production use
- Set `DATABASE_URL` environment variable

Example:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mental_health_db"
```

## ML Model Configuration

The chatbot uses:

1. **Emotion Detection**: `minuva/MiniLMv2-goemotions-v2`
   - Detects 27 emotions
   - Fast inference, lightweight

2. **Sentiment Analysis**: `distilbert-base-uncased-finetuned-sst-2-english`
   - Binary sentiment classification
   - Pre-trained on SST-2 dataset

Models are automatically downloaded on first run and cached locally.

## Security Considerations

1. **Never commit `.env` file to version control**
2. **Use strong `SECRET_KEY` in production**
3. **Enable HTTPS in production**
4. **Implement rate limiting for API endpoints**
5. **Add authentication for sensitive endpoints**
6. **Regularly update dependencies**

## Troubleshooting

### Models not downloading
- Check internet connection
- Set `HF_DATASETS_OFFLINE=0` if using Hugging Face
- Manually download if behind proxy

### Database errors
- Ensure write permissions in project directory
- Check `DATABASE_URL` format
- Run `python db/database.py` to initialize

### Memory issues
- Reduce model size (use distilled models)
- Implement model quantization
- Use CPU-only inference

Add to `run.py` for development debugging.
