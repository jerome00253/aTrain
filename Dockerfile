FROM python:3.11-slim

# Environments variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    XDG_DOCUMENTS_DIR=/data \
    NICEGUI_STORAGE_PATH=/data/aTrain/settings \
    XDG_CACHE_HOME=/data/aTrain/models

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# 1. Heavy ML dependencies (Rarely change - cached)
RUN pip install --no-cache-dir \
    torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 2. atrain_core and stable sub-dependencies (Cached)
RUN pip install --no-cache-dir --no-deps "atrain_core@git+https://github.com/JuergenFleiss/atrain_core.git@v1.4.1" && \
    pip install --no-cache-dir \
    "faster-whisper==1.0.2" \
    "pandas==2.2.3" \
    "pyannote.audio==4.0.3" \
    "numpy==2.2.2" \
    "werkzeug==3.0.3" \
    "huggingface-hub==0.30.2" \
    "platformdirs==4.5.1"

# 3. Application setup - Optimization
# First copy only project definition to install dependencies (fast if no changes)
COPY pyproject.toml .

# CACHE BUSTER for application code/UI changes
# Increment this to force a refresh of the UI/Logic
ARG BUILD_ID=12
RUN echo "Build ID: $BUILD_ID"

# Now copy the actual source code
COPY aTrain ./aTrain
COPY . .

# Final installation of the package itself (must be AFTER copying the code)
RUN pip install --no-cache-dir .

# Create data directory
RUN mkdir -p /data

# Expose port 8088
EXPOSE 8088

# Command to run the application in web mode
CMD ["aTrain", "start", "--no-native", "--host", "0.0.0.0", "--port", "8088"]
