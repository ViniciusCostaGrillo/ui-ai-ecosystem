from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MasterpieceGenerateConfig(BaseModel):
    design_system: bool = Field(True, description="Generate design_system rules")
    skills: bool = Field(True, description="Compile custom skills YAML mapping")
    assets: bool = Field(True, description="Scrape and catalogue premium assets")
    components: bool = Field(True, description="Generate React code from templates")
    animations: bool = Field(True, description="Index GSAP timelines and presets")
    dependencies: bool = Field(True, description="Index and resolve external dependency packages")
    prompt_templates: bool = Field(True, description="Compose masterpiece layout prompts")
    themes: bool = Field(True, description="Build dark/light luxury theme profiles")
    typography: bool = Field(True, description="Record typographic hierarchies")
    color_palettes: bool = Field(True, description="Record color palettes")


class MasterpieceYamlConfig(BaseModel):
    name: str = Field(..., description="Name of the masterpiece website")
    priority: str = Field("masterpiece", description="Priority level: masterpiece or golden_reference")
    category: List[str] = Field(default_factory=list, description="Associated categories (e.g. fashion, luxury, ecommerce)")
    analyze_depth: str = Field("maximum", description="Analysis depth: minimum, medium, maximum")
    generate: List[str] = Field(default_factory=list, description="Enabled extraction modules")
    weight: int = Field(10, description="RAG search priority multiplier weight (defaults to 10)")


class MasterpieceScoreBreakdown(BaseModel):
    visual_quality: float = Field(95.0, description="Visual look and feel score (out of 100)")
    typography: float = Field(92.0, description="Typography contrast and choice score")
    spacing: float = Field(90.0, description="Layout whitespace breathing score")
    motion: float = Field(94.0, description="GSAP scroll-triggers transitions score")
    components: float = Field(93.0, description="Component modularity and clean code score")
    color_harmony: float = Field(96.0, description="Color palette balance and contrast score")
    accessibility: float = Field(88.0, description="A11y compliance score")
    performance: float = Field(85.0, description="Lighthouse loading score")
    responsiveness: float = Field(92.0, description="Mobile-first layout score")


class MasterpieceInfo(BaseModel):
    id: str = Field(..., description="Unique Masterpiece ID")
    name: str = Field(..., description="Masterpiece name")
    url: str = Field(..., description="Masterpiece URL")
    category: List[str] = Field(default_factory=list, description="Categorization tags")
    score: float = Field(90.0, description="Overall masterpiece score")
    score_breakdown: Optional[MasterpieceScoreBreakdown] = Field(None, description="Granular scores breakdown")
    weight: int = Field(10, description="Priority retrieval weight")
    status: str = Field(..., description="Current status: active, analyzing")
    created_at: str = Field(..., description="Timestamp of promotion creation")
    updated_at: str = Field(..., description="Timestamp of latest modifications")
