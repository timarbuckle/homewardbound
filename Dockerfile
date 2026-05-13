FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

# Install system dependencies
# 1. chromium and chromium-driver for Selenium
# 2. ca-certificates for secure connections
# 3. curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions in uv.lock
RUN uv sync --frozen

# Copy the rest of your app code
COPY . .

# Copy and prepare the startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Environment Variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
# This helps Selenium find the right driver path
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Execute the startup script
CMD ["/app/start.sh"]
