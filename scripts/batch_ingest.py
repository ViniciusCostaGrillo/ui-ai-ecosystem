import os
import sys
import logging

# Ensure parent path is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.knowledge.knowledge_builder import KnowledgeBuilderAgent
from backend.knowledge.knowledge_registry import KnowledgeRegistry

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_ingest")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    watch_dir = os.path.join(base_dir, "knowledge_input")
    
    if not os.path.exists(watch_dir):
        logger.error(f"Watch directory {watch_dir} does not exist.")
        sys.exit(1)
        
    builder = KnowledgeBuilderAgent()
    registry = KnowledgeRegistry()
    
    logger.info(f"Scanning directory for ingestion: {watch_dir}")
    
    count_success = 0
    count_failed = 0
    count_skipped = 0
    
    for root, _, files in os.walk(watch_dir):
        for file_name in files:
            # Skip helper files or hidden files
            if file_name.startswith(".") or file_name == ".gitkeep":
                continue

            file_path = os.path.join(root, file_name)
            try:
                file_hash = builder.generate_hash(file_path)
                norm_path = os.path.relpath(file_path, base_dir).replace("\\", "/")

                # If not processed or hash mismatched, ingest
                if not registry.is_file_processed(norm_path, file_hash):
                    logger.info(f"Ingesting changed/new file: {norm_path}")
                    result = builder.ingest_file(file_path)
                    
                    # Update registry
                    registry.register_file(norm_path, file_hash, status="success")
                    count_success += 1
                else:
                    count_skipped += 1
            except Exception as e:
                logger.error(f"Failed to process file '{file_name}': {e}")
                count_failed += 1
                try:
                    norm_path = os.path.relpath(file_path, base_dir).replace("\\", "/")
                    registry.register_file(norm_path, "", status=f"failed: {str(e)}")
                except Exception:
                    pass

    logger.info(f"Ingestion completed. Success: {count_success}, Skipped (already up to date): {count_skipped}, Failed: {count_failed}")

if __name__ == "__main__":
    main()
