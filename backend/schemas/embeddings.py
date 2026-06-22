from typing import List
from pydantic import BaseModel, Field


class PageEmbedding(BaseModel):
    page_vector: List[float] = Field(
        ..., description="384-dimensional dense float vector representation of page layout and text content"
    )
    text_source: str = Field(
        ..., description="Raw text string used to generate page embedding"
    )


class ComponentEmbedding(BaseModel):
    component_id: str = Field(
        ..., description="Identifier of the component"
    )
    vector: List[float] = Field(
        ..., description="384-dimensional dense float vector representing React components logic"
    )
    text_source: str = Field(
        ..., description="Raw component description and code string used to generate embedding"
    )


class StyleEmbedding(BaseModel):
    vector: List[float] = Field(
        ..., description="384-dimensional dense float vector representing visual theme tokens"
    )
    text_source: str = Field(
        ..., description="Theme tokens string representation used to generate style embedding"
    )


class EcosystemEmbeddings(BaseModel):
    page: PageEmbedding = Field(
        ..., description="Semantic page content embeddings details"
    )
    components: List[ComponentEmbedding] = Field(
        default_factory=list, description="Embeddings list of each React UI component code"
    )
    style: StyleEmbedding = Field(
        ..., description="Visual styling and color palette design tokens embedding details"
    )
