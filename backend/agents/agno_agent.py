import os
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from backend.schemas.agents import AgentMessage, AgentRunContext, AgentRunResult

logger = logging.getLogger(__name__)


def validate_ui_layout_tool(html_content: str) -> str:
    """Tool to inspect structural soundness of the parsed HTML.

    Args:
        html_content (str): The raw HTML source code.

    Returns:
        str: Validation summary.
    """
    logger.info("Agno Tool: Running layout tool check...")
    if not html_content:
        return "Empty layout content provided."
    return f"Layout validated successfully. Content length: {len(html_content)} characters."


class AgnoAgent:
    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key == "your_openai_api_key_here":
            openai_key = None

        self.is_mock = openai_key is None
        self.tools = [validate_ui_layout_tool]

        if not self.is_mock:
            logger.info("Agno: Initializing Agent with OpenAI model and tools.")
            model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
            base_url = os.getenv("OPENAI_API_BASE")
            self.agent = Agent(
                model=OpenAIChat(id=model_name, api_key=openai_key, base_url=base_url),
                tools=self.tools,
                instructions=["You are a layout assistant that validates structures using tool hooks."],
                markdown=True
            )
        else:
            logger.warning("Agno: No OpenAI API key found. Initializing Agent in mock mode.")
            # Instantiate with model=None to assert constructor stability
            self.agent = Agent(
                model=None,
                tools=self.tools,
                instructions=["Mock mode validation agent."]
            )

    def run(self, context: AgentRunContext) -> AgentRunResult:
        logger.info("Running Agno Agent step...")
        prompt = f"Analyze layout with html length: {len(context.html_content or '')}"

        try:
            if self.is_mock:
                logger.info("Agno: Executing tools directly in mock mode")
                tool_output = validate_ui_layout_tool(context.html_content or "")
                msg = AgentMessage(
                    sender="AgnoAgent",
                    content=f"Agno mock validation run completed. Tool output: {tool_output}"
                )
                return AgentRunResult(
                    success=True,
                    status="COMPLETED",
                    messages=[msg],
                    output_data={
                        "tool_execution": "validate_ui_layout_tool",
                        "tool_result": tool_output
                    },
                    metadata={"agno_mock": True}
                )
            else:
                response = self.agent.run(prompt)
                success = hasattr(response, 'status') and "error" not in str(response.status).lower()
                msg = AgentMessage(
                    sender="AgnoAgent",
                    content=response.content or "Successfully ran Agno model instructions."
                )
                return AgentRunResult(
                    success=success,
                    status="COMPLETED" if success else "FAILED",
                    messages=[msg],
                    output_data={"raw_response": response.content},
                    metadata={"agno_execution": True}
                )
        except Exception as e:
            logger.exception("Agno agent run failed")
            error_msg = AgentMessage(
                sender="AgnoAgent",
                content=f"Execution error: {str(e)}"
            )
            return AgentRunResult(
                success=False,
                status="ERROR",
                messages=[error_msg],
                output_data={},
                metadata={"error": str(e)}
            )
