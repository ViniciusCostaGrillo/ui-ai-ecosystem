import re
from typing import Optional
from urllib.parse import urlparse


class URLParser:
    """Utility class that sanitizes and parses URLs."""

    @staticmethod
    def sanitize(url: str) -> str:
        """Trims whitespace and ensures URL contains a schema (http/https)."""
        url = url.strip()
        if not url:
            return ""
        
        # Check if URL starts with protocol, if not default to https
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = "https://" + url
            
        return url

    @staticmethod
    def get_domain(url: str) -> str:
        """Extracts clean domain name from URL."""
        parsed = urlparse(url)
        netloc = parsed.netloc or parsed.path
        # Clean port numbers if present
        domain = netloc.split(":")[0]
        # Remove www
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    @classmethod
    def is_valid(cls, url: str) -> bool:
        """Validates if the URL has a correct structure."""
        url = cls.sanitize(url)
        if not url:
            return False
            
        parsed = urlparse(url)
        # Check domain format
        domain = cls.get_domain(url)
        if not domain or "." not in domain or len(domain.split(".")[-1]) < 2:
            return False
            
        return parsed.scheme in ["http", "https"]
