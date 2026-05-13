#!/bin/bash
# google cloud build to run on cloud run
gcloud builds submit --tag us-west1-docker.pkg.dev/tim1-399820/cloud-run-images/hbcats-app:latest . 
