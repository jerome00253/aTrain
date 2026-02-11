FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install the project and its dependencies
RUN pip install --no-cache-dir -e . \
    --extra-index-url https://download.pytorch.org/whl/cu124 \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Create directories for settings and models cache
RUN mkdir -p /settings /models_cache

# Environment variables to point to the mounted volumes
ENV NICEGUI_STORAGE_PATH=/settings
ENV XDG_CACHE_HOME=/models_cache

# Expose port 8088
EXPOSE 8088

# Command to run the application in web mode
CMD ["aTrain", "start", "--no-native", "--host", "0.0.0.0", "--port", "8088"]
