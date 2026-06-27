from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ImportOptions(BaseModel):
    generate_design_systems: bool = Field(True, description="Extract and build design systems")
    extract_components: bool = Field(True, description="Scrape and extract visual React components")
    extract_assets: bool = Field(True, description="Download and organize assets (images, videos, 3d)")
    analyze_motion: bool = Field(True, description="Analyze and save motion/animation sequences")
    generate_skills: bool = Field(True, description="Generate system skills rules")
    generate_prompt_templates: bool = Field(True, description="Compile prompt templates")
    generate_embeddings: bool = Field(True, description="Generate vector embeddings for semantic search")
    save_to_chromadb: bool = Field(True, description="Upsert documents and vectors into ChromaDB")
    promote_to_masterpiece: bool = Field(False, description="Auto promote imported website to masterpiece status")
    rebuild_component_library: bool = Field(False, description="Rebuild component index after completion")


class ImportBatchRequest(BaseModel):
    urls: List[str] = Field(..., description="List of website URLs to import")
    options: ImportOptions = Field(default_factory=ImportOptions)
    category: Optional[str] = Field("general", description="Categorization for imports (e.g. saas, fashion)")


class ImportJob(BaseModel):
    id: str = Field(..., description="Unique job ID")
    url: str = Field(..., description="Target crawl URL")
    status: str = Field(..., description="Current status: queued, running, completed, failed")
    stage: str = Field("Playwright", description="Active pipeline stage")
    progress: int = Field(0, description="Progress percentage")
    elapsed: str = Field("00:00", description="Elapsed time")
    remaining: str = Field("00:00", description="Estimated remaining time")
    logs: List[str] = Field(default_factory=list, description="Execution logs associated with the job")
    error_message: Optional[str] = Field(None, description="Detailed error message if failed")
    created_at: str = Field(..., description="Timestamp when job was created")
    finished_at: Optional[str] = Field(None, description="Timestamp when job finished")


class ImporterStats(BaseModel):
    websites_count: int = Field(0, description="Total number of crawled websites")
    masterpieces_count: int = Field(0, description="Total number of premium masterpieces")
    components_count: int = Field(0, description="Total number of generated components")
    assets_count: int = Field(0, description="Total number of extracted assets")
    design_systems_count: int = Field(0, description="Total number of design systems configurations")
    skills_count: int = Field(0, description="Total number of compiled skills")
    embeddings_count: int = Field(0, description="Total number of vector embeddings created")
    growth_today: int = Field(0, description="Total new elements added today")
    average_time_sec: float = Field(0.0, description="Average processing time per website in seconds")
    error_count: int = Field(0, description="Total count of crawling or analysis failures")
    last_sync: str = Field(..., description="Timestamp of the last ingestion sync")


class URLValidationResult(BaseModel):
    url: str = Field(..., description="Sanitized target URL")
    is_valid: bool = Field(..., description="Validation success status")
    reason: Optional[str] = Field(None, description="Details explaining validation failure")
    is_duplicate: bool = Field(False, description="True if URL already exists in database")
    estimated_time_sec: int = Field(15, description="Estimated crawl duration")
