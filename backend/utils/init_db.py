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
    Masterpiece,
)

def init_database():
    print("Connecting to database and creating tables...")
    try:
        # Create all tables defined in models.py
        Base.metadata.create_all(bind=engine)
        print("Success: Database tables created successfully!")
        
        # Seed default masterpieces
        from backend.database.session import SessionLocal
        from backend.database.models import Masterpiece
        db = SessionLocal()
        defaults = [
            {"name": "Elara Footwear", "url": "https://www.aura.build/templates/elara-footwear", "category": ["fashion", "luxury", "ecommerce"], "score": 98.4},
            {"name": "NoirFrame Fashion", "url": "https://noirframefashion.aura.build", "category": ["fashion", "editorial", "luxury"], "score": 97.2},
            {"name": "Linear", "url": "https://linear.app", "category": ["saas", "minimal", "startup"], "score": 96.5},
            {"name": "Stripe", "url": "https://stripe.com", "category": ["fintech", "saas", "dashboard"], "score": 98.0},
            {"name": "Vercel", "url": "https://vercel.com", "category": ["saas", "developer", "minimal"], "score": 95.8},
            {"name": "Refokus", "url": "https://refokus.com", "category": ["agency", "animation", "motion"], "score": 97.5}
        ]
        for item in defaults:
            existing = db.query(Masterpiece).filter(Masterpiece.url == item["url"]).first()
            if not existing:
                mp = Masterpiece(
                    name=item["name"],
                    url=item["url"],
                    category=item["category"],
                    score=item["score"],
                    weight=10,
                    status="active"
                )
                db.add(mp)
        db.commit()
        db.close()
        print("Success: Default masterpieces seeded successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
