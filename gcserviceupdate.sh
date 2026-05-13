#!/bin/bash
gcloud run services update hbcats-web \
  --region=us-west1 \
  --set-secrets="DEBUG=DEBUG:latest,\
  LOCKDOWN_PASSWORD=LOCKDOWN_PASSWORD:latest,\
  SECRET_KEY=SECRET_KEY:latest,\
  DB_USER=DB_USER:latest,\
  DB_PASSWORD=DB_PASSWORD:latest,\
  DB_HOST=DB_HOST:latest,\
  DB_PORT=DB_PORT:latest,\
  GCP_PROJECTID=GCP_PROJECTID:latest,\
  LOG_FILE=LOG_FILE:latest,\
  CHROMEDRIVER_PATH=CHROMEDRIVER_PATH:latest,\
  CHROMEBROWSER_PATH=CHROMEBROWSER_PATH:latest" \
  --clear-env-vars \
  --clear-volumes \
  --network=default \
  --subnet=default \
  --vpc-egress=private-ranges-only \
  --no-cpu-throttling
