#!/usr/bin/env bash
set -e

# 1) Upgrade tooling (idempotent)
python -m pip install --upgrade pip setuptools wheel || true

# 2) Install declared requirements (idempotent)
python -m pip install -r backend/requirements.txt || true

# 3) Ensure essential runtime packages (explicit)
python -m pip install fastapi motor pymongo python-dotenv scikit-learn joblib opencv-python-headless pandas numpy || true

# 4) Ensure uvicorn present
python -m pip install "uvicorn[standard]" || true

# 5) Start the app
python -m uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8001}
