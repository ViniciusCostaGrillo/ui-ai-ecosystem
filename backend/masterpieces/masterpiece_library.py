import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class MasterpieceLibrary:
    """Manages files and prompt templates stored under the 'masterpieces/' folder."""

    def __init__(self) -> None:
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.masterpieces_dir = os.path.join(self.base_dir, "masterpieces")
        os.makedirs(self.masterpieces_dir, exist_ok=True)

    def list_local_masterpieces(self) -> List[str]:
        """Lists folders for locally cached masterpieces."""
        if not os.path.exists(self.masterpieces_dir):
            return []
        return [
            name for name in os.listdir(self.masterpieces_dir)
            if os.path.isdir(os.path.join(self.masterpieces_dir, name))
        ]

    def get_prompt_template(self, name: str) -> Optional[str]:
        """Reads a prompt template file (e.g. prompt_templates/elara.md)."""
        prompt_dir = os.path.join(self.base_dir, "prompt_templates")
        os.makedirs(prompt_dir, exist_ok=True)
        file_path = os.path.join(prompt_dir, f"{name.lower()}.md")
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
                
        # Return fallback template
        return f"""# Masterpiece Reference: {name.capitalize()}
Analyze and replicate the visual style of {name.capitalize()}:
- Color Palette: Rich Contrast
- Typography: Sophisticated Sans Serif
- Spacing: Wide, spacious breathing rooms
- GSAP triggers: Yes
"""

    def save_prompt_template(self, name: str, content: str) -> None:
        """Saves a prompt template file."""
        prompt_dir = os.path.join(self.base_dir, "prompt_templates")
        os.makedirs(prompt_dir, exist_ok=True)
        file_path = os.path.join(prompt_dir, f"{name.lower()}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def get_masterpiece_specs(self, name: str) -> Dict[str, Any]:
        """Loads specs for a given masterpiece folder."""
        folder = os.path.join(self.masterpieces_dir, name.lower())
        if not os.path.exists(folder):
            return {}

        specs = {}
        for filename in ["colors.json", "typography.json", "motion.json", "theme.json"]:
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        specs[filename.split(".")[0]] = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading masterpiece spec file '{filename}': {e}")
                    
        return specs
