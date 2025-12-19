"""
Database initialization script with SQLite support
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Use SQLite for development/demo (no PostgreSQL needed)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./mental_health_chatbot.db"
)

# SQLite-specific settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize database - create all tables
    """
    from db.models import Base
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on import
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
