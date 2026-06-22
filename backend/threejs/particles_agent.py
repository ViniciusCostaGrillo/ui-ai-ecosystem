import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ParticlesAgent:
    """Agent that creates physics particle structures and vertex animations layouts."""

    def generate_particles(self, count: int) -> Dict[str, Any]:
        logger.info(f"ParticlesAgent: generating layout for count={count} particles...")
        code = (
            "import { useMemo, useRef } from 'react';\n"
            "import { useFrame } from '@react-three/fiber';\n\n"
            "export function ParticleWave() {\n"
            "  const count = 2000;\n"
            "  const pointsRef = useRef();\n"
            "  const positions = useMemo(() => {\n"
            "    const pos = new Float32Array(count * 3);\n"
            "    for (let i = 0; i < count; i++) {\n"
            "      pos[i * 3] = (Math.random() - 0.5) * 10;\n"
            "      pos[i * 3 + 1] = (Math.random() - 0.5) * 10;\n"
            "      pos[i * 3 + 2] = (Math.random() - 0.5) * 10;\n"
            "    }\n"
            "    return pos;\n"
            "  }, []);\n\n"
            "  useFrame((state) => {\n"
            "    const time = state.clock.getElapsedTime();\n"
            "    pointsRef.current.rotation.y = time * 0.1;\n"
            "  });\n\n"
            "  return (\n"
            "    <points ref={pointsRef}>\n"
            "      <bufferGeometry>\n"
            "        <bufferAttribute\n"
            "          attach='attributes-position'\n"
            "          args={[positions, 3]}\n"
            "        />\n"
            "      </bufferGeometry>\n"
            "      <pointsMaterial size={0.05} color='cyan' />\n"
            "    </points>\n"
            "  );\n"
            "}"
        )
        return {
            "library": "@react-three/fiber",
            "particle_count": count,
            "code": code,
            "component_name": "ParticleWave",
        }
