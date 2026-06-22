from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CrawlerHistoryBase(BaseModel):
    url: str
    status_code: Optional[int] = None


class CrawlerHistoryCreate(CrawlerHistoryBase):
    dataset_id: Optional[str] = None


class CrawlerHistoryResponse(CrawlerHistoryBase):
    id: int
    dataset_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
