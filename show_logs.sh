#!/bin/bash
# use -f to tail, -e to show last few entries
journalctl --user -u cats.service -f
