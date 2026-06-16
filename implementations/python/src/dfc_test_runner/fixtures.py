"""Fixture loading utilities."""

import json
from pathlib import Path
from typing import Any


def load_fixture(fixture_path: Path, fixtures_dir: Path) -> dict[str, Any]:
    """Load a JSON-LD fixture file.

    Args:
        fixture_path: Path relative to fixtures directory
        fixtures_dir: Absolute path to fixtures directory

    Returns:
        Parsed JSON-LD as a dictionary

    Raises:
        FileNotFoundError: If fixture file does not exist
        json.JSONDecodeError: If fixture is not valid JSON
    """
    if fixture_path == "*":
        raise ValueError("Wildcard fixture path not supported for direct loading")

    full_path = fixtures_dir / fixture_path
    if not full_path.exists():
        raise FileNotFoundError(f"Fixture not found: {full_path}")

    with open(full_path) as f:
        return json.load(f)


def load_inline_input(input_data: dict[str, Any]) -> dict[str, Any]:
    """Load an inline test input from the YAML spec.

    Args:
        input_data: Inline input data from tests.yaml

    Returns:
        The input data as-is (already a dict)
    """
    return input_data
