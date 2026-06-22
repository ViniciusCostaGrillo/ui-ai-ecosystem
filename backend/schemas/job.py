from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    name: str


class JobCreate(JobBase):
    execution_id: str


class JobUpdate(BaseModel):
    status: Optional[str] = None


class JobResponse(JobBase):
    id: str
    execution_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
