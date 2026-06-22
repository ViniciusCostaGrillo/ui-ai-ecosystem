import trafilatura
from bs4 import BeautifulSoup
from backend.utils.custom_logger import setup_logger

logger = setup_logger("extractor.text_parser")


class TextParser:
    """Parser to extract clean, boilerplate-free text from HTML content using Trafilatura,

    with a BeautifulSoup fallback if Trafilatura returns no results.
    """

    def parse(self, html_content: str) -> str:
        logger.debug("Starting text extraction with Trafilatura...")
        if not html_content or not html_content.strip():
            logger.warning("Empty HTML content received, returning empty string.")
            return ""

        try:
            # Attempt extraction with Trafilatura
            extracted_text = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=True,
                no_fallback=False,
            )
            
            if extracted_text:
                logger.debug(
                    f"Trafilatura successfully extracted {len(extracted_text)} characters."
                )
                return extracted_text.strip()
                
            logger.info("Trafilatura returned no content. Falling back to BeautifulSoup text extraction.")
        except Exception as e:
            logger.exception(f"Error during Trafilatura extraction: {e}. Falling back to BeautifulSoup.")

        # Fallback to BeautifulSoup get_text
        try:
            soup = BeautifulSoup(html_content, "lxml")
            # Remove scripts, styles, and SVG content to avoid junk
            for element in soup(["script", "style", "svg", "noscript"]):
                element.decompose()
            
            fallback_text = soup.get_text(separator="\n", strip=True)
            logger.debug(
                f"BeautifulSoup fallback successfully extracted {len(fallback_text)} characters."
            )
            return fallback_text
        except Exception as e:
            logger.exception(f"Error during BeautifulSoup fallback text extraction: {e}")
            return ""
