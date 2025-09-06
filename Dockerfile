# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system packages needed for some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpq-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install them
COPY backend/requirements.txt /app/requirements.txt

# Upgrade pip and install wheel/setuptools, then requirements
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend source
COPY backend /app

# Expose port (Render provides  at runtime)
ENV PORT=10000
EXPOSE 10000

# Start the FastAPI app using the PORT Render provides at runtime
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port "]
