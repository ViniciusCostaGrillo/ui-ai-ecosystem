import sys
from backend.database.session import engine, Base
# Import models to register them with Base.metadata (noqa: F401)
from backend.database.models import (  # noqa: F401
    User,
    Project,
    Execution,
    Job,
    Log,
    Dataset,
    CrawlerHistory,
    TrainingHistory,
)

def init_database():
    print("Connecting to database and creating tables...")
    try:
        # Create all tables defined in models.py
        Base.metadata.create_all(bind=engine)
        print("Success: Database tables created successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
