from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LogBase(BaseModel):
    message: str
    level: str = "INFO"


class LogCreate(LogBase):
    execution_id: Optional[str] = None
    job_id: Optional[str] = None


class LogResponse(LogBase):
    id: int
    execution_id: Optional[str] = None
    job_id: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
