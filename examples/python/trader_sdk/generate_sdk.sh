#!/usr/bin/env bash
# Regenerate the youngplatform_trader_client Python SDK from the trader OpenAPI spec.
#
# The spec (../../trader_openapi.json) is produced by the API backend — run its
# swagger generation and copy the resulting trader_openapi.json here. This script
# only runs the SDK codegen step from that committed spec:
#
#   openapi-python-client  -> youngplatform_trader_client/
#
# Usage:
#   ./generate_sdk.sh
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
SPEC="$DIR/../../../trader_openapi.json"

if [[ ! -f "$SPEC" ]]; then
  echo "spec not found at '$SPEC' — copy trader_openapi.json from the API backend first" >&2
  exit 1
fi

config="$(mktemp)"
trap 'rm -f "$config"' EXIT
echo "package_name_override: youngplatform_trader_client" > "$config"

cd "$DIR"
rm -rf youngplatform_trader_client
uvx openapi-python-client generate \
  --path "$SPEC" --meta none --config "$config"
rm -rf youngplatform_trader_client/.ruff_cache
echo "regenerated $DIR/youngplatform_trader_client"
