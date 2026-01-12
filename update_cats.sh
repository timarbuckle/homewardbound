#!/bin/bash
# run job to update latest cats
cd "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]}")")"
PATH=/home/tim/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
export DISPLAY=:0
/home/tim/.local/bin/uv run hbcats/manage.py update
