import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class PackageValidator:
    """Validates library dependencies structures and resolves target conflicts."""

    def validate_dependencies(self, deps: List[str]) -> Dict[str, Any]:
        logger.info(f"PackageValidator: validating dependencies {deps}...")

        conflicts = []
        resolved = list(deps)

        # Peer dependency validation checks
        if "@react-three/fiber" in deps and "three" not in deps:
            resolved.append("three")
            conflicts.append("Added missing peer dependency 'three' for '@react-three/fiber'")

        return {
            "resolved_dependencies": resolved,
            "conflicts_resolved": conflicts,
            "is_valid": True,
        }
