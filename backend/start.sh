#!/usr/bin/env bash
# Ensure dependencies are installed in the environment Render created
python -m pip install -r backend/requirements.txt || true
# Start uvicorn using the service python
python -m uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8001}
