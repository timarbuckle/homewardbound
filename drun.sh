#!/bin/bash
# local docker run
docker run -it --rm \
  -p 8080:8080 \
  --env-file .env.localdocker \
  -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/google_credentials.json:ro \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/google_credentials.json \
  hbcats-local
