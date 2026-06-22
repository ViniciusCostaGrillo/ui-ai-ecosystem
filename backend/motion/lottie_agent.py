import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class LottieAgent:
    """Agent that parses lottie animation requests and generates Lottie React embeddings."""

    def generate_animation_component(self, name: str, animation_url: str) -> Dict[str, Any]:
        logger.info(f"LottieAgent: generating Lottie component '{name}' from url '{animation_url}'")
        code = (
            "import React from 'react';\n"
            "import Lottie from 'lottie-react';\n\n"
            f"export default function {name}Animation() {{\n"
            "  const style = {\n"
            "    height: 300,\n"
            "  };\n\n"
            "  return (\n"
            f"    <Lottie animationData={{}} loop={{true}} style={{style}} />\n"
            "  );\n"
            "}"
        )
        return {
            "library": "lottie-react",
            "code": code,
            "component_name": f"{name}Animation",
        }
