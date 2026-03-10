# RASA Chatbot Dockerfile
# Multi-stage build for optimized image size

# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Production
FROM python:3.9-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application files
COPY actions/ ./actions/
COPY quotes/ ./quotes/
COPY config/ ./config/
COPY data/ ./data/
COPY models/ ./models/
COPY web_integration/ ./web_integration/
COPY tests/ ./tests/
COPY domain.yml ./
COPY config.yml ./
COPY endpoints.yml ./
COPY credentials.yml ./
COPY requirements.txt ./

# Expose ports
# - 5005: Rasa server
# - 5055: Rasa action server
EXPOSE 5005 5055

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV Rasa_Process_Name=rasa_server
ENV Action_Process_Name=action_server

# Run both the action server and the Rasa server
# (In real deployments, prefer docker-compose / separate services.)
CMD ["sh", "-lc", "rasa run actions --port 5055 & rasa run --enable-api --cors '*' --port 5005"]
