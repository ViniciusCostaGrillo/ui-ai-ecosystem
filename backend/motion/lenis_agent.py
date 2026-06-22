import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class LenisAgent:
    """Agent that generates smooth scrolling layouts configurations using Lenis."""

    def generate_scroll_config(self) -> Dict[str, Any]:
        logger.info("LenisAgent: generating Lenis smooth scroll configuration...")
        code = (
            "import { useEffect } from 'react';\n"
            "import Lenis from '@studio-freight/lenis';\n\n"
            "export function useSmoothScroll() {\n"
            "  useEffect(() => {\n"
            "    const lenis = new Lenis({\n"
            "      duration: 1.2,\n"
            "      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),\n"
            "      direction: 'vertical',\n"
            "      gestureDirection: 'vertical',\n"
            "      smooth: true,\n"
            "      mouseMultiplier: 1,\n"
            "      smoothTouch: false,\n"
            "      touchMultiplier: 2,\n"
            "      infinite: false,\n"
            "    });\n\n"
            "    function raf(time) {\n"
            "      lenis.raf(time);\n"
            "      requestAnimationFrame(raf);\n"
            "    }\n"
            "    requestAnimationFrame(raf);\n\n"
            "    return () => {\n"
            "      lenis.destroy();\n"
            "    };\n"
            "  }, []);\n"
            "}"
        )
        return {
            "library": "@studio-freight/lenis",
            "code": code,
            "hook_name": "useSmoothScroll",
        }
