import logging
from typing import Dict, Any, List, TypedDict

from langgraph.graph import StateGraph, END

from backend.schemas.agents import AgentMessage, AgentRunContext, AgentRunResult

logger = logging.getLogger(__name__)


class PipelineState(TypedDict):
    messages: List[AgentMessage]
    context: AgentRunContext
    current_node: str
    outputs: Dict[str, Any]
    errors: List[str]


class LangGraphAgent:
    def __init__(self):
        self.workflow = StateGraph(PipelineState)
        self._build_graph()
        self.compiled_graph = self.workflow.compile()

    def _build_graph(self):
        # Define nodes
        self.workflow.add_node("crawler", self.crawler_node)
        self.workflow.add_node("extractor", self.extractor_node)
        self.workflow.add_node("vision", self.vision_node)
        self.workflow.add_node("style", self.style_node)
        self.workflow.add_node("code", self.code_node)
        self.workflow.add_node("dataset", self.dataset_node)
        self.workflow.add_node("rag", self.rag_node)

        # Define progression (routing)
        self.workflow.set_entry_point("crawler")
        self.workflow.add_edge("crawler", "extractor")
        self.workflow.add_edge("extractor", "vision")
        self.workflow.add_edge("vision", "style")
        self.workflow.add_edge("style", "code")
        self.workflow.add_edge("code", "dataset")
        self.workflow.add_edge("dataset", "rag")
        self.workflow.add_edge("rag", END)

    def crawler_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing crawler node")
        msg = AgentMessage(
            sender="CrawlerAgent",
            content="Scaffolded crawler execution. Checked source components."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["crawler_data"] = {"crawled_urls": ["/index.html"], "status": "success"}
        return {
            "messages": new_messages,
            "current_node": "crawler",
            "outputs": new_outputs
        }

    def extractor_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing extractor node")
        msg = AgentMessage(
            sender="ExtractorAgent",
            content="Scaffolded extractor execution. Parsed text/layouts."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["extractor_data"] = {"layout_blocks_count": 5}
        return {
            "messages": new_messages,
            "current_node": "extractor",
            "outputs": new_outputs
        }

    def vision_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing vision node")
        msg = AgentMessage(
            sender="VisionAgent",
            content="Scaffolded vision execution. Verified page layout visual segments."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["vision_data"] = {"ui_elements_detected": ["header", "button", "footer"]}
        return {
            "messages": new_messages,
            "current_node": "vision",
            "outputs": new_outputs
        }

    def style_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing style node")
        msg = AgentMessage(
            sender="StyleAgent",
            content="Scaffolded style execution. Resolved typography and color palette."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["style_data"] = {"primary_color": "#1A1A1A", "font_family": "Inter"}
        return {
            "messages": new_messages,
            "current_node": "style",
            "outputs": new_outputs
        }

    def code_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing code node")
        msg = AgentMessage(
            sender="CodeAgent",
            content="Scaffolded code generation. Created react element components."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["code_data"] = {"component_code": "const App = () => <div>Hello</div>;"}
        return {
            "messages": new_messages,
            "current_node": "code",
            "outputs": new_outputs
        }

    def dataset_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing dataset node")
        msg = AgentMessage(
            sender="DatasetAgent",
            content="Scaffolded dataset builder. Formatted component metadata package."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["dataset_data"] = {"dataset_path": "dataset/site_000001"}
        return {
            "messages": new_messages,
            "current_node": "dataset",
            "outputs": new_outputs
        }

    def rag_node(self, state: PipelineState) -> Dict[str, Any]:
        logger.info("LangGraph: executing rag node")
        msg = AgentMessage(
            sender="RagAgent",
            content="Scaffolded RAG engine node. Uploaded layouts to ChromaDB index."
        )
        new_messages = list(state.get("messages", [])) + [msg]
        new_outputs = dict(state.get("outputs", {}))
        new_outputs["rag_data"] = {"indexed_documents": 3}
        return {
            "messages": new_messages,
            "current_node": "rag",
            "outputs": new_outputs
        }

    def run(self, context: AgentRunContext) -> AgentRunResult:
        initial_state: PipelineState = {
            "messages": [],
            "context": context,
            "current_node": "entry",
            "outputs": {},
            "errors": []
        }
        try:
            final_state = self.compiled_graph.invoke(initial_state)
            # If standard dictionary is returned, extract errors
            errors = final_state.get("errors", [])
            success = len(errors) == 0
            status = "COMPLETED" if success else "FAILED"
            return AgentRunResult(
                success=success,
                status=status,
                messages=final_state.get("messages", []),
                output_data=final_state.get("outputs", {}),
                metadata={"langgraph_execution": True}
            )
        except Exception as e:
            logger.exception("Failed to run LangGraph multi-agent pipeline")
            error_msg = AgentMessage(
                sender="LangGraphEngine",
                content=f"Error executing graph pipeline: {str(e)}"
            )
            return AgentRunResult(
                success=False,
                status="ERROR",
                messages=[error_msg],
                output_data={},
                metadata={"error": str(e)}
            )
