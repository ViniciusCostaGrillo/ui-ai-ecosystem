import logging
from typing import Tuple, Optional, List
from sqlalchemy.orm import Session
from backend.database.models import Dataset
from backend.importer.url_parser import URLParser

logger = logging.getLogger(__name__)


class ImportValidator:
    """Validates URLs for batch ingestion."""

    def __init__(self, domain_blacklist: Optional[list] = None) -> None:
        self.blacklist = domain_blacklist or ["localhost", "127.0.0.1", "0.0.0.0"]

    def validate(self, db: Session, url: str) -> Tuple[bool, Optional[str]]:
        """Checks if URL is valid, not duplicate, and not blacklisted."""
        sanitized_url = URLParser.sanitize(url)
        
        if not URLParser.is_valid(sanitized_url):
            return False, "Invalid URL format"
            
        domain = URLParser.get_domain(sanitized_url)
        if domain in self.blacklist:
            return False, f"Domain '{domain}' is blacklisted"
            
        # Check if URL was already crawled recently (within the datasets table)
        existing = db.query(Dataset).filter(Dataset.url == sanitized_url).first()
        if existing:
            return True, "duplicate"  # Valid URL but already processed
            
        return True, None

    def validate_bulk(self, db: Session, urls: List[str]) -> dict:
        """Validates a list of URLs in bulk, using optimized database queries."""
        results = {}
        sanitized_urls = []
        url_map = {}  # sanitized -> original
        
        # 1. Validate URL formats and check blacklist in-memory
        for url in urls:
            sanitized = URLParser.sanitize(url)
            if not URLParser.is_valid(sanitized):
                results[url] = (False, "Invalid URL format")
                continue
                
            domain = URLParser.get_domain(sanitized)
            if domain in self.blacklist:
                results[url] = (False, f"Domain '{domain}' is blacklisted")
                continue
                
            sanitized_urls.append(sanitized)
            url_map[sanitized] = url
            
        # 2. Bulk duplicate check in database (chunked to prevent SQLite parameter limits)
        existing_sanitized = set()
        chunk_size = 500
        for i in range(0, len(sanitized_urls), chunk_size):
            chunk = sanitized_urls[i:i + chunk_size]
            db_results = db.query(Dataset.url).filter(Dataset.url.in_(chunk)).all()
            existing_sanitized.update(r[0] for r in db_results)
            
        # 3. Populate final validation outcomes
        for sanitized in sanitized_urls:
            orig_url = url_map[sanitized]
            if sanitized in existing_sanitized:
                results[orig_url] = (True, "duplicate")
            else:
                results[orig_url] = (True, None)
                
        return results
