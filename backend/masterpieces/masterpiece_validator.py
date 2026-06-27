import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MasterpieceValidator:
    """Validator that checks masterpiece components, designs, and visual scores."""

    def validate_code(self, code: str) -> Dict[str, Any]:
        """Validates component code structure (e.g. imports, responsiveness classes)."""
        errors = []
        warnings = []
        
        # Check standard React/Tailwind properties
        if "className" not in code:
            warnings.append("Component does not use any Tailwind classes (className missing).")
        
        # Check if responsive utility prefixes are used (sm:, md:, lg:)
        responsive_rules = ["sm:", "md:", "lg:", "xl:"]
        if not any(rule in code for rule in responsive_rules):
            warnings.append("Component lacks responsive utility classes (sm:, md:, lg:).")

        # Check for imports
        if "import " not in code:
            errors.append("Component has no imports.")
            
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    def validate_design_rules(self, design_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validates colors, typography, and spacing specs."""
        errors = []
        if "colors" not in design_rules or not design_rules["colors"]:
            errors.append("Design system requires at least one primary color hex code.")
        if "typography" not in design_rules or not design_rules["typography"]:
            errors.append("Design system requires font pairings.")
            
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    def calculate_score(
        self,
        performance: float,
        accessibility: float,
        visual_quality: float,
        responsiveness: float
    ) -> float:
        """Heuristic calculation of Masterpiece Design Score."""
        # Weighted score: 40% Visual, 20% Performance, 20% A11y, 20% Responsiveness
        score = (visual_quality * 0.40) + (performance * 0.20) + (accessibility * 0.20) + (responsiveness * 0.20)
        return round(score, 1)
