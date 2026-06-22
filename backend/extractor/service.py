from bs4 import BeautifulSoup
from backend.schemas.extractor import ExtractionResult
from backend.extractor.metadata_parser import MetadataParser
from backend.extractor.html_parser import HtmlParser
from backend.extractor.css_parser import CssParser
from backend.extractor.text_parser import TextParser
from backend.utils.custom_logger import setup_logger

logger = setup_logger("extractor.service")


class ExtractorService:
    """Orchestrates metadata, semantic element DOM, CSS style, and clean text parsers

    to convert raw HTML content into a structured, validated ExtractionResult.
    """

    def __init__(self) -> None:
        self.metadata_parser = MetadataParser()
        self.html_parser = HtmlParser()
        self.css_parser = CssParser()
        self.text_parser = TextParser()
        logger.debug("ExtractorService sub-parsers initialized successfully.")

    def extract(self, html_content: str) -> ExtractionResult:
        logger.info("Starting extraction workflow...")
        if not html_content or not html_content.strip():
            logger.error("Attempted extraction on empty HTML content.")
            raise ValueError("HTML content cannot be empty.")

        # Parse HTML using BeautifulSoup and lxml
        logger.debug("Loading HTML string into BeautifulSoup (lxml parser)...")
        soup = BeautifulSoup(html_content, "lxml")

        # 1. Page Metadata (SEO / OpenGraph tags)
        logger.debug("Executing MetadataParser...")
        metadata = self.metadata_parser.parse(soup)

        # 2. DOM Elements (Semantic tree hierarchy)
        logger.debug("Executing HtmlParser...")
        elements = self.html_parser.parse(soup)

        # 3. CSS Styles (Colors, fonts, layout classes)
        logger.debug("Executing CssParser...")
        styles = self.css_parser.parse(soup)

        # 4. Boilerplate-free body text
        logger.debug("Executing TextParser...")
        clean_text = self.text_parser.parse(html_content)

        logger.info("Extraction workflow completed.")
        return ExtractionResult(
            metadata=metadata,
            elements=elements,
            styles=styles,
            clean_text=clean_text,
        )
