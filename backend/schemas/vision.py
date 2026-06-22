from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ColorPalette(BaseModel):
    dominant_colors: List[str] = Field(
        default_factory=list, description="Top dominant color hex codes (e.g. #ffffff)"
    )
    background_color: Optional[str] = Field(
        None, description="Inferred primary background color hex code"
    )


class GridLayout(BaseModel):
    vertical_splits: List[float] = Field(
        default_factory=list,
        description="Relative horizontal percentages (0.0 to 1.0) where vertical layout partitions exist",
    )
    horizontal_splits: List[float] = Field(
        default_factory=list,
        description="Relative vertical percentages (0.0 to 1.0) where horizontal layout partitions exist",
    )
    grid_type: str = Field(
        "single_column", description="Identified layout type (e.g., single_column, split, grid)"
    )


class SpacingMetrics(BaseModel):
    margins: Dict[str, int] = Field(
        default_factory=dict,
        description="Estimated outer margin thicknesses in pixels: top, bottom, left, right",
    )
    content_gaps: List[int] = Field(
        default_factory=list,
        description="Common whitespace spacing intervals between text and image blocks in pixels",
    )


class VisualDensity(BaseModel):
    content_percentage: float = Field(
        0.0, ge=0.0, le=100.0, description="Percentage of space occupied by active content elements"
    )
    whitespace_percentage: float = Field(
        100.0, ge=0.0, le=100.0, description="Percentage of space left as empty background padding"
    )


class VisionMetadata(BaseModel):
    colors: ColorPalette
    grid: GridLayout
    spacing: SpacingMetrics
    density: VisualDensity
