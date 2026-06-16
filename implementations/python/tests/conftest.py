"""Shared pytest fixtures for DFC/JSON-LD interop tests."""

import json
from pathlib import Path

import pytest
import yaml


FIXTURES_DIR = Path(__file__).parent.parent.parent.parent / "fixtures"
SPEC_PATH = Path(__file__).parent.parent.parent.parent / "spec" / "tests.yaml"


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to the fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture
def spec() -> dict:
    """Load the test specification."""
    with open(SPEC_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture
def dfc_spec(spec) -> dict:
    """DFC-specific test specification."""
    for s in spec["specs"]:
        if s["name"] == "dfc-interop":
            return s
    raise ValueError("DFC spec not found")


@pytest.fixture
def jsonld_spec(spec) -> dict:
    """JSON-LD-specific test specification."""
    for s in spec["specs"]:
        if s["name"] == "jsonld-interop":
            return s
    raise ValueError("JSON-LD spec not found")


@pytest.fixture
def load_fixture(fixtures_dir):
    """Fixture loader function."""
    def _load(relative_path: str) -> dict:
        full_path = fixtures_dir / relative_path
        with open(full_path) as f:
            return json.load(f)
    return _load
