# Use official Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install minimal system packages required for builds
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpq-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt /app/requirements.txt

# Upgrade pip, setuptools, wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Install requirements, write pip freeze, and print it so it appears in build logs
RUN pip install --no-cache-dir -r /app/requirements.txt && \
    python -m pip freeze > /app/pip_freeze.txt && \
    echo "===== BEGIN PIP FREEZE =====" && cat /app/pip_freeze.txt && echo "=====  END PIP FREEZE ====="

# Copy backend source
COPY backend /app

# Show files in /app for debugging
RUN echo "===== LS /app =====" && ls -la /app || true

ENV PORT=10000
EXPOSE 10000

# Start with python -m uvicorn (avoids PATH surprises)
CMD ["sh", "-c", "python -m uvicorn server:app --host 0.0.0.0 --port ${PORT}"]
