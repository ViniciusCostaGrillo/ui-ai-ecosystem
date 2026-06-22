from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class DatasetBase(BaseModel):
    url: str
    screenshot_path: Optional[str] = None
    html_path: Optional[str] = None
    css_path: Optional[str] = None
    markdown_path: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class DatasetCreate(DatasetBase):
    project_id: str


class DatasetUpdate(BaseModel):
    screenshot_path: Optional[str] = None
    html_path: Optional[str] = None
    css_path: Optional[str] = None
    markdown_path: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class DatasetResponse(DatasetBase):
    id: str
    project_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
