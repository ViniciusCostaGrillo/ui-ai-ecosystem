from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from backend.designer.visual_planning_engine import VisualPlanningEngine
from backend.schemas.designer import VisualPlan
from backend.utils.custom_logger import setup_logger

logger = setup_logger("api.routers.designer")
router = APIRouter(prefix="/designer", tags=["Designer Intelligence Engine"])


class PlanRequest(BaseModel):
    prompt: str = Field(..., description="The user's prompt text detailing their layout intention.")


@router.post("/plan", response_model=VisualPlan, status_code=status.HTTP_200_OK)
def compile_design_plan(request: PlanRequest) -> VisualPlan:
    """Executes the visual planning agent pipeline to determine layout block orders,

    typographies, spacing rules, and GSAP choices before code generation.
    """
    logger.info(f"Received request to compile design plan for prompt: '{request.prompt}'")
    planner = VisualPlanningEngine()
    plan = planner.plan(request.prompt)
    return plan
