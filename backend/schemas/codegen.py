from typing import List, Optional
from pydantic import BaseModel, Field


class GeneratedComponent(BaseModel):
    name: str = Field(
        ..., description="Name of the React component class (e.g. Header, HeroSection, FeatureGrid)"
    )
    code: str = Field(
        ..., description="Complete self-contained React TSX component code using Tailwind utilities"
    )
    description: str = Field(
        ..., description="Explanation of what layout features this component represents"
    )


class CodegenResult(BaseModel):
    components: List[GeneratedComponent] = Field(
        default_factory=list, description="List of React components generated for the layout"
    )
    global_styles: Optional[str] = Field(
        None, description="Global Tailwind or custom styling directives needed for these components"
    )
