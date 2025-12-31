#!/bin/bash
#export DJANGO_SETTINGS_MODULE=hbcats.hbcats.settings
#export PYTHONPATH=$(pwd)

#pushd hbcats
#uv run gunicorn hbcats.asgi:application \
#  -k uvicorn.workers.UvicornWorker \
#  --bind 127.0.0.1:8000
#popd

uv run gunicorn hbcats.wsgi:application \
  --chdir hbcats \
  --workers 3 \
  --bind 0.0.0.0:8000