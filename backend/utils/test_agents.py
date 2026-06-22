import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.schemas.agents import AgentRunContext
from backend.agents.langgraph_agent import LangGraphAgent
from backend.agents.pydantic_ai_agent import PydanticAIAgent
from backend.agents.agno_agent import AgnoAgent
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_agents")


def run_tests() -> None:
    logger.info("Initializing Multi-Agent Frameworks Scaffolding Test Harness...")

    # Set up a mock AgentRunContext
    context = AgentRunContext(
        html_content="<div class='container'><button class='btn btn-primary'>Click me</button></div>",
        css_content=".btn-primary { background-color: #007bff; }",
        screenshot_path="mock/screenshot.png",
        target_framework="React",
        metadata={"project_id": "test_proj_99"}
    )
    logger.info("Created mock AgentRunContext successfully.")

    # 1. Test LangGraph Pipeline
    logger.info("Running LangGraph Agent workflow validation...")
    try:
        langgraph_pipeline = LangGraphAgent()
        lg_result = langgraph_pipeline.run(context)
        
        logger.info("Evaluating LangGraph results...")
        logger.info(f"LangGraph success status: {lg_result.success}")
        logger.info(f"LangGraph execution status: {lg_result.status}")
        logger.info(f"LangGraph messages counts: {len(lg_result.messages)}")
        
        # Verify result contains messages from nodes
        assert lg_result.success is True, "LangGraph execution failed"
        assert len(lg_result.messages) >= 7, "LangGraph pipeline did not run all nodes (expected at least 7 messages)"
        assert "crawler_data" in lg_result.output_data, "LangGraph crawler data missing from output"
        assert "rag_data" in lg_result.output_data, "LangGraph RAG data missing from output"
        logger.info("[PASS] LangGraph Pipeline assertions passed.")
    except Exception as e:
        logger.error(f"LangGraph validation failed with exception: {e}")
        sys.exit(1)

    # 2. Test PydanticAI Agent
    logger.info("Running PydanticAI Agent validation...")
    try:
        pydantic_ai_agent = PydanticAIAgent()
        pai_result = pydantic_ai_agent.run(context)

        logger.info("Evaluating PydanticAI results...")
        logger.info(f"PydanticAI success status: {pai_result.success}")
        logger.info(f"PydanticAI execution status: {pai_result.status}")
        logger.info(f"PydanticAI messages counts: {len(pai_result.messages)}")

        assert pai_result.success is True, "PydanticAI agent execution failed"
        assert len(pai_result.messages) > 0, "PydanticAI agent did not record any messages"
        assert "validation_status" in pai_result.output_data, "PydanticAI validation output missing"
        logger.info("[PASS] PydanticAI Agent assertions passed.")
    except Exception as e:
        logger.error(f"PydanticAI validation failed with exception: {e}")
        sys.exit(1)

    # 3. Test Agno Agent
    logger.info("Running Agno Assistant Agent validation...")
    try:
        agno_agent = AgnoAgent()
        agno_result = agno_agent.run(context)

        logger.info("Evaluating Agno Assistant results...")
        logger.info(f"Agno success status: {agno_result.success}")
        logger.info(f"Agno execution status: {agno_result.status}")
        logger.info(f"Agno messages counts: {len(agno_result.messages)}")

        assert agno_result.success is True, "Agno agent execution failed"
        assert len(agno_result.messages) > 0, "Agno agent did not record any messages"
        assert "tool_execution" in agno_result.output_data, "Agno tool execution indicator missing"
        logger.info("[PASS] Agno Assistant Agent assertions passed.")
    except Exception as e:
        logger.error(f"Agno validation failed with exception: {e}")
        sys.exit(1)

    logger.info("ALL MULTI-AGENT FRAMEWORK CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
