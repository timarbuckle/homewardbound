#!/bin/bash
# google cloud run command

if [[  "$1" == "full" ]]; then
  gcloud run deploy hbcats-web \
    --source . \
    --image us-west1-docker.pkg.dev/tim1-399820/cloud-run-images/hbcats-app:latest \
    --region us-west1 \
    --memory 2Gi \
    --allow-unauthenticated \
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
    --cpu-throttling \
    --min-instances 0 \
    --cpu-boost
  #  --set-env-vars=DEBUG=False \
  #  --set-env-vars=LOCKDOWN_PASSWORD="kitcat" \
  #  --set-env-vars=SECRET_KEY="django-insecure-0=98+^cir)1p_hq7^$&v-q8*ygi7mlbx3#)=$=_&qxhn9di*r8" \
  #  --set-env-vars=DB_USER="kitcat" \
  #  --set-env-vars=DB_PASSWORD="meow" \
  #  --set-env-vars=DB_HOST="10.138.0.4" \
  #  --set-env-vars=DB_PORT="5432" \
  #  --set-env-vars=GCP_PROJECTID="tim1-399820" \
  #  --set-env-vars=LOG_FILE="stdout" \
  #  --set-env-vars=CHROMEDRIVER_PATH="/usr/bin/chromedriver" \
  #  --set-env-vars=CHROMEBROWSER_PATH="/usr/bin/chromium" \
  #  --set-env-vars="DATABASE_URL=postgres://kitcat:meow@100.125.216.44:5432/hbcats" \
  #  --access-logfile - \
  #  --error-logfile - \
else
  gcloud run deploy hbcats-web \
    --source . \
    --region us-west1 \
    --cpu-throttling \
    --min-instances 0 \
    --cpu-boost
fi

