#!/bin/bash

OS=$(uname -s)
if [[ "$OS" == "Linux" ]]; then
  tw="./bin/tailwindcss-linux-arm64"
elif [[ "$OS" == "Darwin" ]]; then
  tw="./bin/tailwindcss-macos-arm64"
else
  echo "Unsupported OS: $OS"
  exit 1
fi

# update tailwind css
"$tw" -i hbcats/cats/static/cats/css/input.css -o hbcats/static/cats/css/output.cs
