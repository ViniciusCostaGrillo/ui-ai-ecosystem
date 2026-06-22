import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class PackageRegistry:
    """Registry cataloging verified versions of motion, animation, and 3D libraries."""

    def __init__(self) -> None:
        self.packages: Dict[str, str] = {
            "gsap": "^3.12.2",
            "@studio-freight/lenis": "^1.0.28",
            "framer-motion": "^10.16.4",
            "three": "^0.156.1",
            "@react-three/fiber": "^8.14.2",
            "@react-three/drei": "^9.85.3",
            "lottie-react": "^2.4.0",
        }

    def get_version(self, name: str) -> Optional[str]:
        return self.packages.get(name)
