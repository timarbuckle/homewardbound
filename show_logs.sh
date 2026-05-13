#!/bin/bash
# view app logs when running as a systemctl service
# use -f to tail, -e to show last few entries
journalctl --user -u cats.service -f
