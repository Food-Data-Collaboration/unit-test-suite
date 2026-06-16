"""CLI entry point for the test runner."""

import argparse
import sys
from pathlib import Path

import yaml


def load_spec(spec_path: Path) -> dict:
    """Load the YAML test specification."""
    with open(spec_path) as f:
        return yaml.safe_load(f)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="DFC/JSON-LD interop test runner")
    parser.add_argument(
        "--spec",
        type=Path,
        default=Path(__file__).parent.parent.parent.parent / "spec" / "tests.yaml",
        help="Path to tests.yaml",
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path(__file__).parent.parent.parent.parent / "fixtures",
        help="Path to fixtures directory",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent.parent / "results",
        help="Path to results directory",
    )
    parser.add_argument(
        "--platform-name",
        default="python-rdflib",
        help="Platform name for results",
    )
    args = parser.parse_args()

    spec = load_spec(args.spec)
    print(f"Loaded spec with {len(spec['specs'])} test suites")
    for suite in spec["specs"]:
        print(f"  - {suite['name']}: {len(suite['tests'])} tests")

    print(f"\nFixtures directory: {args.fixtures}")
    print(f"Results directory: {args.results_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
