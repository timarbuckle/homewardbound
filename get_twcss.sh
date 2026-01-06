#!/bin/bash

echo "Pulling tailwindcss binaries"
wget -P ./bin https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.18/tailwindcss-linux-arm64
wget -P ./bin https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.18/tailwindcss-macos-arm64
