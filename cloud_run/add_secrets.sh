#!/bin/bash
echo -n "$2" | gcloud secrets create $1 --data-file=-
gcloud secrets add-iam-policy-binding $1 \
  --member="serviceAccount:32514012237-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
