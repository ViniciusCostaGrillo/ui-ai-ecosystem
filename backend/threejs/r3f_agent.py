import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class R3fAgent:
    """Agent that compiles React Three Fiber Canvas and Mesh setups."""

    def generate_canvas(self, name: str) -> Dict[str, Any]:
        logger.info(f"R3fAgent: compiling canvas model component for {name}...")
        code = (
            "import React, { useRef } from 'react';\n"
            "import { Canvas, useFrame } from '@react-three/fiber';\n"
            "import { OrbitControls } from '@react-three/drei';\n\n"
            "function Box(props) {\n"
            "  const ref = useRef();\n"
            "  useFrame((state, delta) => (ref.current.rotation.x += delta));\n"
            "  return (\n"
            "    <mesh {...props} ref={ref}>\n"
            "      <boxGeometry args={[1, 1, 1]} />\n"
            "      <meshStandardMaterial color='hotpink' />\n"
            "    </mesh>\n"
            "  );\n"
            "}\n\n"
            f"export default function {name}Canvas() {{\n"
            "  return (\n"
            "    <Canvas>\n"
            "      <ambientLight />\n"
            "      <pointLight position={[10, 10, 10]} />\n"
            "      <Box position={[-1.2, 0, 0]} />\n"
            "      <OrbitControls />\n"
            "    </Canvas>\n"
            "  );\n"
            "}"
        )
        return {
            "library": "@react-three/fiber",
            "code": code,
            "component_name": f"{name}Canvas",
        }
