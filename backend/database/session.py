import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Get PostgreSQL connection string from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/ui_ai_db"
)

# Create engine and session factories
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()

# FastAPI Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
