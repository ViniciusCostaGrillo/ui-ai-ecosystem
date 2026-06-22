import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class GsapAgent:
    """Agent that analyzes requirements and synthesizes GSAP animation code sequences."""

    def generate_timeline(self, element_id: str, effect: str) -> Dict[str, Any]:
        logger.info(f"GsapAgent: generating timeline for element={element_id}, effect={effect}")

        # Choose the right timeline animation code
        if effect == "stagger_reveal":
            code = (
                f"gsap.fromTo('#{element_id} .item', \n"
                f"  {{ opacity: 0, y: 50 }},\n"
                f"  {{ opacity: 1, y: 0, duration: 0.8, stagger: 0.2, ease: 'power3.out' }}\n"
                f");"
            )
        elif effect == "scroll_trigger_fade":
            code = (
                f"gsap.from('#{element_id}', {{\n"
                f"  scrollTrigger: {{\n"
                f"    trigger: '#{element_id}',\n"
                f"    start: 'top 80%',\n"
                f"    toggleActions: 'play none none reverse'\n"
                f"  }},\n"
                f"  opacity: 0,\n"
                f"  y: 30,\n"
                f"  duration: 1.0\n"
                f"}});"
            )
        else:
            code = f"gsap.to('#{element_id}', {{ opacity: 1, duration: 0.5 }});"

        return {
            "library": "gsap",
            "element_id": element_id,
            "effect": effect,
            "code": code,
            "imports": ["gsap", "ScrollTrigger"],
        }
