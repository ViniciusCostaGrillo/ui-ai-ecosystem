import os
import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.rag.embeddings import EmbeddingGenerator
from backend.schemas.analyzer import AnalysisResult
from backend.schemas.codegen import GeneratedComponent
from backend.schemas.embeddings import EcosystemEmbeddings
from backend.schemas.extractor import ExtractionResult
from backend.schemas.vision import VisionMetadata
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_embeddings")


def run_tests() -> None:
    logger.info("Initializing Embeddings Test Harness...")

    # Define paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    site_dir = base_dir / "dataset" / "site_000001"

    extraction_path = site_dir / "extraction_result.json"
    vision_path = site_dir / "vision_metadata.json"
    analysis_path = site_dir / "layout_analysis.json"
    components_dir = site_dir / "components"

    # Verify input existence
    for path in [extraction_path, vision_path, analysis_path, components_dir]:
        if not path.exists():
            logger.error(f"Input asset not found at: {path}")
            sys.exit(1)

    # 1. Load Pydantic files
    logger.info("Loading extractions, visual meta, and layout analysis files...")
    try:
        with open(extraction_path, "r", encoding="utf-8") as f:
            extraction = ExtractionResult.model_validate_json(f.read())
        with open(vision_path, "r", encoding="utf-8") as f:
            vision = VisionMetadata.model_validate_json(f.read())
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis = AnalysisResult.model_validate_json(f.read())
        logger.info("[PASS] Input Pydantic models loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load input JSON models: {e}")
        sys.exit(1)

    # 2. Load React components code
    logger.info("Reading generated React component TSX files...")
    components = []
    for file in os.listdir(components_dir):
        if file.endswith(".tsx"):
            comp_name = file.replace(".tsx", "")
            comp_path = components_dir / file
            with open(comp_path, "r", encoding="utf-8") as f:
                code = f.read()
            components.append(
                GeneratedComponent(
                    name=comp_name,
                    code=code,
                    description=f"React component {comp_name} loaded from packaged folder."
                )
            )

    # 3. Generate Embeddings
    generator = EmbeddingGenerator()

    # Page Embedding
    logger.info("Generating page content embedding...")
    try:
        page_emb = generator.generate_page_embedding(extraction, analysis)
    except Exception as e:
        logger.error(f"Failed generating page embedding: {e}")
        sys.exit(1)

    # Style Embedding
    logger.info("Generating styling rules embedding...")
    try:
        style_emb = generator.generate_style_embedding(analysis, vision)
    except Exception as e:
        logger.error(f"Failed generating style embedding: {e}")
        sys.exit(1)

    # Components Embeddings
    logger.info("Generating components code embeddings...")
    comp_embs = []
    for comp in components:
        # Match with component metadata from analysis
        comp_meta = None
        for m in analysis.components:
            # simple fuzzy match
            if m.type.lower() in comp.name.lower():
                comp_meta = m
                break
        
        # Fallback if no match
        if not comp_meta:
            comp_meta = analysis.components[0]

        try:
            comp_emb = generator.generate_component_embedding(comp, comp_meta)
            comp_embs.append(comp_emb)
        except Exception as e:
            logger.error(f"Failed generating component embedding for {comp.name}: {e}")
            sys.exit(1)

    # 4. Package results
    ecosystem_embs = EcosystemEmbeddings(
        page=page_emb,
        components=comp_embs,
        style=style_emb
    )

    # 5. Assertions
    logger.info("------------- Verification Results -------------")
    logger.info(f"Page Vector Size: {len(ecosystem_embs.page.page_vector)} dimensions")
    logger.info(f"Style Vector Size: {len(ecosystem_embs.style.vector)} dimensions")
    logger.info(f"Components Embedded Count: {len(ecosystem_embs.components)}")
    for c in ecosystem_embs.components:
        logger.info(f"- Component {c.component_id} Vector Size: {len(c.vector)} dimensions")

    logger.info("Running validation checks...")
    # MiniLM dimensions is 384
    assert len(ecosystem_embs.page.page_vector) == 384, "Page vector dimension mismatch!"
    assert len(ecosystem_embs.style.vector) == 384, "Style vector dimension mismatch!"
    assert len(ecosystem_embs.components) == len(components), "Component embeddings count mismatch!"
    for c in ecosystem_embs.components:
        assert len(c.vector) == 384, f"Component {c.component_id} vector dimension mismatch!"

    logger.info("[PASS] Vector dimension validation checks passed.")

    # 6. Save embeddings JSON
    try:
        json_data = ecosystem_embs.model_dump_json(indent=2)
        output_json_path = site_dir / "embeddings.json"
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            out_f.write(json_data)
        logger.info(f"Ecosystem embeddings serialized and saved to: {output_json_path}")
    except Exception as e:
        logger.error(f"Failed schema serialization check: {e}")
        sys.exit(1)

    logger.info("ALL EMBEDDINGS CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
