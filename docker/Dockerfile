# 1. Use a slim Python base
FROM python:3.14-slim AS builder

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set working directory and sync dependencies
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev

# 4. Final Stage
FROM python:3.14-slim
WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Ensure we use the virtualenv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy your Django project files
COPY . .

# Cloud Run listens on $PORT
CMD [ \
  "uv", "run", "gunicorn", \
  "hbcats.wsgi:application", \
  "--bind", "0.0.0.0:8080", \
  "--chdir", "hbcats", \
  "--workers", "1", \
  "--threads", "2", \
  "--worker-class", \
  "gthread", "--preload", \
  "--timeout" "120", \
  "--max-requests", "100" \
  ]
