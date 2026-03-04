#!/bin/bash
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  --add-host host.docker.internal:host-gateway \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
