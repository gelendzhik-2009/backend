"""Initialization script — creates all tables from models"""

from app.database import engine, Base
import app.models  # noqa: F401 — registers all model metadata
import app.models.associations  # noqa: F401

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")
