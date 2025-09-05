#!/usr/bin/env bash
set -e
# Upgrade tooling first
python -m pip install --upgrade pip setuptools wheel || true
# Install requirements (idempotent)
python -m pip install -r backend/requirements.txt || true
# If uvicorn still missing, install it explicitly
python -c "import importlib,sys; 
try:
    importlib.import_module('uvicorn')
except Exception:
    import subprocess; subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'uvicorn[standard]'])"
# Start uvicorn using the service python
python -m uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8001}
