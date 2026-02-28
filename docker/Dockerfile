FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    sox \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY backend /app

# Create temporary audio directory
RUN mkdir -p tmp_audio

# Expose HTTP / WebSocket port
EXPOSE 5000

# Start server with Eventlet or default
CMD ["python", "app.py"]
