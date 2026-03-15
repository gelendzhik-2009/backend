"""
Initialization script for first-time setup.
Optional: Run this to verify the database connection.
"""

from app.database import engine, Base
from app.models import User

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("Tables created:")
    print("  - users")
