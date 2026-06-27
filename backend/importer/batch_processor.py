import json
import csv
import logging
import threading
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.importer.queue_manager import QueueManager
from backend.importer.website_importer import WebsiteImporter
from backend.importer.import_validator import ImportValidator
from backend.importer.url_parser import URLParser

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Processes lists of URLs uploaded via files and schedules them for import."""

    def __init__(self) -> None:
        self.queue = QueueManager()
        self.importer = WebsiteImporter()
        self.validator = ImportValidator()

    def process_txt(self, file_content: str) -> List[str]:
        """Extracts valid, unique URLs from plain text content (one URL per line)."""
        urls = []
        for line in file_content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            sanitized = URLParser.sanitize(line)
            if URLParser.is_valid(sanitized) and sanitized not in urls:
                urls.append(sanitized)
        return urls

    def process_csv(self, file_content: str) -> List[Dict[str, Any]]:
        """Extracts records from CSV formatted text (Name, URL, Category, Priority)."""
        records = []
        reader = csv.DictReader(file_content.splitlines())
        for row in reader:
            url = row.get("URL", row.get("url", "")).strip()
            if not url:
                continue
            sanitized = URLParser.sanitize(url)
            if URLParser.is_valid(sanitized):
                records.append({
                    "name": row.get("Name", row.get("name", "Unnamed")).strip(),
                    "url": sanitized,
                    "category": row.get("Category", row.get("category", "general")).strip(),
                    "priority": row.get("Priority", row.get("priority", "normal")).strip()
                })
        return records

    def process_json(self, file_content: str) -> List[Dict[str, Any]]:
        """Extracts records from JSON formatted text."""
        records = []
        try:
            data = json.loads(file_content)
            if isinstance(data, list):
                for item in data:
                    url = item.get("url", "").strip()
                    if not url:
                        continue
                    sanitized = URLParser.sanitize(url)
                    if URLParser.is_valid(sanitized):
                        records.append({
                            "name": item.get("name", "Unnamed").strip(),
                            "url": sanitized,
                            "category": item.get("category", "general").strip(),
                            "priority": item.get("priority", "normal").strip()
                        })
            elif isinstance(data, dict):
                # Single object conversion
                url = data.get("url", "").strip()
                if url:
                    sanitized = URLParser.sanitize(url)
                    if URLParser.is_valid(sanitized):
                        records.append({
                            "name": data.get("name", "Unnamed").strip(),
                            "url": sanitized,
                            "category": data.get("category", "general").strip(),
                            "priority": data.get("priority", "normal").strip()
                        })
        except Exception as e:
            logger.error(f"Error decoding JSON in batch processor: {e}")
        return records

    def enqueue_batch(
        self,
        records: List[Dict[str, Any]],
        options: Dict[str, Any]
    ) -> List[str]:
        """Enqueues batch records and triggers background import threads."""
        job_ids = []
        
        # Deduplicate URLs in this enqueue batch
        seen_urls = set()
        unique_records = []
        for record in records:
            if record["url"] not in seen_urls:
                seen_urls.add(record["url"])
                unique_records.append(record)

        for record in unique_records:
            url = record["url"]
            job = self.queue.create_job(url)
            job_id = job["id"]
            job_ids.append(job_id)
            
            # Start background thread for each crawling job
            thread = threading.Thread(
                target=self._run_job_async,
                args=(job_id, url, options, record.get("category", "general")),
                daemon=True
            )
            thread.start()
            
        return job_ids

    def _run_job_async(self, job_id: str, url: str, options: Dict[str, Any], category: str) -> None:
        """Helper that initializes session and executes the importer synchronously."""
        db: Session = SessionLocal()
        try:
            self.importer.import_website_sync(
                db=db,
                job_id=job_id,
                url=url,
                options=options,
                category=category
            )
        except Exception as e:
            logger.error(f"Async job execution failed for {url}: {e}")
            self.queue.update_job(job_id, {
                "status": "failed",
                "progress": 100,
                "stage": "Failed",
                "error_message": str(e),
                "log": f"Error: Job thread encountered a critical error: {e}"
            })
        finally:
            db.close()
