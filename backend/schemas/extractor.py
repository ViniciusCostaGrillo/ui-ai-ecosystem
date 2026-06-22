from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class PageMetadata(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    og_properties: Dict[str, str] = {}


class SemanticElement(BaseModel):
    tag: str
    text: Optional[str] = None
    attributes: Dict[str, str] = {}
    children: List["SemanticElement"] = []

    model_config = ConfigDict(from_attributes=True)


class ExtractedStyles(BaseModel):
    colors: List[str] = []
    fonts: List[str] = []
    layout_rules: Dict[str, Any] = {}
    class_list: List[str] = []


class ExtractionResult(BaseModel):
    metadata: PageMetadata
    elements: List[SemanticElement]
    styles: ExtractedStyles
    clean_text: str

    model_config = ConfigDict(from_attributes=True)


# Rebuild the recursive model registry for Pydantic v2
SemanticElement.model_rebuild()
