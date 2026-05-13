#!/bin/sh
# command to start django app in google cloud run
#
# Note: Cloud Run usually expects the app on port 8080 by default
echo "Starting Gunicorn..."
exec uv run gunicorn hbcats.wsgi:application \
  --chdir hbcats \
  --workers 2 \
  --threads 4 \
  --worker-class gthread \
  --preload \
  --timeout 120 \
  --max-requests 100 \
  --bind 0.0.0.0:8080

