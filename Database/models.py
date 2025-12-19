from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MentalHealthFeature(Base):
    __tablename__ = "mental_health_features"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    emotion = Column(String, nullable=False)
    emotion_score = Column(Float, default=0.0)
    sentiment_score = Column(Float, nullable=False)
    message_length = Column(Integer, default=0)
    sadness_streak = Column(Integer, default=0)
    risk_level = Column(String, default="LOW")

    def __repr__(self):
        return f"<MentalHealthFeature(id={self.id}, emotion={self.emotion}, risk_level={self.risk_level})>"
