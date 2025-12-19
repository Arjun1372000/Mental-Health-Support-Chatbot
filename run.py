#!/usr/bin/env python3
"""
Main entry point for the Mental Health Support Chatbot
Run this file to start the application
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize database
from db.database import init_db

# Initialize database tables
print("Initializing database...")
init_db()
print("Database initialized!")

# Import and run Flask app
from app.main import app

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧠 Mental Health Support Chatbot")
    print("="*50)
    print("\n✨ Server starting on http://localhost:5000")
    print("Press CTRL+C to stop the server\n")
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader in development
        )
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped.")
        sys.exit(0)
