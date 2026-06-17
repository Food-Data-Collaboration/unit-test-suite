#!/usr/bin/env bash
# Run the DFC/JSON-LD interoperability tests
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== DFC/JSON-LD Interoperability Test Runner (PHP) ==="
echo ""

if [ ! -d "vendor" ]; then
  echo "Installing dependencies..."
  composer install --quiet
fi

echo "Running tests..."
vendor/bin/phpunit --configuration phpunit.xml --log-junit ../../results/php-connector/results.xml

echo ""
echo "=== Tests complete ==="
echo "Results written to: results/php-connector/results.xml"
