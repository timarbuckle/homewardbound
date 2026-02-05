#!/bin/bash

# this script is now for running manually instead of via cron
echo "updating cats ..."
#systemctl --user start cats.service
uv run hbcats/manage.py update
