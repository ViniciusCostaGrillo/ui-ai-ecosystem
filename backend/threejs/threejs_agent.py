import logging
from typing import Any, Dict

from backend.threejs.particles_agent import ParticlesAgent
from backend.threejs.r3f_agent import R3fAgent
from backend.threejs.shader_agent import ShaderAgent

logger = logging.getLogger(__name__)


class ThreejsAgent:
    """Orchestrator for the ThreeJS / 3D Render Engine cluster."""

    def __init__(self) -> None:
        self.r3f = R3fAgent()
        self.shader = ShaderAgent()
        self.particles = ParticlesAgent()

    def generate_3d_suite(self, name: str) -> Dict[str, Any]:
        logger.info(f"ThreejsAgent: compiling full 3D suite for name={name}...")
        return {
            "canvas": self.r3f.generate_canvas(name),
            "shader": self.shader.generate_shader(name),
            "particles": self.particles.generate_particles(1000),
        }
