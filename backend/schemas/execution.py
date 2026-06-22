from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class ExecutionBase(BaseModel):
    config: Optional[Dict[str, Any]] = None


class ExecutionCreate(ExecutionBase):
    project_id: str


class ExecutionUpdate(BaseModel):
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    finished_at: Optional[datetime] = None


class ExecutionResponse(ExecutionBase):
    id: str
    project_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    finished_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
