#!/bin/bash

# be sure to wrap "$SCHEDULE" in quotes when using below due to the *s
SCHEDULE="0 12,16,20 * * *"

if [[ "$1" == "now" ]]; then
  gcloud scheduler jobs run hbcats-selenium-run --location=us-west1
elif [[ "$1" == "create" ]]; then
  gcloud scheduler jobs create http hbcats-selenium-run \
    --schedule="$SCHEDULE" \
    --time-zone="America/Los_Angeles" \
    --uri="https://hbcats-web-32514012237.us-west1.run.app/api/update/" \
    --http-method=GET \
    --location=us-west1 \
    --oidc-service-account-email="32514012237-compute@developer.gserviceaccount.com" \
    --oidc-token-audience="https://hbcats-web-32514012237.us-west1.run.app/your-endpoint/"
elif [[ "$1" == "update" ]]; then
  # Only need to include the flags you want to change.
  # If you are only changing the time, you don't need to re-type the --uri
  # or the --oidc-service-account-email.
  # Cloud Scheduler will remember the rest.
  gcloud scheduler jobs update http hbcats-selenium-run \
    --schedule="$SCHEDULE" \
    --time-zone="America/Los_Angeles" \
    --location=us-west1
    #--uri="https://hbcats-web-32514012237.us-west1.run.app/api/update/" \
    #--http-method=GET \
    #--oidc-service-account-email="32514012237-compute@developer.gserviceaccount.com" \
    #--oidc-token-audience="https://hbcats-web-32514012237.us-west1.run.app/your-endpoint/"
elif [[ "$1" == "pause" ]]; then
  gcloud scheduler jobs pause hbcats-selenium-run --location=us-west1
elif [[ "$1" == "resume" ]]; then
  gcloud scheduler jobs resume hbcats-selenium-run --location=us-west1
elif [[ "$1" == "show" ]]; then
  gcloud scheduler jobs describe hbcats-selenium-run --location=us-west1
else
  echo "options: now, create, update, pause, resume, show"
fi
