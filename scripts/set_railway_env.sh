#!/usr/bin/env bash
set -euo pipefail

# Usage: create .env.deploy from .env.deploy.example, fill values, then run this script
# Requires: Railway CLI installed and project linked (run `railway login` and `railway link`)

if ! command -v railway >/dev/null 2>&1; then
  echo "railway CLI not found. Install it: https://docs.railway.app/develop/cli"
  exit 1
fi

if [ ! -f .env.deploy ]; then
  echo ".env.deploy file not found. Copy .env.deploy.example -> .env.deploy and fill values." 
  exit 1
fi

echo "Make sure you're logged in and have the correct project linked:"
echo "  railway login"
echo "  railway link"
read -p "Press Enter to continue once linked to the correct project..." 

while IFS='=' read -r key value; do
  # skip empty lines and comments
  [[ -z "$key" ]] && continue
  [[ ${key:0:1} == "#" ]] && continue
  # trim whitespace
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | xargs)
  if [ -z "$key" ]; then
    continue
  fi
  echo "Setting variable: $key"
  railway variables set "$key" "$value"
done < .env.deploy

echo "All variables set."
