#!/usr/bin/env bash
set -e
 HEAD

# Upgrade install tools (idempotent)
python -m pip install --upgrade pip setuptools wheel || true

# Install declared requirements (idempotent)
python -m pip install -r backend/requirements.txt || true

# Ensure core runtime packages that the app needs are present
python -m pip install fastapi pymongo motor python-dotenv "uvicorn[standard]" scikit-learn joblib pandas opencv-python-headless || true

# Start the app
exec python -m uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8001}

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
 771aedd (Make start.sh install requirements and ensure uvicorn at runtime)
