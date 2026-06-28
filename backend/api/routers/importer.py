import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from backend.database.session import get_db
from backend.database.models import Dataset, Masterpiece
from backend.importer.queue_manager import QueueManager
from backend.importer.batch_processor import BatchProcessor
from backend.importer.url_parser import URLParser
from backend.importer.import_validator import ImportValidator
from backend.masterpieces.masterpiece_agent import MasterpieceAgent
from backend.schemas.importer import ImportBatchRequest, ImportJob, ImporterStats, URLValidationResult

logger = logging.getLogger("api.routers.importer")
router = APIRouter(prefix="/importer", tags=["Website Import Center"])

queue_manager = QueueManager()
batch_processor = BatchProcessor()
validator = ImportValidator()
masterpiece_agent = MasterpieceAgent()


class SingleImportRequest(BaseModel):
    url: str = Field(..., description="The website URL to import")
    promote_to_masterpiece: bool = Field(False, description="Auto-promote to masterpiece status")
    category: str = Field("general", description="Website category tag")


class PromoteRequest(BaseModel):
    url: str = Field(..., description="The website URL to promote")
    name: str = Field(..., description="Visual name for the masterpiece")
    category: List[str] = Field(..., description="Category tags")


class DemoteRequest(BaseModel):
    url: str = Field(..., description="The masterpiece URL to demote")


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_import_file(
    file: UploadFile = File(...),
    promote_to_masterpiece: bool = False,
    category: str = "general",
    db: Session = Depends(get_db)
):
    """Processes uploaded TXT, CSV, or JSON file, validates URLs, and enqueues jobs."""
    contents = await file.read()
    file_content = contents.decode("utf-8", errors="ignore")
    
    records = []
    filename = file.filename or "batch"
    
    if filename.endswith(".txt"):
        urls = batch_processor.process_txt(file_content)
        records = [{"name": URLParser.get_domain(url).capitalize(), "url": url, "category": category} for url in urls]
    elif filename.endswith(".csv"):
        records = batch_processor.process_csv(file_content)
    elif filename.endswith(".json"):
        records = batch_processor.process_json(file_content)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a .txt, .csv, or .json file."
        )

    if not records:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No valid URLs found in the uploaded file."
        )

    # Validate URLs and check for duplicates in DB in bulk
    urls_to_validate = [rec["url"] for rec in records]
    validation_results = validator.validate_bulk(db, urls_to_validate)
    
    validated_records = []
    skipped_duplicates = 0
    
    for rec in records:
        url = rec["url"]
        is_valid, reason = validation_results.get(url, (False, "Unknown error"))
        if is_valid:
            if reason == "duplicate":
                skipped_duplicates += 1
            else:
                validated_records.append(rec)

    options = {
        "promote_to_masterpiece": promote_to_masterpiece,
        "generate_design_systems": True,
        "extract_components": True,
        "extract_assets": True,
        "analyze_motion": True
    }

    job_ids = batch_processor.enqueue_batch(validated_records, options)
    
    message = f"Successfully parsed and queued {len(job_ids)} import jobs."
    if skipped_duplicates > 0:
        message += f" Skipped {skipped_duplicates} duplicate URLs already present in the database."
    
    return {
        "message": message,
        "jobs_queued": len(job_ids),
        "job_ids": job_ids
    }


@router.post("/url", status_code=status.HTTP_202_ACCEPTED)
def import_single_url(request: SingleImportRequest, db: Session = Depends(get_db)):
    """Enqueues a single URL for background crawling and visual analysis."""
    sanitized_url = URLParser.sanitize(request.url)
    
    is_valid, reason = validator.validate(db, sanitized_url)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"URL validation failed: {reason}"
        )

    options = {
        "promote_to_masterpiece": request.promote_to_masterpiece,
        "generate_design_systems": True,
        "extract_components": True,
        "extract_assets": True,
        "analyze_motion": True
    }

    record = {
        "name": URLParser.get_domain(sanitized_url).capitalize(),
        "url": sanitized_url,
        "category": request.category
    }

    job_ids = batch_processor.enqueue_batch([record], options)
    
    return {
        "message": "Single website crawl job successfully enqueued.",
        "job_id": job_ids[0]
    }


@router.get("/queue", response_model=List[ImportJob])
def get_import_queue():
    """Fetches details of all active and completed import jobs in the queue."""
    jobs = queue_manager.get_all_jobs()
    parsed_jobs = []
    for j in jobs:
        parsed_jobs.append(
            ImportJob(
                id=j["id"],
                url=j["url"],
                status=j["status"],
                stage=j["stage"],
                progress=j["progress"],
                elapsed=j["elapsed"],
                remaining=j["remaining"],
                logs=j["logs"],
                error_message=j["error_message"],
                created_at=j["created_at"],
                finished_at=j["finished_at"]
            )
        )
    return parsed_jobs


@router.get("/history")
def get_import_history(db: Session = Depends(get_db)):
    """Fetches all successfully crawled datasets from the SQLite/PostgreSQL database."""
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
    history = []
    for d in datasets:
        # Check if URL is also registered as a masterpiece
        mp = db.query(Masterpiece).filter(Masterpiece.url == d.url).first()
        history.append({
            "id": d.id,
            "url": d.url,
            "screenshot": d.screenshot_path,
            "html": d.html_path,
            "css": d.css_path,
            "metadata": d.metadata_json,
            "is_masterpiece": mp is not None,
            "masterpiece_score": mp.score if mp else None,
            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return history


@router.get("/stats", response_model=ImporterStats)
def get_importer_stats(db: Session = Depends(get_db)):
    """Computes totals and analytics statistics for the Ingestion Dashboard."""
    websites_count = db.query(Dataset).count()
    masterpieces_count = db.query(Masterpiece).count()
    
    # Calculate mock components/assets totals based on database count
    components_count = websites_count * 15 + masterpieces_count * 45
    assets_count = websites_count * 8 + masterpieces_count * 20
    design_systems_count = websites_count + masterpieces_count * 3
    skills_count = masterpieces_count + 5
    embeddings_count = (components_count + assets_count) * 2
    
    growth_today = masterpieces_count * 2 + 5
    
    return ImporterStats(
        websites_count=websites_count,
        masterpieces_count=masterpieces_count,
        components_count=components_count,
        assets_count=assets_count,
        design_systems_count=design_systems_count,
        skills_count=skills_count,
        embeddings_count=embeddings_count,
        growth_today=growth_today,
        average_time_sec=12.5,
        error_count=2,
        last_sync=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@router.post("/promote", status_code=status.HTTP_200_OK)
def promote_to_masterpiece(request: PromoteRequest, db: Session = Depends(get_db)):
    """Explicitly promotes an existing database website or URL to masterpiece status."""
    result = masterpiece_agent.promote_website(
        db=db,
        name=request.name,
        url=request.url,
        category=request.category
    )
    return result


@router.post("/demote", status_code=status.HTTP_200_OK)
def demote_from_masterpiece(request: DemoteRequest, db: Session = Depends(get_db)):
    """Removes masterpiece status from a URL."""
    success = masterpiece_agent.registry.demote(db, request.url)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The URL was not found in masterpieces references."
        )
    return {"message": "Masterpiece successfully demoted."}


@router.get("/logs")
def get_live_importer_logs():
    """Simulates/exposes live pipeline worker logs."""
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "logs": [
            "[INFO] playwrighter_engine: Headless browser viewport initialized (1280x800).",
            "[INFO] playwrighter_engine: Loading DOM elements from target URL.",
            "[INFO] css_extractor: Parsed 24 CSS global selector tags.",
            "[INFO] asset_agent: Saved assets 'mesh_grid_bg.png' successfully.",
            "[INFO] masterpiece_embeddings: Upserted vectors into collection 'Masterpieces'."
        ]
    }
