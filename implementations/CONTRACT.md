# Implementation Contract

**Version:** 1.0.0

This document tells implementers exactly what's expected when building a test adapter for a new platform.

---

## Overview

Each platform adapter must:

1. Load fixture files from `/fixtures/`
2. Execute test cases defined in `/spec/tests.yaml`
3. Emit results as JUnit XML to `/results/{platform-name}/results.xml`

---

## Quick Start

### 1. Choose a platform name

Use a consistent lowercase hyphenated name:
- `python-rdflib`
- `ruby-ofn`
- `php-connector`
- `java-titanium`
- `node-jsonld`
- `go-jsonld`

### 2. Create your implementation directory

```
/implementations/{platform-name}/
```

### 3. Implement the adapter interface

Your adapter must implement these operations:

| Operation | Description |
|-----------|-------------|
| `parse_jsonld(data)` | Parse JSON-LD dict into native structure |
| `serialize_jsonld(data)` | Serialize native structure back to JSON-LD |
| `validate(data)` | Validate against context, return error list |
| `expand(data)` | Expand JSON-LD |
| `compact(data, context)` | Compact expanded JSON-LD |
| `flatten(data)` | Flatten JSON-LD |

---

## Which Fixtures to Load

Read the `fixture` field from each test case in `tests.yaml`. If the fixture is `null`, use the `inline_inputs` field instead.

Example test case:

```yaml
- id: SER-001
  fixture: enterprise/enterprise_full.jsonld
  action: "Parse the fixture..."
  expected: "All fields accessible..."
```

Load: `/fixtures/enterprise/enterprise_full.jsonld`

---

## What Functions/Classes to Test

Each test case maps to one assertion in your test suite. The test ID (e.g., `SER-001`) must appear in the JUnit XML `classname` attribute.

### Test Structure

```
tests/
  conftest.py          # Shared fixtures (fixture loader)
  test_dfc_serialization.py
  test_dfc_schema.py
  test_dfc_edge_cases.py
  test_jsonld_serialization.py
  test_jsonld_schema.py
  test_jsonld_edge_cases.py
```

---

## What Assertions to Make

Each test case in the YAML spec has an `action` and `expected` field. Your assertions should verify:

1. **Action performed**: Did you execute the described operation?
2. **Expected result**: Does the output match the expected criteria?

### Assertion Examples

| Test ID | Assertion Type |
|---------|---------------|
| SER-001 | Field accessibility, type resolution |
| SCH-003 | Error raised for invalid input |
| EDG-002 | Both forms accepted without error |
| EDG-010 | Empty collection returned, no error |

---

## How to Name Tests

Use the test ID as the `classname` in JUnit XML:

```xml
<testcase classname="SER-001" name="Parse a DFC Organization document" time="0.021"/>
```

The `name` field should match the test description from the spec.

---

## How to Submit Results

1. Run your tests and capture JUnit XML output
2. Place the file at: `/results/{platform-name}/results.xml`
3. Commit and push to the shared repository

### Example Results Structure

```
/results/
  /python-rdflib/
    results.xml
  /ruby-ofn/
    results.xml
  /php-connector/
    results.xml
```

---

## JUnit XML Format

All platforms MUST emit results in this format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="dfc-interop" time="2.345">
  <testsuite name="serialization" tests="11" failures="0" errors="0" skipped="0">
    <testcase classname="SER-001" name="Parse a DFC Organization document" time="0.021"/>
    <testcase classname="SER-002" name="Parse a SuppliedProduct with QuantitativeValue" time="0.018"/>
  </testsuite>
  <testsuite name="schema" tests="9" failures="0" errors="0" skipped="1">
    <testcase classname="SCH-009" name="Validate context version matches ontology version">
      <skipped message="Version pinning not yet implemented"/>
    </testcase>
  </testsuite>
  <testsuite name="edge-case" tests="15" failures="1" errors="0" skipped="0">
    <testcase classname="EDG-006" name="Refrigeration flags as booleans vs strings" time="0.009">
      <failure message="String 'true' not accepted" type="AssertionError">
        Expected truthy result for dfc-b:refrigerated = "true", got parsing error.
      </failure>
    </testcase>
  </testsuite>
</testsuites>
```

### Key Rules

- `classname` = test ID (e.g., `SER-001`)
- `name` = test description from spec
- `time` = execution time in seconds
- Use `<skipped>` for optional tests not implemented
- Use `<failure>` for assertion failures
- Use `<error>` for runtime errors

---

## Running Tests

### Python (reference implementation)

```bash
cd implementations/python
./run_tests.sh
```

### Manual runner

```bash
# Load spec
cat spec/tests.yaml

# For each test case:
#   1. Load fixture
#   2. Execute action
#   3. Assert expected result
#   4. Record pass/fail/skip
```

---

## Checklist

Before submitting your results:

- [ ] All fixtures load successfully
- [ ] All mandatory tests are implemented
- [ ] JUnit XML uses correct `classname` attributes
- [ ] Results file is at `/results/{platform-name}/results.xml`
- [ ] Platform name matches your implementation directory

---

## Questions?

Open an issue in the shared repository with the `test-spec` label.
