import logging
import os

# Read log level from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").strip().upper()


class DatabaseLoggingHandler(logging.Handler):
    """Custom logging Handler to write log entries directly to the database.

    Works thread-safely by utilizing sessionmaker factories.
    """

    def __init__(self, session_maker) -> None:
        super().__init__()
        self.session_maker = session_maker

    def emit(self, record: logging.LogRecord) -> None:
        db = None
        try:
            log_message = self.format(record)
            
            # Extract execution_id or job_id if attached
            execution_id = getattr(record, "execution_id", None)
            job_id = getattr(record, "job_id", None)
            
            # Create session and write
            db = self.session_maker()
            from backend.database.models import Log
            db_log = Log(
                execution_id=execution_id,
                job_id=job_id,
                level=record.levelname,
                message=log_message
            )
            db.add(db_log)
            db.commit()
        except Exception:
            # Prevent logging errors from crashing the main application flow
            pass
        finally:
            if db is not None:
                db.close()


def setup_logger(name: str) -> logging.Logger:
    """Configures a standardized structured logger for all API endpoints and services."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Avoid duplicate handlers if already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add database logging handler if SessionLocal is available
        try:
            from backend.database.session import SessionLocal
            db_handler = DatabaseLoggingHandler(SessionLocal)
            db_handler.setFormatter(formatter)
            db_handler.setLevel(logging.INFO)
            logger.addHandler(db_handler)
        except Exception:
            pass
        
    return logger
