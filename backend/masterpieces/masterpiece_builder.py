import os
import json
import logging
from typing import Dict, Any, List
import yaml

logger = logging.getLogger(__name__)


class MasterpieceBuilder:
    """Auto-generates structured files (yaml, md, json specs) for promoted websites inside masterpieces/ directory."""

    def __init__(self) -> None:
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.masterpieces_dir = os.path.join(self.base_dir, "masterpieces")
        os.makedirs(self.masterpieces_dir, exist_ok=True)

    def build(self, name: str, url: str, category: List[str], details: Dict[str, Any]) -> str:
        """Builds folder structure and files (colors, typography, skill, DESIGN.md) for a masterpiece."""
        mp_name = name.lower().replace(" ", "_")
        folder = os.path.join(self.masterpieces_dir, mp_name)
        os.makedirs(folder, exist_ok=True)

        logger.info(f"MasterpieceBuilder: Generating files in '{folder}' for {name}.")

        # 1. Generate colors.json
        colors = details.get("colors", ["#0a0a0a", "#f5f5f7", "#d4af37"])
        with open(os.path.join(folder, "colors.json"), "w", encoding="utf-8") as f:
            json.dump(colors, f, indent=2)

        # 2. Generate typography.json
        typography = details.get("typography", ["Playfair Display", "Inter"])
        with open(os.path.join(folder, "typography.json"), "w", encoding="utf-8") as f:
            json.dump(typography, f, indent=2)

        # 3. Generate motion.json
        motion = details.get("motion", {
            "gsap": ["TimelineLite", "ScrollTrigger"],
            "preset": "stagger_reveal"
        })
        with open(os.path.join(folder, "motion.json"), "w", encoding="utf-8") as f:
            json.dump(motion, f, indent=2)

        # 4. Generate theme.json
        theme = details.get("theme", {
            "name": f"{mp_name}_theme",
            "type": "dark_gold" if "luxury" in category else "minimal_dark"
        })
        with open(os.path.join(folder, "theme.json"), "w", encoding="utf-8") as f:
            json.dump(theme, f, indent=2)

        # 5. Generate skill.yaml (System skills matching FASE 27)
        skill_data = {
            "name": f"{mp_name}_skill",
            "description": f"Custom layout synthesis parameters learned from {name}.",
            "category": category,
            "rules": [
                f"Prioritize visual layouts emphasizing {', '.join(category)} features.",
                f"Combine fonts {', '.join(typography)} for headline-body pairings.",
                "Inject smooth Lenis scrolling animations."
            ]
        }
        
        # Save skill.yaml inside the masterpiece folder
        with open(os.path.join(folder, "skill.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(skill_data, f, default_flow_style=False)

        # Also save to backend/skills/ for skill engine execution
        skills_dest = os.path.join(self.base_dir, "backend", "skills")
        os.makedirs(skills_dest, exist_ok=True)
        with open(os.path.join(skills_dest, f"{mp_name}_skill.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(skill_data, f, default_flow_style=False)

        # 6. Generate DESIGN.md
        design_md = f"""# Masterpiece Design Specifications: {name}

Reference URL: {url}
Category Tags: {', '.join(category)}

## Style Guidelines
- **Artistic Statement**: Premium high-end layout utilizing custom visual tokens.
- **Color Palette**: {', '.join(colors)}
- **Typography pairing**: {', '.join(typography)}
- **Transitions and Scroll**: Custom GSAP timelines and Lenis integrations.

## Components Map
* Hero layout: Large italics displaying brand name overlays
* Metrics grid: Clean border-line separations
* Animation triggers: Slow staggered fade-in animations on viewport scroll
"""
        with open(os.path.join(folder, "DESIGN.md"), "w", encoding="utf-8") as f:
            f.write(design_md)

        # 7. Write a custom prompt template under prompt_templates/
        prompt_templates_dir = os.path.join(self.base_dir, "prompt_templates")
        os.makedirs(prompt_templates_dir, exist_ok=True)
        prompt_md = f"""# Prompt Template: {name}
Create a layout matching the {name} aesthetic:
- Spacing: Spacious and airy margins (min 120px)
- Contrast: Dark Editorial contrast
- Fonts: {', '.join(typography)}
- Colors: {', '.join(colors)}
"""
        with open(os.path.join(prompt_templates_dir, f"{mp_name}.md"), "w", encoding="utf-8") as f:
            f.write(prompt_md)

        return os.path.relpath(folder, self.base_dir)
