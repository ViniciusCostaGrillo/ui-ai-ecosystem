from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TrainingHistoryBase(BaseModel):
    model_name: str
    base_model: str
    dataset_path: str
    epochs: int = 1


class TrainingHistoryCreate(TrainingHistoryBase):
    pass


class TrainingHistoryUpdate(BaseModel):
    loss: Optional[float] = None
    status: Optional[str] = None


class TrainingHistoryResponse(TrainingHistoryBase):
    id: str
    loss: Optional[float] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
