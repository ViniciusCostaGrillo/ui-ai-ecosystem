import logging
from typing import Tuple, Optional
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
