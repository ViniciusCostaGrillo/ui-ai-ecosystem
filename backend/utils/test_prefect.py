import os
import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.orchestration.prefect_flow import generation_pipeline_flow
from backend.database.chroma_client import ChromaClientManager
from backend.rag.embeddings import EmbeddingGenerator
from backend.schemas.dataset_builder import DatasetManifest
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_prefect")


def run_tests() -> None:
    logger.info("Initializing Prefect Orchestration Test Harness...")

    # Define paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    site_dir = base_dir / "dataset" / "site_000004"

    # Reset site directory from previous runs to ensure clean test
    if site_dir.exists():
        import shutil
        logger.info(f"Removing old dataset directory: {site_dir}")
        shutil.rmtree(site_dir)

    # 1. Execute Prefect generation flow
    logger.info("Executing Prefect automated flow...")
    try:
        flow_result = generation_pipeline_flow(
            url="https://example.com",
            target_framework="React",
            project_id=4
        )
    except Exception as e:
        logger.exception(f"Prefect flow run failed with exception: {e}")
        sys.exit(1)

    logger.info("------------- Prefect Flow Execution Results -------------")
    logger.info(f"Flow returned site directory: {flow_result.get('site_dir')}")
    logger.info(f"RAG indexed documents count: {flow_result.get('rag_indexed_docs')}")

    # 2. Verify packaged assets
    logger.info("Verifying generated package structures...")
    assert site_dir.exists(), "Dataset site package directory site_000004 not created!"
    assert (site_dir / "raw_html.html").exists(), "raw_html.html missing from package!"
    assert (site_dir / "screenshot.png").exists(), "screenshot.png missing from package!"
    assert (site_dir / "extraction_result.json").exists(), "extraction_result.json missing from package!"
    assert (site_dir / "vision_metadata.json").exists(), "vision_metadata.json missing from package!"
    assert (site_dir / "layout_analysis.json").exists(), "layout_analysis.json missing from package!"
    assert (site_dir / "manifest.json").exists(), "manifest.json index missing from package!"

    # Verify component subfolder contains generated components
    components_dir = site_dir / "components"
    assert components_dir.exists(), "components subfolder missing!"
    components_files = [f for f in os.listdir(components_dir) if f.endswith(".tsx")]
    assert len(components_files) > 0, "No React components found in components subfolder!"
    logger.info(f"[PASS] Packaged files checked. Found {len(components_files)} components: {components_files}")

    # Load and check manifest details
    with open(site_dir / "manifest.json", "r", encoding="utf-8") as f:
        manifest = DatasetManifest.model_validate_json(f.read())
    assert manifest.site_id == "site_000004", "Manifest site_id mismatch!"
    assert manifest.url == "https://example.com", "Manifest url mismatch!"
    logger.info(f"[PASS] Manifest metadata checked: site_id={manifest.site_id}, components={manifest.components_count}")

    # 3. Verify RAG semantic index
    logger.info("Verifying RAG search against ChromaDB vector index...")
    chroma = ChromaClientManager()
    generator = EmbeddingGenerator()

    query_text = "Prefect orchestrated layout pages"
    query_vector = generator.get_embedding(query_text)

    search_result = chroma.query_similarity(
        collection_name="pages",
        query_vector=query_vector,
        limit=5
    )

    logger.info(f"ChromaDB search matches count: {len(search_result.results)}")
    found = False
    for res in search_result.results:
        logger.info(f"Match: ID={res.id}, Distance={res.distance:.4f}, SiteID={res.metadata.get('site_id')}")
        if res.metadata.get("site_id") == "site_000004":
            found = True

    assert found is True, "The crawled page site_000004 was not found in ChromaDB 'pages' semantic index!"
    logger.info("[PASS] RAG semantic search query check passed.")

    logger.info("ALL PREFECT FLOW INTEGRATION CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
