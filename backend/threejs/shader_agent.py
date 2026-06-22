import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ShaderAgent:
    """Agent that designs GLSL vertex/fragment custom shaders configurations."""

    def generate_shader(self, shader_name: str) -> Dict[str, Any]:
        logger.info(f"ShaderAgent: compiling custom WebGL shaders for {shader_name}...")

        # Vertex shader
        vertex_shader = (
            "varying vec2 vUv;\n"
            "void main() {\n"
            "  vUv = uv;\n"
            "  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);\n"
            "}"
        )

        # Fragment shader
        fragment_shader = (
            "uniform float uTime;\n"
            "varying vec2 vUv;\n"
            "void main() {\n"
            "  vec2 uv = vUv;\n"
            "  vec3 color = 0.5 + 0.5 * cos(uTime + uv.xyx + vec3(0, 2, 4));\n"
            "  gl_FragColor = vec4(color, 1.0);\n"
            "}"
        )

        return {
            "name": shader_name,
            "vertex_shader": vertex_shader,
            "fragment_shader": fragment_shader,
            "uniforms": {"uTime": {"type": "f", "value": 0.0}},
        }
