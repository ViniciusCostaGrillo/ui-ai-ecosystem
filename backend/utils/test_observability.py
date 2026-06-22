import asyncio
import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient

from backend.api.main import app
from backend.database.models import Log
from backend.database.session import Base, SessionLocal, engine
from backend.utils.custom_logger import setup_logger
from backend.utils.retries import retry_on_failure

logger = setup_logger("utils.test_observability")

# Ensure SQLite test tables are created locally
Base.metadata.create_all(bind=engine)


def test_retry_on_failure() -> None:
    logger.info("Testing retry_on_failure decorator...")

    # 1. Sync function retry test
    sync_attempts = 0

    @retry_on_failure(
        max_retries=3,
        initial_delay=0.01,
        backoff_factor=1.5,
        exceptions=(ValueError,),
    )
    def fail_sync() -> str:
        nonlocal sync_attempts
        sync_attempts += 1
        if sync_attempts < 3:
            raise ValueError("Transient sync error")
        return "success_sync"

    result = fail_sync()
    assert result == "success_sync"
    assert sync_attempts == 3
    logger.info("[PASS] Sync function retry test passed.")

    # 2. Async function retry test
    async_attempts = 0

    @retry_on_failure(
        max_retries=3,
        initial_delay=0.01,
        backoff_factor=1.5,
        exceptions=(ValueError,),
    )
    async def fail_async() -> str:
        nonlocal async_attempts
        async_attempts += 1
        if async_attempts < 3:
            raise ValueError("Transient async error")
        return "success_async"

    result_async = asyncio.run(fail_async())
    assert result_async == "success_async"
    assert async_attempts == 3
    logger.info("[PASS] Async function retry test passed.")


def test_database_logging_handler() -> None:
    logger.info("Testing DatabaseLoggingHandler integration...")

    test_logger = setup_logger("test_observability_db_logger")
    test_message = "Test observability database logging message - unique token 123"

    # Log the message with extra attributes
    test_logger.info(
        test_message,
        extra={"execution_id": "test-execution-uuid", "job_id": "test-job-uuid"},
    )

    # Query database to check if the message was written
    db = SessionLocal()
    try:
        inserted_log = (
            db.query(Log).filter(Log.message.contains("unique token 123")).first()
        )
        assert inserted_log is not None, "Log message was not found in the database!"
        assert inserted_log.level == "INFO"
        assert inserted_log.execution_id == "test-execution-uuid"
        assert inserted_log.job_id == "test-job-uuid"
        logger.info(
            f"[PASS] Found log record in DB: ID={inserted_log.id}, level={inserted_log.level}"
        )
    finally:
        db.close()


def test_http_tracing_middleware() -> None:
    logger.info("Testing TracingMiddleware via TestClient...")

    client = TestClient(app)
    response = client.get("/projects/")  # Call projects endpoint to test tracking

    assert response.status_code == 200
    assert (
        "X-Request-ID" in response.headers
    ), "X-Request-ID header missing from response!"
    request_id = response.headers["X-Request-ID"]
    logger.info(f"[PASS] Request trace successfully tracked with ID: {request_id}")


def test_health_check_endpoint() -> None:
    logger.info("Testing detailed system /health endpoint...")

    client = TestClient(app)
    response = client.get("/health/")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "redis" in data
    assert "chromadb" in data

    logger.info(f"[PASS] /health response payload: {data}")


def main() -> None:
    logger.info("------------- Observability Orchestration Tests -------------")
    try:
        test_retry_on_failure()
        test_database_logging_handler()
        test_http_tracing_middleware()
        test_health_check_endpoint()
        logger.info("ALL OBSERVABILITY VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    except Exception as e:
        logger.error(f"Observability verification check failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
