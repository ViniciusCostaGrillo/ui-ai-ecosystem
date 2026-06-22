import sys
from pathlib import Path

# Ensure backend can be imported correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.database.chroma_client import ChromaClientManager
from backend.dependencies.dependency_agent import DependencyAgent
from backend.motion.motion_agent import MotionAgent
from backend.threejs.threejs_agent import ThreejsAgent
from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.test_motion_engine")


def test_motion_agent() -> None:
    logger.info("Testing MotionAgent suite generation...")
    agent = MotionAgent()
    suite = agent.generate_animation_suite("test-btn")

    assert "gsap" in suite
    assert "lenis" in suite
    assert "lottie" in suite
    assert "parallax" in suite
    assert "transition" in suite
    assert "microinteraction" in suite

    assert suite["gsap"]["library"] == "gsap"
    assert "ScrollTrigger" in suite["gsap"]["imports"]
    assert "Lenis" in suite["lenis"]["code"]
    logger.info("[PASS] MotionAgent animation suite generated successfully.")


def test_threejs_agent() -> None:
    logger.info("Testing ThreejsAgent suite generation...")
    agent = ThreejsAgent()
    suite = agent.generate_3d_suite("HeroBackground")

    assert "canvas" in suite
    assert "shader" in suite
    assert "particles" in suite

    assert suite["canvas"]["library"] == "@react-three/fiber"
    assert "boxgeometry" in suite["canvas"]["code"].lower()
    assert "vertex_shader" in suite["shader"]
    assert "gl_Position" in suite["shader"]["vertex_shader"]
    assert "ParticleWave" in suite["particles"]["component_name"]
    logger.info("[PASS] ThreejsAgent 3D suite generated successfully.")


def test_dependency_agent() -> None:
    logger.info("Testing DependencyAgent packages resolution...")
    agent = DependencyAgent()

    # Check resolving standard list
    res = agent.resolve_requirements(["gsap", "framer-motion", "lottie-react"])
    assert res["status"] == "success"
    assert res["dependencies"]["gsap"] == "^3.12.2"
    assert res["dependencies"]["framer-motion"] == "^10.16.4"
    assert len(res["conflicts_resolved"]) == 0

    # Check resolving peer dependency conflict
    res_conflict = agent.resolve_requirements(["@react-three/fiber"])
    assert "three" in res_conflict["dependencies"]
    assert len(res_conflict["conflicts_resolved"]) > 0
    logger.info("[PASS] DependencyAgent package conflicts resolved successfully.")


def test_chromadb_motion_indexing() -> None:
    logger.info("Testing ChromaDB vector collections indexing for animation/3D...")
    chroma = ChromaClientManager()

    collections = [
        "AnimationPatterns",
        "MotionComponents",
        "GSAPTimelines",
        "ThreeJSScenes",
        "Dependencies",
    ]

    for col in collections:
        try:
            # Create/Verify collection
            collection = chroma.client.get_or_create_collection(name=col)
            # Add a test record
            collection.upsert(
                ids=[f"test_{col}_1"],
                embeddings=[[0.1] * 384],
                documents=[f"Test document for {col}"],
                metadatas=[{"type": "test"}],
            )
            logger.info(f"[PASS] Successfully indexed test document in collection '{col}'.")
        except Exception as e:
            logger.error(f"Failed to create/index collection '{col}': {e}")
            raise


def main() -> None:
    logger.info("------------- Motion Engine Orchestration Tests -------------")
    try:
        test_motion_agent()
        test_threejs_agent()
        test_dependency_agent()
        test_chromadb_motion_indexing()
        logger.info("ALL MOTION ENGINE VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    except Exception as e:
        logger.error(f"Motion Engine verification check failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
