import os
import time
import uuid
import logging
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class QueueManager:
    """Manages crawl import jobs in an active queue, supporting fallbacks."""

    _jobs: Dict[str, Dict[str, Any]] = {}
    _lock = threading.RLock()

    def __init__(self) -> None:
        from backend.database.redis_client import RedisClientManager, MockRedis
        self.use_redis = False
        try:
            manager = RedisClientManager()
            self.redis_client = manager.get_client()
            if not isinstance(self.redis_client, MockRedis):
                self.use_redis = True
                logger.info("QueueManager: Connected to Redis successfully.")
            else:
                logger.info("QueueManager: Redis not available. Using local MockRedis.")
        except Exception as e:
            logger.warning(f"QueueManager: Redis check failed: {e}. Using local thread-based job tracking.")

    def create_job(self, url: str) -> Dict[str, Any]:
        """Creates a new queued job."""
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        job = {
            "id": job_id,
            "url": url,
            "status": "queued",
            "stage": "Playwright",
            "progress": 0,
            "elapsed": "00:00",
            "remaining": "00:00",
            "logs": [f"[{datetime.now().strftime('%H:%M')}] Job created, queued in line."],
            "error_message": None,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "finished_at": None,
            "start_time": time.time()
        }
        
        with self._lock:
            self._jobs[job_id] = job
            
        return job

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Returns details of a job."""
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                # Update elapsed time if running
                if job["status"] == "running":
                    elapsed_sec = int(time.time() - job.get("run_start_time", job["start_time"]))
                    job["elapsed"] = f"{elapsed_sec // 60:02d}:{elapsed_sec % 60:02d}"
                    # Calculate estimated remaining time (mock baseline 15s total)
                    remaining_sec = max(0, 15 - elapsed_sec)
                    job["remaining"] = f"{remaining_sec // 60:02d}:{remaining_sec % 60:02d}"
                return job.copy()
        return None

    def update_job(self, job_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Updates attributes of an existing job."""
        with self._lock:
            if job_id in self._jobs:
                job = self._jobs[job_id]
                for key, val in updates.items():
                    if key == "log":
                        # Append log line
                        job["logs"].append(f"[{datetime.now().strftime('%H:%M')}] {val}")
                    else:
                        job[key] = val
                return job.copy()
        return None

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Returns all jobs currently tracked in the system."""
        with self._lock:
            # Trigger updates for elapsed times
            for job_id in self._jobs.keys():
                self.get_job(job_id)
            return list(self._jobs.values())

    def clear(self) -> None:
        """Clears the job registry."""
        with self._lock:
            self._jobs.clear()
