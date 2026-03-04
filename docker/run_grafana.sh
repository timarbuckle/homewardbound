#!/bin/bash
docker run -d \
  --name grafana \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  grafana/grafana
