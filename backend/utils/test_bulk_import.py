import sys
import time
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.database.session import Base, SessionLocal, engine
from backend.database.models import Dataset
from backend.importer.import_validator import ImportValidator


def run_bulk_tests():
    print("------------- Bulk Import Verification Tests -------------")
    db = SessionLocal()
    
    # 1. Clean and setup test DB tables
    Base.metadata.create_all(bind=engine)
    
    # Ensure database is clean of our test duplicates
    db.query(Dataset).filter(Dataset.url.like("https://test-bulk-%")).delete(synchronize_session=False)
    db.commit()
    
    # 2. Insert dummy records to act as duplicates
    existing_url_1 = "https://test-bulk-exists-1.com"
    existing_url_2 = "https://test-bulk-exists-2.com"
    
    dataset_1 = Dataset(
        project_id="mock-project-id-1",
        url=existing_url_1,
        screenshot_path="screenshot.png",
        html_path="page.html",
        css_path="style.css",
        markdown_path="content.md",
        metadata_json={}
    )
    dataset_2 = Dataset(
        project_id="mock-project-id-1",
        url=existing_url_2,
        screenshot_path="screenshot.png",
        html_path="page.html",
        css_path="style.css",
        markdown_path="content.md",
        metadata_json={}
    )
    db.add(dataset_1)
    db.add(dataset_2)
    db.commit()
    
    # 3. Compile validation test set (including new, duplicate, blacklisted, and invalid URLs)
    urls = [
        "https://test-bulk-exists-1.com",  # Duplicate
        "https://test-bulk-exists-2.com",  # Duplicate
        "https://test-bulk-new-1.com",     # Valid New
        "https://test-bulk-new-2.com",     # Valid New
        "invalid-url-format",              # Invalid
        "https://blacklisted.com/path",    # Blacklisted
    ]
    
    # Add an additional 1000 simulated URLs to verify scalability/speed
    for i in range(1000):
        urls.append(f"https://test-bulk-scale-{i}.com")
        
    print(f"Submitting {len(urls)} URLs to validate_bulk...")
    
    start_time = time.time()
    validator = ImportValidator(domain_blacklist=["blacklisted.com"])
    results = validator.validate_bulk(db, urls)
    duration = time.time() - start_time
    
    print(f"Validation completed in {duration:.4f} seconds.")
    
    # Assertions
    # 1. Duplicates
    assert results[existing_url_1] == (True, "duplicate"), f"Failed: {existing_url_1}"
    assert results[existing_url_2] == (True, "duplicate"), f"Failed: {existing_url_2}"
    
    # 2. New URLs
    assert results["https://test-bulk-new-1.com"] == (True, None)
    assert results["https://test-bulk-new-2.com"] == (True, None)
    
    # 3. Invalid
    assert results["invalid-url-format"] == (False, "Invalid URL format")
    
    # 4. Blacklisted
    assert results["https://blacklisted.com/path"] == (False, "Domain 'blacklisted.com' is blacklisted")
    
    # 5. Scalability check
    assert len(results) == len(urls)
    assert results["https://test-bulk-scale-999.com"] == (True, None)
    
    print("[PASS] Bulk validation tests passed successfully!")
    
    # Clean up test database entries
    db.query(Dataset).filter(Dataset.url.like("https://test-bulk-%")).delete(synchronize_session=False)
    db.commit()
    db.close()


if __name__ == "__main__":
    run_bulk_tests()
