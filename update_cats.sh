#!/bin/bash
# run job to update latest cats
cd "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]}")")"
uv run hbcats/manage.py update
