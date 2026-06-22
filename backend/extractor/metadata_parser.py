from bs4 import BeautifulSoup
from backend.schemas.extractor import PageMetadata
from backend.utils.custom_logger import setup_logger

logger = setup_logger("extractor.metadata_parser")


class MetadataParser:
    """Parser to extract website meta headers (SEO and OpenGraph keys)."""

    def parse(self, soup: BeautifulSoup) -> PageMetadata:
        logger.debug("Starting metadata parsing...")
        
        # 1. Title
        title = soup.title.string.strip() if soup.title else None

        # 2. Description & Keywords
        description = None
        keywords = None
        og_properties = {}

        # Look through all meta tags
        for meta in soup.find_all("meta"):
            name = meta.get("name", "").lower()
            property_attr = meta.get("property", "").lower()
            content = meta.get("content", "").strip()

            if not content:
                continue

            if name == "description":
                description = content
            elif name == "keywords":
                keywords = content
            elif property_attr.startswith("og:") or property_attr.startswith("twitter:"):
                og_properties[property_attr] = content

        logger.debug("Metadata parsing completed successfully")
        return PageMetadata(
            title=title,
            description=description,
            keywords=keywords,
            og_properties=og_properties,
        )
