import re
from typing import Set
from bs4 import BeautifulSoup
from backend.schemas.extractor import ExtractedStyles
from backend.utils.custom_logger import setup_logger

logger = setup_logger("extractor.css_parser")

# CSS parsing patterns
HEX_COLOR_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{3,4}){1,2}\b")
RGB_HSL_COLOR_PATTERN = re.compile(r"(?:rgb|hsl)a?\([^)]+\)", re.IGNORECASE)
GOOGLE_FONT_PATTERN = re.compile(r"family=([^&:]+)", re.IGNORECASE)


class CssParser:
    """Parser to extract visual styling attributes (colors, fonts, layout indicators, class names)

    from HTML content, stylesheet tags, and class utility declarations.
    """

    def parse(self, soup: BeautifulSoup) -> ExtractedStyles:
        logger.debug("Starting CSS styles parsing...")
        colors: Set[str] = set()
        fonts: Set[str] = set()
        class_list: Set[str] = set()

        layout_rules = {
            "display_counts": {},
            "position_counts": {},
            "has_flex": False,
            "has_grid": False,
            "box_model": {
                "padding_elements_count": 0,
                "margin_elements_count": 0,
            },
        }

        # 1. Check style tags for colors and font rules
        for style_tag in soup.find_all("style"):
            style_content = style_tag.string
            if style_content:
                # Find hex colors
                for color in HEX_COLOR_PATTERN.findall(style_content):
                    colors.add(color.lower())
                # Find rgb/hsl colors
                for color in RGB_HSL_COLOR_PATTERN.findall(style_content):
                    colors.add(color.lower())

                # Find font-family rules
                font_families = re.findall(
                    r"font-family\s*:\s*([^;}]+)", style_content, re.IGNORECASE
                )
                for family_decl in font_families:
                    for part in family_decl.split(","):
                        clean_font = part.strip().strip("'\"")
                        if clean_font:
                            fonts.add(clean_font)

        # 2. Check external webfont stylesheets (e.g. Google Fonts)
        for link in soup.find_all("link", rel="stylesheet"):
            href = link.get("href", "")
            if "fonts.googleapis.com" in href or "fonts.cdnfonts.com" in href:
                matches = GOOGLE_FONT_PATTERN.findall(href)
                for match in matches:
                    font_name = match.replace("+", " ").strip()
                    if font_name:
                        fonts.add(font_name)

        # 3. Scan DOM elements for inline style attributes and class lists
        for element in soup.find_all(True):
            # Class list extraction
            classes = element.get("class")
            if classes:
                if isinstance(classes, list):
                    for cls in classes:
                        class_list.add(cls)
                elif isinstance(classes, str):
                    class_list.add(classes)

            # Inline styles extraction
            style_attr = element.get("style")
            if style_attr:
                declarations = style_attr.split(";")
                for decl in declarations:
                    if ":" not in decl:
                        continue
                    key, val = decl.split(":", 1)
                    key = key.strip().lower()
                    val = val.strip().lower()

                    # Color properties
                    if key in ("color", "background-color", "background", "border-color"):
                        for color in HEX_COLOR_PATTERN.findall(val):
                            colors.add(color.lower())
                        for color in RGB_HSL_COLOR_PATTERN.findall(val):
                            colors.add(color.lower())

                    # Font properties
                    elif key == "font-family":
                        for part in val.split(","):
                            clean_font = part.strip().strip("'\"")
                            if clean_font:
                                fonts.add(clean_font)

                    # Layout configurations
                    elif key == "display":
                        layout_rules["display_counts"][val] = (
                            layout_rules["display_counts"].get(val, 0) + 1
                        )
                        if "flex" in val:
                            layout_rules["has_flex"] = True
                        if "grid" in val:
                            layout_rules["has_grid"] = True
                    elif key == "position":
                        layout_rules["position_counts"][val] = (
                            layout_rules["position_counts"].get(val, 0) + 1
                        )
                    elif key.startswith("padding"):
                        layout_rules["box_model"]["padding_elements_count"] += 1
                    elif key.startswith("margin"):
                        layout_rules["box_model"]["margin_elements_count"] += 1

            # Extract layout metrics from Tailwind-like utilities in classes
            if classes and isinstance(classes, list):
                for cls in classes:
                    if cls == "flex":
                        layout_rules["has_flex"] = True
                        layout_rules["display_counts"]["flex"] = (
                            layout_rules["display_counts"].get("flex", 0) + 1
                        )
                    elif cls == "grid":
                        layout_rules["has_grid"] = True
                        layout_rules["display_counts"]["grid"] = (
                            layout_rules["display_counts"].get("grid", 0) + 1
                        )
                    elif (
                        cls.startswith("p-")
                        or cls.startswith("px-")
                        or cls.startswith("py-")
                        or cls.startswith("pt-")
                        or cls.startswith("pb-")
                        or cls.startswith("pl-")
                        or cls.startswith("pr-")
                    ):
                        layout_rules["box_model"]["padding_elements_count"] += 1
                    elif (
                        cls.startswith("m-")
                        or cls.startswith("mx-")
                        or cls.startswith("my-")
                        or cls.startswith("mt-")
                        or cls.startswith("mb-")
                        or cls.startswith("ml-")
                        or cls.startswith("mr-")
                    ):
                        layout_rules["box_model"]["margin_elements_count"] += 1
                    elif cls in ("relative", "absolute", "fixed", "sticky"):
                        layout_rules["position_counts"][cls] = (
                            layout_rules["position_counts"].get(cls, 0) + 1
                        )

        sorted_colors = sorted(list(colors))
        sorted_fonts = sorted(list(fonts))
        sorted_classes = sorted(list(class_list))

        logger.debug(
            f"CSS Parsing completed: {len(sorted_colors)} colors, "
            f"{len(sorted_fonts)} fonts, {len(sorted_classes)} classes extracted."
        )

        return ExtractedStyles(
            colors=sorted_colors,
            fonts=sorted_fonts,
            layout_rules=layout_rules,
            class_list=sorted_classes,
        )
