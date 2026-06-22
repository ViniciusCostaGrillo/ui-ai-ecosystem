import os
import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient

from backend.api.main import app
from backend.database.models import Execution, Job, Log
from backend.database.session import Base, SessionLocal
from backend.database.sharding import analytics_engine, core_engine
from backend.rag.service import RAGService
from backend.schemas.rag import RAGQueryRequest
from backend.utils.custom_logger import setup_logger
from backend.workers.queue import TaskQueue
from backend.workers.worker import BackgroundWorker

logger = setup_logger("utils.test_complete_system")

# Start with a fresh test database state
Base.metadata.drop_all(bind=core_engine)
Base.metadata.drop_all(bind=analytics_engine)
Base.metadata.create_all(bind=core_engine)
Base.metadata.create_all(bind=analytics_engine)


def test_end_to_end_generation() -> None:
    logger.info("Initializing FASE 25 Complete System Integration Test...")

    # 1. Trigger generation via FastAPI client
    client = TestClient(app)
    prompt = "I want a dark dashboard page with statistics cards and a left sidebar"
    response = client.post(
        "/generation/generate/",
        json={"project_id": "1", "prompt": prompt},
    )

    assert response.status_code == 202, f"Failed generation start: {response.text}"
    data = response.json()
    assert "execution_id" in data
    assert data["status"] == "pending"
    execution_id = data["execution_id"]
    logger.info(f"[PASS] REST API request accepted. Execution ID: {execution_id}")

    # 2. Dequeue the task and process it synchronously via worker
    t_queue = TaskQueue()
    listen_list = ["generation_tasks_high", "generation_tasks_default", "generation_tasks_low"]
    task = t_queue.dequeue(listen_list, timeout=2)

    assert task is not None, "Failed to dequeue the generated task from the queue!"
    assert task["task_type"] == "prompt_generation"
    assert task["payload"]["execution_id"] == execution_id
    logger.info("[PASS] Successfully dequeued generation task from high-priority queue.")

    # Execute worker processing
    worker = BackgroundWorker()
    worker.process_task(task)
    logger.info("[PASS] Synced background task execution complete.")

    # 3. Verify Database Execution & Job records in Core DB
    db = SessionLocal()
    try:
        execution = db.query(Execution).filter(Execution.id == execution_id).first()
        assert execution is not None
        assert execution.status == "completed"
        assert execution.project_id == "1"
        assert execution.result is not None
        assert "components_dir" in execution.result

        job = db.query(Job).filter(Job.execution_id == execution_id).first()
        assert job is not None
        assert job.status == "success"
        assert job.name == "prompt_generation"
        logger.info("[PASS] Execution and Job records updated in transactional Core DB.")
    finally:
        db.close()

    # 4. Verify vertical sharding log writes in Analytics DB
    from sqlalchemy.orm import sessionmaker
    analytics_session = sessionmaker(bind=analytics_engine)()
    try:
        logs = analytics_session.query(Log).filter(Log.execution_id == execution_id).all()
        assert len(logs) > 0, "No logs were written to the analytics database!"
        # Verify specific logs exist
        messages = [log.message for log in logs]
        assert any("Starting prompt-to-code generation pipeline" in msg for msg in messages)
        assert any("Prompt-to-code generation pipeline completed successfully" in msg for msg in messages)
        logger.info("[PASS] Logging details written thread-safely to sharded Analytics DB.")
    finally:
        analytics_session.close()

    # 5. Verify generated component files on disk
    base_dir = Path(__file__).resolve().parent.parent.parent
    project_dir = base_dir / "storage" / "projects" / "1"
    components_dir = project_dir / "components"
    assert components_dir.exists(), "Components directory was not created!"
    files = os.listdir(components_dir)
    assert len(files) > 0, "No TSX React files generated on disk!"
    logger.info(f"[PASS] Generated files found in project storage: {files}")

    # 6. Verify that the output was packaged as a dataset site item
    dataset_dir = base_dir / "dataset" / f"site_{1:06d}"
    assert dataset_dir.exists(), f"Dataset site packaging directory {dataset_dir} was not created!"
    manifest_path = dataset_dir / "manifest.json"
    assert manifest_path.exists(), "Dataset manifest index missing!"
    logger.info("[PASS] Dataset package compiled and written to local filesystem.")

    # 7. Verify the new page was indexed and is queryable in ChromaDB (Continuous Growth)
    logger.info("Verifying prompt-to-code feedback loop retrieval in ChromaDB...")
    rag = RAGService()
    search_res = rag.query(RAGQueryRequest(prompt="dark dashboard statistics sidebar", limit=1))
    
    assert len(search_res.retrieved_contexts) > 0, "No contexts retrieved from ChromaDB!"
    closest_doc = search_res.retrieved_contexts[0]
    # Check that it retrieved our newly generated site package (site_000001)
    assert str(closest_doc.id) == "site_000001", f"Expected to retrieve site_000001 from feedback loop, retrieved: {closest_doc.id}"

    logger.info(f"[PASS] ChromaDB RAG query correctly retrieved the newly indexed code: ID={closest_doc.id}, distance={closest_doc.distance:.4f}")


def main() -> None:
    logger.info("------------- Complete System Integration Tests -------------")
    try:
        test_end_to_end_generation()
        logger.info("ALL INTEGRATION VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    except Exception as e:
        logger.error(f"Complete system integration check failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
