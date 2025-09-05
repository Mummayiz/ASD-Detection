#!/usr/bin/env bash
set -e

# Upgrade install tools (idempotent)
python -m pip install --upgrade pip setuptools wheel || true

# Install declared requirements (idempotent)
python -m pip install -r backend/requirements.txt || true

# Ensure core runtime packages that the app needs are present
python -m pip install fastapi pymongo motor python-dotenv "uvicorn[standard]" scikit-learn joblib pandas opencv-python-headless || true

# Start the app
exec python -m uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8001}
