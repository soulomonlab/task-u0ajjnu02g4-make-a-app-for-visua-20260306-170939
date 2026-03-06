# Multi-stage Dockerfile for Python application
# Final image runs as non-root user

FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Install pip-tools/cache separately if needed
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app

# Create a limited-privilege user
RUN useradd --create-home --shell /bin/bash appuser

# Copy wheels and install
COPY --from=builder /wheels /wheels
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . /app
RUN pip install --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels /root/.cache

# Application listens on PORT env var (default 8080)
ENV PORT=8080
EXPOSE ${PORT}

# Use non-root user
USER appuser

# Entrypoint — configurable by CMD override in docker-compose or k8s
CMD ["gunicorn", "src.app:app", "-b", "0.0.0.0:8080", "--workers", "2"]
