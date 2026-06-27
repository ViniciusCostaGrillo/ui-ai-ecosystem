import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.masterpieces.masterpiece_registry import MasterpieceRegistry
from backend.masterpieces.masterpiece_builder import MasterpieceBuilder
from backend.masterpieces.masterpiece_embeddings import MasterpieceEmbeddingsManager
from backend.masterpieces.masterpiece_validator import MasterpieceValidator

logger = logging.getLogger(__name__)


class MasterpieceAgent:
    """Orchestrates promotions, scrapes content, parses design rules, calculates scores,

    and indexes metadata inside database and ChromaDB.
    """

    def __init__(self) -> None:
        self.registry = MasterpieceRegistry()
        self.builder = MasterpieceBuilder()
        self.embeddings = MasterpieceEmbeddingsManager()
        self.validator = MasterpieceValidator()

    def promote_website(
        self,
        db: Session,
        name: str,
        url: str,
        category: List[str],
        crawler_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Runs the entire masterpiece promotion pipeline."""
        logger.info(f"MasterpieceAgent: Starting promotion flow for url={url}...")
        
        # 1. Update status to analyzing
        self.registry.promote(db, name, url, category, score=85.0)
        self.registry.update_status(db, url, "analyzing")

        # 2. Extract visual characteristics (from crawler data or fallback default mock settings)
        if not crawler_data:
            crawler_data = {}

        colors = crawler_data.get("colors", ["#0A0A0A", "#D4AF37", "#FFFFFF"])
        typography = crawler_data.get("typography", ["Playfair Display", "Geist Sans"])
        motion = crawler_data.get("motion", {
            "animations": ["Gsap slow reveal", "Lenis smooth scroll"]
        })
        
        perf = crawler_data.get("performance", 88.0)
        a11y = crawler_data.get("accessibility", 90.0)
        visual = crawler_data.get("visual_quality", 98.0)
        resp = crawler_data.get("responsiveness", 95.0)

        # 3. Calculate designer scores
        final_score = self.validator.calculate_score(
            performance=perf,
            accessibility=a11y,
            visual_quality=visual,
            responsiveness=resp
        )
        logger.info(f"MasterpieceAgent: Calculated aesthetic quality score = {final_score}")

        details = {
            "colors": colors,
            "typography": typography,
            "motion": motion,
            "performance": perf,
            "accessibility": a11y,
            "visual_quality": visual,
            "responsiveness": resp
        }

        # 4. Generate structured configs and YAML files
        relative_folder = self.builder.build(name, url, category, details)

        # 5. Index in ChromaDB
        doc_content = f"""Masterpiece Website: {name}
Reference URL: {url}
Category Tags: {', '.join(category)}
Color Palette: {', '.join(colors)}
Typography pairing: {', '.join(typography)}
Style statement: High-end luxury visual design system and clean grids.
"""
        
        # Index visual system
        self.embeddings.index_masterpiece_item(
            collection_name="Masterpieces",
            item_id=f"masterpiece:{name.lower()}",
            document=doc_content,
            metadata={
                "name": name,
                "url": url,
                "score": final_score,
                "categories": ",".join(category),
                "weight": 10
            }
        )

        # Index components config
        comp_content = f"Component Library reference based on {name} style: hero, cards, navbar, footers templates."
        self.embeddings.index_masterpiece_item(
            collection_name="MasterpieceComponents",
            item_id=f"masterpiece:components:{name.lower()}",
            document=comp_content,
            metadata={
                "name": name,
                "url": url,
                "weight": 10
            }
        )

        # 6. Update database record with final score and active status
        self.registry.promote(db, name, url, category, score=final_score, weight=10)
        self.registry.update_status(db, url, "active")

        return {
            "status": "success",
            "name": name,
            "url": url,
            "score": final_score,
            "folder": relative_folder,
        }
