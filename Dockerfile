# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt


# ── Stage 2: Production image ─────────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="your-email@example.com"
LABEL description="Contact Form Flask App"

# Runtime dependency only (no compiler needed — pre-built wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy pre-built wheels and install
COPY --from=builder /build/wheels /wheels
RUN pip install --no-index --find-links /wheels /wheels/* \
 && rm -rf /wheels

# Copy application source
COPY app/ .

# Ownership
RUN chown -R appuser:appuser /app

USER appuser

# Environment defaults (overridden by docker-compose / .env)
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    FLASK_PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

# Wait-for-db + run migrations + start gunicorn
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:create_app()"]
