#!/bin/bash
uv run hbcats/manage.py dumpdata cats.Cat --indent 2 >cats_export.json
