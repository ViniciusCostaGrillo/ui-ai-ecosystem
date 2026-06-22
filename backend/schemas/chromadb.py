from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChromaQuery(BaseModel):
    query_text: str = Field(
        ..., description="Raw text string to run semantic search against"
    )
    limit: int = Field(
        5, ge=1, le=100, description="Maximum number of matched layout results to retrieve"
    )
    collection_name: str = Field(
        ..., description="Target ChromaDB collection to search (pages, components, styles)"
    )


class ChromaResultItem(BaseModel):
    id: str = Field(
        ..., description="Unique alphanumeric identifier of the matched layout block"
    )
    distance: float = Field(
        ..., description="Calculated vector distance score (smaller means higher similarity)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata dictionary associated with the matched vector"
    )
    document: Optional[str] = Field(
        None, description="The raw source code or semantic content matched by similarity"
    )


class ChromaQueryResponse(BaseModel):
    results: List[ChromaResultItem] = Field(
        default_factory=list, description="Sorted list of semantic similarity matching records"
    )
