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

## Performance Tuning

### Reduce Memory Usage
```python
# Use CPU instead of GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

### Speed Up Inference
```python
# Use quantized models for faster inference
# Requires: pip install optimum onnxruntime
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

Build and run:
```bash
docker build -t mental-health-chatbot .
docker run -p 5000:5000 mental-health-chatbot
```

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

## Logging

To enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Add to `run.py` for development debugging.
