import logging
from typing import Any, Dict, List

from backend.dependencies.package_registry import PackageRegistry
from backend.dependencies.package_validator import PackageValidator

logger = logging.getLogger(__name__)


class DependencyAgent:
    """Agent in charge of managing package dependencies requirements and validators."""

    def __init__(self) -> None:
        self.registry = PackageRegistry()
        self.validator = PackageValidator()

    def resolve_requirements(self, required_libs: List[str]) -> Dict[str, Any]:
        logger.info(f"DependencyAgent: resolving version constraints for {required_libs}...")

        # 1. Validate
        validation = self.validator.validate_dependencies(required_libs)
        resolved_libs = validation["resolved_dependencies"]

        # 2. Map versions
        manifest_deps = {}
        for lib in resolved_libs:
            version = self.registry.get_version(lib) or "latest"
            manifest_deps[lib] = version

        return {
            "dependencies": manifest_deps,
            "conflicts_resolved": validation["conflicts_resolved"],
            "status": "success",
        }
