import sys
import time
from unittest.mock import MagicMock
import redis
# Mock redis to instantly trigger local fallback
redis.Redis = MagicMock(side_effect=Exception("Mock Redis Connection Failure"))

from backend.database.session import SessionLocal
from backend.importer.url_parser import URLParser
from backend.importer.import_validator import ImportValidator
from backend.importer.queue_manager import QueueManager
from backend.database.models import Dataset

# Mock WebsiteImporter before importing BatchProcessor
sys.modules['backend.importer.website_importer'] = MagicMock()
from backend.importer.batch_processor import BatchProcessor


def run_tests():
    print("Running Importer Engine validation suite...")
    success = True
    db = SessionLocal()

    processor = BatchProcessor()

    # 1. URL Parser
    try:
        assert URLParser.sanitize("google.com ") == "https://google.com"
        assert URLParser.sanitize("http://google.com") == "http://google.com"
        assert URLParser.get_domain("https://www.google.com/search") == "google.com"
        assert URLParser.is_valid("https://linear.app") is True
        assert URLParser.is_valid("invalid-url") is False
        print("PASS - URLParser utility")
    except Exception as e:
        print(f"FAIL - URLParser utility: {e}")
        success = False

    # 2. Ingest CSV & JSON parsing
    try:
        csv_data = "Name,URL,Category,Priority\nLinear,https://linear.app,saas,masterpiece\nStripe,https://stripe.com,fintech,normal"
        records = processor.process_csv(csv_data)
        assert len(records) == 2
        assert records[0]["name"] == "Linear"
        assert records[0]["url"] == "https://linear.app"
        assert records[0]["category"] == "saas"
        
        json_data = '[{"url": "https://vercel.com", "category": "hosting"}]'
        json_records = processor.process_json(json_data)
        assert len(json_records) == 1
        assert json_records[0]["url"] == "https://vercel.com"
        print("PASS - Batch file format parsers")
    except Exception as e:
        print(f"FAIL - Batch file format parsers: {e}")
        success = False

    # 3. Queue Manager Job Creation
    try:
        queue = QueueManager()
        queue.clear()
        
        job = queue.create_job("https://stripe.com")
        job_id = job["id"]
        assert job["url"] == "https://stripe.com"
        assert job["status"] == "queued"
        
        updated = queue.update_job(job_id, {"status": "running", "log": "Connecting..."})
        assert updated["status"] == "running"
        assert len(updated["logs"]) > 1
        
        jobs = queue.get_all_jobs()
        assert len(jobs) == 1
        print("PASS - QueueManager states")
    except Exception as e:
        print(f"FAIL - QueueManager states: {e}")
        success = False

    db.close()
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
