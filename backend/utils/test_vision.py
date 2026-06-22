import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.utils.custom_logger import setup_logger
from backend.vision.analyzer import VisionAnalyzer

logger = setup_logger("utils.test_vision")


def run_tests() -> None:
    logger.info("Initializing Vision Service Test Harness...")

    # Define paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    img_path = base_dir / "storage" / "test_crawl" / "playwright" / "screenshot.png"

    if not img_path.exists():
        logger.error(f"Test screenshot file not found at: {img_path}")
        sys.exit(1)

    logger.info(f"Loading screenshot from: {img_path}")

    # Instantiate vision analyzer
    analyzer = VisionAnalyzer()

    # Analyze screenshot
    try:
        result = analyzer.analyze(str(img_path))
    except Exception as e:
        logger.exception(f"Visual analysis failed with exception: {e}")
        sys.exit(1)

    # Output verification details
    logger.info("------------- Verification Results -------------")
    logger.info(f"Primary Background Color: {result.colors.background_color}")
    logger.info(f"Dominant Colors: {result.colors.dominant_colors}")
    logger.info(f"Content Area Density: {result.density.content_percentage}%")
    logger.info(f"Whitespace Density: {result.density.whitespace_percentage}%")
    logger.info(f"Estimated Margins: {result.spacing.margins}")
    logger.info(f"Estimated Content Gaps: {result.spacing.content_gaps}")
    logger.info(f"Grid Layout Type: {result.grid.grid_type}")
    logger.info(f"Vertical Splits: {result.grid.vertical_splits}")
    logger.info(f"Horizontal Splits: {result.grid.horizontal_splits}")

    # Assertions
    logger.info("Running validation checks...")

    # 1. Colors checks
    assert result.colors.background_color is not None, "Background color is null!"
    assert result.colors.background_color.startswith("#"), "Background color must be hex string!"
    assert len(result.colors.dominant_colors) > 0, "No dominant colors extracted!"
    for color in result.colors.dominant_colors:
        assert color.startswith("#"), f"Color code {color} must be hex!"
    logger.info("[PASS] Color extraction checks passed.")

    # 2. Density checks
    assert 0.0 <= result.density.content_percentage <= 100.0, "Content density range invalid!"
    assert 0.0 <= result.density.whitespace_percentage <= 100.0, "Whitespace density range invalid!"
    assert abs(result.density.content_percentage + result.density.whitespace_percentage - 100.0) < 0.1, "Density sum must be 100%!"
    logger.info("[PASS] Visual density checks passed.")

    # 3. Spacing checks
    for dir_key in ["top", "bottom", "left", "right"]:
        assert dir_key in result.spacing.margins, f"Margin direction {dir_key} missing!"
        assert result.spacing.margins[dir_key] >= 0, f"Margin value for {dir_key} must be non-negative!"
    logger.info("[PASS] Spacing metrics checks passed.")

    # 4. Grid checks
    assert result.grid.grid_type in [
        "grid",
        "stacked_sections",
        "single_column",
    ] or result.grid.grid_type.startswith("multi_column_"), "Invalid grid type classified!"
    logger.info("[PASS] Grid layout checks passed.")

    # Schema Export check
    try:
        json_data = result.model_dump_json(indent=2)
        logger.info("Pydantic Schema Serialization check passed.")

        # Write output vision metadata JSON for inspection
        output_json_path = (
            base_dir / "storage" / "test_crawl" / "playwright" / "vision_metadata.json"
        )
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            out_f.write(json_data)
        logger.info(f"Vision metadata serialized and saved to: {output_json_path}")
    except Exception as e:
        logger.error(f"Failed schema serialization check: {e}")
        sys.exit(1)

    logger.info("ALL VISION CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
