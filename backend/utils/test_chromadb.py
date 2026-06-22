import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.database.chroma_client import ChromaClientManager
from backend.rag.embeddings import EmbeddingGenerator
from backend.schemas.embeddings import EcosystemEmbeddings
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_chromadb")


def run_tests() -> None:
    logger.info("Initializing ChromaDB Test Harness...")

    # Define paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    site_dir = base_dir / "dataset" / "site_000001"
    embeddings_path = site_dir / "embeddings.json"

    if not embeddings_path.exists():
        logger.error(f"Embeddings index file not found at: {embeddings_path}")
        sys.exit(1)

    # 1. Load packaged vectors
    logger.info("Loading pre-calculated embeddings...")
    try:
        with open(embeddings_path, "r", encoding="utf-8") as f:
            ecosystem_embs = EcosystemEmbeddings.model_validate_json(f.read())
        logger.info("[PASS] Embeddings models loaded.")
    except Exception as e:
        logger.error(f"Failed to load embeddings JSON: {e}")
        sys.exit(1)

    # 2. Instantiate Chroma client
    chroma = ChromaClientManager()

    # Reset previous index if possible
    try:
        chroma.reset()
        logger.info("Database collections reset successfully.")
    except Exception as e:
        logger.debug(f"Client reset skipped or not supported: {e}")

    # 3. Index page vector
    logger.info("Indexing page vectors into ChromaDB...")
    chroma.upsert(
        collection_name="pages",
        doc_id="site_000001",
        vector=ecosystem_embs.page.page_vector,
        document=ecosystem_embs.page.text_source,
        metadata={"url": "https://example.com", "site_id": "site_000001"},
    )

    # 4. Index style vector
    logger.info("Indexing style visual tokens into ChromaDB...")
    chroma.upsert(
        collection_name="styles",
        doc_id="site_000001",
        vector=ecosystem_embs.style.vector,
        document=ecosystem_embs.style.text_source,
        metadata={"site_id": "site_000001"},
    )

    # 5. Index components vectors
    logger.info("Indexing component layouts into ChromaDB...")
    for comp in ecosystem_embs.components:
        doc_id = f"site_000001_{comp.component_id}"
        chroma.upsert(
            collection_name="components",
            doc_id=doc_id,
            vector=comp.vector,
            document=comp.text_source,
            metadata={"site_id": "site_000001", "component_id": comp.component_id},
        )

    # 6. Test semantic queries
    logger.info("Setting up SentenceTransformers query encoder...")
    generator = EmbeddingGenerator()

    # Query 1: Search Pages
    query_text_page = "documentation layout about document guides"
    logger.info(f"Querying 'pages' collection with query: '{query_text_page}'")
    query_vector_page = generator.get_embedding(query_text_page)
    
    page_results = chroma.query_similarity(
        collection_name="pages", query_vector=query_vector_page, limit=1
    )

    # Query 2: Search Components
    query_text_comp = "Explore more React action buttons"
    logger.info(f"Querying 'components' collection with query: '{query_text_comp}'")
    query_vector_comp = generator.get_embedding(query_text_comp)
    
    comp_results = chroma.query_similarity(
        collection_name="components", query_vector=query_vector_comp, limit=1
    )

    # Output verification details
    logger.info("------------- Verification Results -------------")
    logger.info(f"Page query matches count: {len(page_results.results)}")
    if page_results.results:
        item = page_results.results[0]
        logger.info(f"Page match: ID={item.id}, Distance={item.distance:.4f}, SiteID={item.metadata.get('site_id')}")

    logger.info(f"Component query matches count: {len(comp_results.results)}")
    if comp_results.results:
        item = comp_results.results[0]
        logger.info(f"Component match: ID={item.id}, Distance={item.distance:.4f}, CompID={item.metadata.get('component_id')}")

    # Assertions
    logger.info("Running validation checks...")
    assert len(page_results.results) > 0, "No page query matches returned!"
    assert page_results.results[0].id == "site_000001", "Page query ID mismatch!"
    assert page_results.results[0].metadata.get("site_id") == "site_000001", "Page query metadata mismatch!"

    assert len(comp_results.results) > 0, "No component query matches returned!"
    assert comp_results.results[0].metadata.get("site_id") == "site_000001", "Component query metadata mismatch!"
    
    logger.info("[PASS] Semantic search query retrieval assertions passed.")
    logger.info("ALL CHROMADB CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
