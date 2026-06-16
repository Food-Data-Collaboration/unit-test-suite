#!/usr/bin/env bash
# Run the DFC/JSON-LD interoperability tests
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== DFC/JSON-LD Interoperability Test Runner ==="
echo ""

# Check if uv is available, otherwise use pip
if command -v uv &> /dev/null; then
    echo "Using uv for dependency management..."
    uv run pytest tests/ -v --junitxml=../../results/python-rdflib/results.xml
else
    echo "Using pip for dependency management..."
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    pytest tests/ -v --junitxml=../../results/python-rdflib/results.xml
fi

echo ""
echo "=== Tests complete ==="
echo "Results written to: results/python-rdflib/results.xml"
