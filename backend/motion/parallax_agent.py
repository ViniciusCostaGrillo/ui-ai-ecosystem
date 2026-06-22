import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ParallaxAgent:
    """Agent that synthesizes scroll-bound parallax motion sequences."""

    def generate_parallax(self, element_id: str, speed: float) -> Dict[str, Any]:
        logger.info(f"ParallaxAgent: generating parallax sequence for element={element_id}, speed={speed}")
        code = (
            f"gsap.to('#{element_id}', {{\n"
            f"  yPercent: {-speed * 20},\n"
            f"  ease: 'none',\n"
            f"  scrollTrigger: {{\n"
            f"    trigger: '#{element_id}',\n"
            f"    scrub: true,\n"
            f"    start: 'top bottom',\n"
            f"    end: 'bottom top'\n"
            f"  }}\n"
            f"}});"
        )
        return {
            "library": "gsap",
            "element_id": element_id,
            "speed": speed,
            "code": code,
            "imports": ["gsap", "ScrollTrigger"],
        }
