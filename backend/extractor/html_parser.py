from typing import List, Optional
from bs4 import BeautifulSoup, Tag
from backend.schemas.extractor import SemanticElement
from backend.utils.custom_logger import setup_logger

logger = setup_logger("extractor.html_parser")


class HtmlParser:
    """Parser to construct a recursive SemanticElement tree from HTML content,

    focusing on high-value semantic nodes and interactive layout elements.
    """

    def parse(self, soup: BeautifulSoup) -> List[SemanticElement]:
        logger.debug("Starting HTML DOM semantic parsing...")

        # We start parsing from body if available, otherwise from the soup root
        root = soup.body if soup.body else soup

        elements: List[SemanticElement] = []
        # Find all direct children of the root element
        for child in root.find_all(recursive=False):
            if isinstance(child, Tag):
                parsed = self._parse_node(child)
                if parsed:
                    elements.append(parsed)

        logger.debug(
            f"HTML parsing completed. Extracted {len(elements)} top-level elements."
        )
        return elements

    def _parse_node(self, element: Tag) -> Optional[SemanticElement]:
        tag_name = element.name.lower()

        # Ignored tags
        ignored_tags = {
            "script",
            "style",
            "noscript",
            "svg",
            "path",
            "g",
            "iframe",
            "embed",
            "object",
            "link",
            "head",
            "meta",
            "param",
            "source",
        }
        if tag_name in ignored_tags:
            return None

        # Extract attributes of interest
        attributes = {}
        target_attrs = [
            "id",
            "class",
            "href",
            "src",
            "alt",
            "placeholder",
            "type",
            "name",
            "value",
            "role",
            "aria-label",
        ]
        for attr in target_attrs:
            val = element.get(attr)
            if val is not None:
                if isinstance(val, list):
                    attributes[attr] = " ".join(val)
                else:
                    attributes[attr] = str(val)

        # Parse children first
        children = []
        for child in element.find_all(recursive=False):
            if isinstance(child, Tag):
                parsed_child = self._parse_node(child)
                if parsed_child:
                    children.append(parsed_child)

        # Get direct text content
        # If it has no children, we can use the entire text content.
        # Otherwise, get only the direct text elements to avoid duplication.
        if not children:
            text = element.get_text(strip=True)
        else:
            text = "".join(
                child for child in element.children if isinstance(child, str)
            ).strip()

        # If text is empty, set to None
        text_val = text if text else None

        # Filter out completely empty container elements to keep the DOM clean
        is_empty_container = (
            not text_val
            and not children
            and not attributes
            and tag_name in {"div", "span", "section", "article", "main", "p"}
        )
        if is_empty_container:
            return None

        return SemanticElement(
            tag=tag_name,
            text=text_val,
            attributes=attributes,
            children=children,
        )
