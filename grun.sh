#!/bin/bash
#export DJANGO_SETTINGS_MODULE=hbcats.hbcats.settings
#export PYTHONPATH=$(pwd)

# run django app using uv
uv run gunicorn hbcats.wsgi:application \
  --chdir hbcats \
  --workers 2 \
  --threads 4 \
  --worker-class gthread \
  --preload \
  --timeout 120 \
  --max-requests 100 \
  --bind 0.0.0.0:8000
