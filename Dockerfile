# syntax=docker/dockerfile:1

# Use official Python runtime as base image with specific version
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_CACHE_DIR=/tmp/.uv-cache

# Install uv - fast Python package installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /tmp/chilingo && \
    chown -R appuser:appuser /app /tmp/chilingo

# Builder stage - install dependencies
FROM base AS builder

# Copy dependency files first (for better layer caching)
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies using uv
# RUN --mount=type=cache,target=/tmp/.uv-cache \
#     uv sync --frozen
RUN uv sync --frozen

# Final stage - minimal runtime image
FROM base AS runtime

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser main.py ./

# Switch to non-root user
USER appuser

# Make sure venv binaries are in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose Streamlit default port
EXPOSE 8094

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8094", "--server.address=0.0.0.0"]
