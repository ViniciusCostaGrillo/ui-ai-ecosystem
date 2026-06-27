import sys
from backend.database.session import SessionLocal
from backend.masterpieces.masterpiece_agent import MasterpieceAgent
from backend.schemas.masterpieces import MasterpieceInfo
from backend.database.models import Masterpiece


def run_tests():
    print("Running Masterpiece Engine validation suite...")
    success = True
    db = SessionLocal()

    agent = MasterpieceAgent()

    # 1. Test Heuristic Calculation
    try:
        score = agent.validator.calculate_score(
            performance=80.0,
            accessibility=90.0,
            visual_quality=98.0,
            responsiveness=95.0
        )
        assert round(score, 1) == 92.2
        print("PASS - Validator score calculation")
    except Exception as e:
        print(f"FAIL - Validator score calculation: {e}")
        success = False

    # 2. Test Code Validator
    try:
        res = agent.validator.validate_code("import React from 'react';\nexport default function Test() { return <div className='p-4 md:p-8'>Test</div>; }")
        assert res["is_valid"] is True
        assert len(res["warnings"]) == 0
        print("PASS - Validator code validation (valid)")
    except Exception as e:
        print(f"FAIL - Validator code validation (valid): {e}")
        success = False

    # 3. Test Registry & Promotion Flow
    try:
        # Clean existing test masterpiece if any
        test_url = "https://test-masterpiece-url.com"
        existing = db.query(Masterpiece).filter(Masterpiece.url == test_url).first()
        if existing:
            db.delete(existing)
            db.commit()

        result = agent.promote_website(
            db=db,
            name="Test Boutique",
            url=test_url,
            category=["luxury", "editorial"],
            crawler_data={
                "colors": ["#000000", "#ffffff"],
                "typography": ["Lora", "Inter"],
                "performance": 90.0,
                "accessibility": 85.0,
                "visual_quality": 95.0,
                "responsiveness": 92.0
            }
        )

        assert result["status"] == "success"
        assert result["name"] == "Test Boutique"
        assert result["score"] == 91.4 # (95*0.4)+(90*0.2)+(85*0.2)+(92*0.2) = 38+18+17+18.4 = 91.4
        
        # Verify in database
        db_mp = db.query(Masterpiece).filter(Masterpiece.url == test_url).first()
        assert db_mp is not None
        assert db_mp.score == 91.4
        assert db_mp.status == "active"
        
        # Clean up
        db.delete(db_mp)
        db.commit()

        print("PASS - Promotion Flow & Registry")
    except Exception as e:
        print(f"FAIL - Promotion Flow & Registry: {e}")
        success = False

    db.close()
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
