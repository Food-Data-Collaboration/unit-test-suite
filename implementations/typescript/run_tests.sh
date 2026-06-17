#!/usr/bin/env bash
# Run the DFC/JSON-LD interoperability tests
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== DFC/JSON-LD Interoperability Test Runner (TypeScript) ==="
echo ""

if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install --silent
fi

echo "Building TypeScript..."
npx tsc --quiet

echo "Running tests..."
npx jest --config jest.config.js

echo ""
echo "=== Tests complete ==="
echo "Results written to: results/node-jsonld/results.xml"
