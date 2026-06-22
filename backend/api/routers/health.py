from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database.chroma_client import ChromaClientManager
from backend.database.redis_client import RedisClientManager
from backend.database.session import get_db
from backend.utils.custom_logger import setup_logger

logger = setup_logger("api.routers.health")
router = APIRouter(prefix="/health", tags=["health"])


class ComponentStatus(BaseModel):
    status: str
    details: str


class SystemHealthResponse(BaseModel):
    status: str
    database: ComponentStatus
    redis: ComponentStatus
    chromadb: ComponentStatus


@router.get("/", response_model=SystemHealthResponse, status_code=status.HTTP_200_OK)
def get_health(db: Session = Depends(get_db)):
    logger.info("Performing system health check audits...")

    # 1. Database Check
    database_status = "healthy"
    database_details = "Connection successful"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        database_status = "unhealthy"
        database_details = str(e)
        logger.error(f"Database health check failed: {e}")

    # 2. Redis Check
    redis_status = "healthy"
    redis_details = "Ping successful"
    try:
        redis_manager = RedisClientManager()
        client = redis_manager.get_client()
        if not client.ping():
            raise Exception("Ping returned False")

        # Handle MockRedis info
        from backend.database.redis_client import MockRedis
        if isinstance(client, MockRedis):
            redis_details = "Ping successful (MockRedis Fallback)"
    except Exception as e:
        redis_status = "unhealthy"
        redis_details = str(e)
        logger.error(f"Redis health check failed: {e}")

    # 3. ChromaDB Check
    chromadb_status = "healthy"
    chromadb_details = "Connection successful"
    try:
        chroma_manager = ChromaClientManager()
        collections = chroma_manager.client.list_collections()
        chromadb_details = f"Connected. Collections: {len(collections)}"

        # Identify client type
        import chromadb
        client_class = type(chroma_manager.client)
        is_persistent = False
        if hasattr(chromadb, "PersistentClient") and isinstance(chromadb.PersistentClient, type):
            is_persistent = isinstance(chroma_manager.client, chromadb.PersistentClient)
        else:
            is_persistent = "Persistent" in client_class.__name__ or "Segment" in client_class.__name__

        if is_persistent:
            chromadb_details += " (PersistentClient Fallback)"

    except Exception as e:
        chromadb_status = "unhealthy"
        chromadb_details = str(e)
        logger.error(f"ChromaDB health check failed: {e}")

    # Determine overall status
    overall_status = "healthy"
    if database_status == "unhealthy" or redis_status == "unhealthy" or chromadb_status == "unhealthy":
        overall_status = "unhealthy"

    return SystemHealthResponse(
        status=overall_status,
        database=ComponentStatus(status=database_status, details=database_details),
        redis=ComponentStatus(status=redis_status, details=redis_details),
        chromadb=ComponentStatus(status=chromadb_status, details=chromadb_details),
    )
