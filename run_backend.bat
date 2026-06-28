@echo off
set PYTHONPATH=.
set DATABASE_URL=sqlite:///./storage/helix.db
set ANALYTICS_DATABASE_URL=sqlite:///./storage/helix_analytics.db
set CHROMADB_PORT=8001
set CHROMADB_HOST=localhost
set LOG_LEVEL=INFO
".venv\Scripts\python.exe" -m uvicorn backend.api.main:app --port 8000 --host 127.0.0.1 --log-level info
