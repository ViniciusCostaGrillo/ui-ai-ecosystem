"""Helix UI - Knowledge Watchdog Runner"""
from backend.knowledge.watchdog import KnowledgeWatchdog
import time

if __name__ == "__main__":
    print("=" * 50)
    print("  Helix UI - Knowledge Watchdog")
    print("  Monitorando: knowledge_input/")
    print("  Pressione Ctrl+C para parar")
    print("=" * 50)
    print()

    w = KnowledgeWatchdog()
    w.start()
    print("Watchdog ativo!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nWatchdog encerrado.")
        w.stop()
