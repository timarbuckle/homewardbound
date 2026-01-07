#!/bin/bash

OS=$(uname -s)
if [[ "$OS" == "Linux" ]]; then
  tw="tailwindcss-linux-arm64"
elif [[ "$OS" == "Darwin" ]]; then
  tw="tailwindcss-macos-arm64"
else
  echo "OS not supported: $OS"
  exit 1
fi
echo "Pulling tailwindcss binaries"
wget -P ./bin "https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.18/$tw"
chmod +x "./bin/$tw"
