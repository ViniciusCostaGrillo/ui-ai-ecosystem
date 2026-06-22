from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentMessage(BaseModel):
    sender: str = Field(..., description="Name or identifier of the agent/source that created this message")
    content: str = Field(..., description="Text content or structured logs from the agent execution")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO 8601 formatted timestamp when the message was recorded"
    )


class AgentRunContext(BaseModel):
    html_content: Optional[str] = Field(None, description="Optional raw HTML layout from the crawl stage")
    css_content: Optional[str] = Field(None, description="Optional styling specifications or profiles")
    screenshot_path: Optional[str] = Field(None, description="Optional file path to visual guides or layouts")
    target_framework: str = Field("React", description="Target component framework (e.g., React, Vue, HTML/CSS)")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary execution context metadata"
    )


class AgentRunResult(BaseModel):
    success: bool = Field(..., description="Indicates whether the agent run completed successfully")
    status: str = Field(..., description="Short status description (e.g., COMPLETED, FAILED, RUNNING)")
    messages: List[AgentMessage] = Field(
        default_factory=list, description="Audit log of agent communications and steps"
    )
    output_data: Dict[str, Any] = Field(
        default_factory=dict, description="Generated structures, code, or profile outputs"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional tracing or performance diagnostics"
    )
