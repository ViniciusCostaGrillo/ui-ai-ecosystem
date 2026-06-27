import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import Masterpiece

logger = logging.getLogger(__name__)


class MasterpieceRegistry:
    """Manages database promotions, queries, and updates for Masterpieces."""

    def promote(
        self,
        db: Session,
        name: str,
        url: str,
        category: List[str],
        score: float = 95.0,
        weight: int = 10,
    ) -> Masterpiece:
        """Promotes a website to Masterpiece status, saving it in the database."""
        logger.info(f"MasterpieceRegistry: Promoting website '{name}' ({url}) to masterpiece status.")
        
        # Check if already exists
        existing = db.query(Masterpiece).filter(Masterpiece.url == url).first()
        if existing:
            logger.info(f"MasterpieceRegistry: Website already registered. Updating status and metadata.")
            existing.name = name
            existing.category = category
            existing.score = score
            existing.weight = weight
            existing.status = "active"
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing

        # Create new record
        mp = Masterpiece(
            name=name,
            url=url,
            category=category,
            score=score,
            weight=weight,
            status="active"
        )
        db.add(mp)
        db.commit()
        db.refresh(mp)
        return mp

    def demote(self, db: Session, url: str) -> bool:
        """Removes masterpiece status from a website."""
        logger.info(f"MasterpieceRegistry: Demoting website with URL '{url}' from masterpiece status.")
        mp = db.query(Masterpiece).filter(Masterpiece.url == url).first()
        if mp:
            db.delete(mp)
            db.commit()
            return True
        logger.warning(f"MasterpieceRegistry: URL '{url}' was not found in masterpieces table.")
        return False

    def get_all(self, db: Session) -> List[Masterpiece]:
        """Returns all masterpieces."""
        return db.query(Masterpiece).order_by(Masterpiece.score.desc()).all()

    def get_by_url(self, db: Session, url: str) -> Optional[Masterpiece]:
        """Returns a masterpiece by URL."""
        return db.query(Masterpiece).filter(Masterpiece.url == url).first()

    def update_status(self, db: Session, url: str, status: str) -> Optional[Masterpiece]:
        """Updates the status of a masterpiece (e.g. active, analyzing)."""
        mp = db.query(Masterpiece).filter(Masterpiece.url == url).first()
        if mp:
            mp.status = status
            mp.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(mp)
            return mp
        return None
