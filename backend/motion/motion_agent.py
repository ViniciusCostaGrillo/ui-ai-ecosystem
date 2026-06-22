import logging
from typing import Any, Dict

from backend.motion.gsap_agent import GsapAgent
from backend.motion.lenis_agent import LenisAgent
from backend.motion.lottie_agent import LottieAgent
from backend.motion.microinteraction_agent import MicrointeractionAgent
from backend.motion.parallax_agent import ParallaxAgent
from backend.motion.transition_agent import TransitionAgent

logger = logging.getLogger(__name__)


class MotionAgent:
    """Orchestrator for the Advanced Motion Engine cluster."""

    def __init__(self) -> None:
        self.gsap = GsapAgent()
        self.lenis = LenisAgent()
        self.lottie = LottieAgent()
        self.parallax = ParallaxAgent()
        self.transition = TransitionAgent()
        self.microinteraction = MicrointeractionAgent()

    def generate_animation_suite(self, element_id: str) -> Dict[str, Any]:
        logger.info(f"MotionAgent: compiling full motion animation suite for element={element_id}...")
        return {
            "gsap": self.gsap.generate_timeline(element_id, "stagger_reveal"),
            "lenis": self.lenis.generate_scroll_config(),
            "lottie": self.lottie.generate_animation_component("Loading", "https://assets.local/anim.json"),
            "parallax": self.parallax.generate_parallax(element_id, 0.5),
            "transition": self.transition.generate_page_transition(),
            "microinteraction": self.microinteraction.generate_hover_microinteraction("magnetic"),
        }
