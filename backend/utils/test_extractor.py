import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.extractor.service import ExtractorService
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_extractor")


def run_tests() -> None:
    logger.info("Initializing Extractor Service Test Harness...")

    # Define paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    html_path = base_dir / "storage" / "test_crawl" / "playwright" / "page.html"

    if not html_path.exists():
        logger.error(f"Test HTML file not found at: {html_path}")
        sys.exit(1)

    logger.info(f"Loading HTML content from: {html_path}")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Instantiate extractor service
    service = ExtractorService()

    # Extract info
    try:
        result = service.extract(html_content)
    except Exception as e:
        logger.exception(f"Extraction failed with exception: {e}")
        sys.exit(1)

    # Output verification details
    logger.info("------------- Verification Results -------------")
    logger.info(f"Page Title: {result.metadata.title}")
    logger.info(f"Description: {result.metadata.description}")
    logger.info(f"Keywords: {result.metadata.keywords}")
    logger.info(f"Unique CSS Colors: {result.styles.colors}")
    logger.info(f"Unique Font Families: {result.styles.fonts}")
    logger.info(f"Unique Class Names (Count): {len(result.styles.class_list)}")
    logger.info(f"Layout Rules Summary: {result.styles.layout_rules}")
    logger.info(f"Clean Text Length: {len(result.clean_text)}")
    logger.info(f"DOM Semantic Nodes Extracted: {len(result.elements)}")

    # Assertions
    logger.info("Running validation checks...")

    # 1. Metadata checks
    assert result.metadata.title == "Example Domain", "Title mismatch!"
    logger.info("[PASS] Metadata checks passed.")

    # 2. Text Parser checks
    assert "This domain is for use" in result.clean_text, "Body text missing from clean text!"
    logger.info("[PASS] Text parser checks passed.")

    # 3. CSS Parser checks
    # Expect colors #eee and #348
    colors_lower = [c.lower() for c in result.styles.colors]
    assert any("eee" in c for c in colors_lower), "Color #eee not extracted!"
    assert any("348" in c for c in colors_lower), "Color #348 not extracted!"
    # Expect font system-ui, sans-serif
    fonts_lower = [f.lower() for f in result.styles.fonts]
    assert "system-ui" in fonts_lower, "Font system-ui not extracted!"
    assert "sans-serif" in fonts_lower, "Font sans-serif not extracted!"
    logger.info("[PASS] CSS parser checks passed.")

    # 4. DOM Parser checks
    # Verify we extracted h1, p, a tags recursively
    def has_tag(nodes, target_tag):
        for node in nodes:
            if node.tag == target_tag:
                return True
            if has_tag(node.children, target_tag):
                return True
        return False

    assert has_tag(result.elements, "h1"), "H1 tag not found in semantic elements tree!"
    assert has_tag(result.elements, "p"), "P tag not found in semantic elements tree!"
    assert has_tag(result.elements, "a"), "A tag not found in semantic elements tree!"
    logger.info("[PASS] HTML DOM parser checks passed.")

    # Schema Export check
    try:
        json_data = result.model_dump_json(indent=2)
        logger.info("Pydantic Schema Serialization check passed.")
        
        # Write clean output summary for inspection
        output_json_path = base_dir / "storage" / "test_crawl" / "playwright" / "extraction_result.json"
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            out_f.write(json_data)
        logger.info(f"Extraction result serialized and saved to: {output_json_path}")
    except Exception as e:
        logger.error(f"Failed schema serialization check: {e}")
        sys.exit(1)

    logger.info("ALL EXTRACTION CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
