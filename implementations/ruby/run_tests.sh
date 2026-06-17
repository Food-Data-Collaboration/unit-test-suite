#!/usr/bin/env bash
# Run the DFC/JSON-LD interoperability tests
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== DFC/JSON-LD Interoperability Test Runner (Ruby) ==="
echo ""

if [ ! -d ".bundle" ]; then
  echo "Installing dependencies..."
  bundle install
fi

echo "Running tests..."
bundle exec rake spec

echo ""
echo "=== Tests complete ==="
echo "Results written to: results/ruby-ofn/results.xml"
