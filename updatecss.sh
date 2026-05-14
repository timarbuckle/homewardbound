#!/bin/bash

 npx @tailwindcss/cli -i  hbcats/static/cats/css/input.css -o hbcats/static/cats/css/output.css --minify
 uv run python3 hbcats/manage.py collectstatic --noinput
