#!/usr/bin/env python3
"""Cross-platform validation script.

Compares JUnit XML outputs from multiple platforms to identify:
- Tests that all platforms pass
- Tests that some platforms fail
- Tests that platforms skip
- Missing test coverage

Usage:
    python scripts/validate_results.py [--results-dir ./results]
"""

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def parse_junit_xml(xml_path: Path) -> dict[str, dict]:
    """Parse a JUnit XML file and extract test results.

    Returns:
        Dict mapping test_id -> {status, classname, name, time, message}
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    results = {}
    for testsuite in root.findall(".//testsuite"):
        for testcase in testsuite.findall("testcase"):
            classname = testcase.get("classname", "")
            name = testcase.get("name", "")
            time_val = testcase.get("time", "0")

            failure = testcase.find("failure")
            error = testcase.find("error")
            skipped = testcase.find("skipped")

            if failure is not None:
                status = "failure"
                message = failure.get("message", "")
            elif error is not None:
                status = "error"
                message = error.get("message", "")
            elif skipped is not None:
                status = "skipped"
                message = skipped.get("message", "")
            else:
                status = "pass"
                message = ""

            results[classname] = {
                "status": status,
                "classname": classname,
                "name": name,
                "time": time_val,
                "message": message,
            }

    return results


def validate_results(results_dir: Path) -> dict[str, dict]:
    """Validate all platform results in the results directory.

    Returns:
        Dict mapping platform_name -> parsed results
    """
    all_results = {}

    for platform_dir in results_dir.iterdir():
        if not platform_dir.is_dir():
            continue

        results_xml = platform_dir / "results.xml"
        if not results_xml.exists():
            continue

        platform_name = platform_dir.name
        try:
            all_results[platform_name] = parse_junit_xml(results_xml)
        except ET.ParseError as e:
            print(f"Warning: Failed to parse {results_xml}: {e}", file=sys.stderr)

    return all_results


def compare_results(all_results: dict[str, dict]) -> dict:
    """Compare results across platforms.

    Returns:
        Summary dict with pass/fail/skip stats
    """
    # Collect all test IDs across platforms
    all_test_ids = set()
    for platform_results in all_results.values():
        all_test_ids.update(platform_results.keys())

    comparison = {
        "total_tests": len(all_test_ids),
        "platforms": list(all_results.keys()),
        "all_pass": [],
        "some_fail": [],
        "some_skip": [],
        "missing": [],
    }

    for test_id in sorted(all_test_ids):
        statuses = []
        for platform, results in all_results.items():
            if test_id in results:
                statuses.append(results[test_id]["status"])
            else:
                statuses.append("missing")

        if all(s == "pass" for s in statuses):
            comparison["all_pass"].append(test_id)
        elif any(s in ("failure", "error") for s in statuses):
            comparison["some_fail"].append(test_id)
        elif any(s == "skipped" for s in statuses):
            comparison["some_skip"].append(test_id)
        else:
            comparison["missing"].append(test_id)

    return comparison


def print_report(comparison: dict):
    """Print a human-readable comparison report."""
    print("=" * 60)
    print("Cross-Platform Validation Report")
    print("=" * 60)
    print()

    print(f"Platforms tested: {len(comparison['platforms'])}")
    for platform in comparison["platforms"]:
        print(f"  - {platform}")
    print()

    print(f"Total test cases: {comparison['total_tests']}")
    print(f"All pass: {len(comparison['all_pass'])}")
    print(f"Some fail: {len(comparison['some_fail'])}")
    print(f"Some skip: {len(comparison['some_skip'])}")
    print(f"Missing: {len(comparison['missing'])}")
    print()

    if comparison["some_fail"]:
        print("FAILURES:")
        for test_id in comparison["some_fail"]:
            print(f"  - {test_id}")
        print()

    if comparison["some_skip"]:
        print("SKIPPED:")
        for test_id in comparison["some_skip"]:
            print(f"  - {test_id}")
        print()

    if comparison["missing"]:
        print("MISSING:")
        for test_id in comparison["missing"]:
            print(f"  - {test_id}")
        print()

    # Compliance rate
    total = comparison["total_tests"]
    passing = len(comparison["all_pass"])
    if total > 0:
        rate = (passing / total) * 100
        print(f"Compliance rate: {rate:.1f}% ({passing}/{total})")
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate cross-platform JUnit results")
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path(__file__).parent.parent / "results",
        help="Path to results directory",
    )
    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"Results directory not found: {args.results_dir}", file=sys.stderr)
        return 1

    all_results = validate_results(args.results_dir)
    if not all_results:
        print("No platform results found in", args.results_dir, file=sys.stderr)
        return 1

    comparison = compare_results(all_results)
    print_report(comparison)

    # Return non-zero if any failures
    if comparison["some_fail"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
