#!/bin/bash
# Update .env file and version
gcloud secrets versions add django_env --data-file=".env"
