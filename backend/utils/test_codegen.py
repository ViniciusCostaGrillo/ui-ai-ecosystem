import os
import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.codegen.code_generator import CodeGenerator
from backend.schemas.analyzer import AnalysisResult
from backend.schemas.extractor import ExtractionResult
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_codegen")


def run_tests() -> None:
    logger.info("Initializing Code Generator Test Harness...")

    # Define paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    playwright_dir = base_dir / "storage" / "test_crawl" / "playwright"

    extraction_path = playwright_dir / "extraction_result.json"
    analysis_path = playwright_dir / "metadata.json"

    if not extraction_path.exists():
        logger.error(f"Extraction file not found at: {extraction_path}")
        sys.exit(1)

    if not analysis_path.exists():
        logger.error(f"Analysis layout file not found at: {analysis_path}")
        sys.exit(1)

    # 1. Load data
    logger.info("Loading extraction result and analysis metadata JSON files...")
    with open(extraction_path, "r", encoding="utf-8") as f:
        extraction_data = f.read()

    with open(analysis_path, "r", encoding="utf-8") as f:
        analysis_data = f.read()

    # Validate back to Pydantic objects
    try:
        extraction = ExtractionResult.model_validate_json(extraction_data)
        analysis = AnalysisResult.model_validate_json(analysis_data)
        logger.info("Successfully validated files back into Pydantic models.")
    except Exception as e:
        logger.error(f"Failed to validate input files against Pydantic models: {e}")
        sys.exit(1)

    # 2. Run Code Generator
    generator = CodeGenerator()
    try:
        result = generator.generate(extraction, analysis)
    except Exception as e:
        logger.exception(f"Code generator service failed with exception: {e}")
        sys.exit(1)

    # 3. Output results
    logger.info("------------- Verification Results -------------")
    logger.info(f"React Components Generated (Count): {len(result.components)}")
    for i, comp in enumerate(result.components):
        logger.info(f"Component {i+1}: Name={comp.name}, Code size={len(comp.code)} chars")

    # Assertions
    logger.info("Running validation checks...")

    assert len(result.components) > 0, "No React components generated!"
    for comp in result.components:
        assert comp.name is not None and len(comp.name) > 0, "Component name missing!"
        assert "React" in comp.code, f"Component {comp.name} code is missing React imports!"
        assert "export default function" in comp.code, f"Component {comp.name} code is missing default export declaration!"
        assert "className=" in comp.code, f"Component {comp.name} code does not contain Tailwind classes!"

    logger.info("[PASS] Code generation output validations passed.")

    # 4. Save components to storage
    components_dir = playwright_dir / "components"
    os.makedirs(components_dir, exist_ok=True)
    logger.info(f"Writing generated components to: {components_dir}")

    for comp in result.components:
        comp_file = components_dir / f"{comp.name}.tsx"
        with open(comp_file, "w", encoding="utf-8") as cf:
            cf.write(comp.code)
        logger.info(f"Saved React component: {comp_file.name}")

    if result.global_styles:
        styles_file = playwright_dir / "global_styles.css"
        with open(styles_file, "w", encoding="utf-8") as sf:
            sf.write(result.global_styles)
        logger.info(f"Saved CSS variables to: {styles_file.name}")

    logger.info("ALL CODEGEN CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
