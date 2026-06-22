import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class TransitionAgent:
    """Agent that generates route page transition animations templates."""

    def generate_page_transition(self) -> Dict[str, Any]:
        logger.info("TransitionAgent: generating Framer Motion page transition component...")
        code = (
            "import { motion } from 'framer-motion';\n\n"
            "const pageTransition = {\n"
            "  initial: { opacity: 0, y: 20 },\n"
            "  animate: { opacity: 1, y: 0 },\n"
            "  exit: { opacity: 0, y: -20 }\n"
            "};\n\n"
            "export default function PageTransitionWrapper({ children }) {\n"
            "  return (\n"
            "    <motion.div\n"
            "      initial='initial'\n"
            "      animate='animate'\n"
            "      exit='exit'\n"
            "      variants={pageTransition}\n"
            "      transition={{ duration: 0.5, ease: [0.6, -0.05, 0.01, 0.9] }}\n"
            "    >\n"
            "      {children}\n"
            "    </motion.div>\n"
            "  );\n"
            "}"
        )
        return {
            "library": "framer-motion",
            "code": code,
            "component_name": "PageTransitionWrapper",
        }
