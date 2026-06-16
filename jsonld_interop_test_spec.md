# JSON-LD Interoperability Test Specification

**Version:** 1.0.0
**Status:** Draft
**Last Updated:** 2026-06-16

---

## Purpose

This document defines the canonical test suite for JSON-LD data interoperability across all participating platforms. Every platform implementing this specification must pass all mandatory tests and report results in JUnit XML format.

The spec covers three areas:

- Serialization & deserialization
- Schema validation
- Edge cases & error handling

---

## Conventions

- **MUST** — mandatory; test failure if not met
- **SHOULD** — strongly recommended
- **MAY** — optional
- All fixture files are located in `/fixtures/` in the shared repository
- Test IDs are stable and must not be changed once published
- All platforms MUST use the fixture files as-is; locally generated equivalents are not acceptable

---

## Repository Structure

```
/spec
  jsonld_interop_test_spec.md   ← this document
/fixtures
  /valid
    minimal.jsonld
    full_context.jsonld
    nested_nodes.jsonld
    array_values.jsonld
    multilingual.jsonld
  /invalid
    malformed_json.jsonld
    missing_context.jsonld
    broken_iri.jsonld
    type_mismatch.jsonld
  /roundtrip
    source.jsonld
    compacted.jsonld
    expanded.jsonld
    flattened.jsonld
/results
  /{platform-name}/results.xml  ← JUnit XML output
```

---

## Test Case Format

Each test case below follows this structure:

| Field | Description |
|---|---|
| **ID** | Stable unique identifier (never reused) |
| **Category** | `serialization`, `schema`, or `edge-case` |
| **Priority** | `mandatory` or `optional` |
| **Fixture** | File path relative to `/fixtures/` |
| **Action** | What the platform must do |
| **Expected Result** | Pass/fail criteria |

---

## 1. Serialization & Deserialization

### SER-001 — Parse minimal valid JSON-LD

| | |
|---|---|
| **ID** | SER-001 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `valid/minimal.jsonld` |
| **Action** | Parse the fixture into the platform's native JSON-LD structure |
| **Expected Result** | Parses without error; `@context` and `@type` fields are accessible |

**Fixture content** (`valid/minimal.jsonld`):
```json
{
  "@context": "https://schema.org/",
  "@type": "Person",
  "name": "Jane Smith"
}
```

---

### SER-002 — Serialise native object to JSON-LD string

| | |
|---|---|
| **ID** | SER-002 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `valid/minimal.jsonld` |
| **Action** | Construct an equivalent object natively, serialize to JSON-LD string, parse back, and compare |
| **Expected Result** | Round-trip produces semantically equivalent JSON-LD (key order MAY vary) |

---

### SER-003 — Expand JSON-LD

| | |
|---|---|
| **ID** | SER-003 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `roundtrip/source.jsonld` and `roundtrip/expanded.jsonld` |
| **Action** | Expand the source fixture and compare against the expected expanded form |
| **Expected Result** | Expanded output matches `expanded.jsonld` semantically |

---

### SER-004 — Compact JSON-LD

| | |
|---|---|
| **ID** | SER-004 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `roundtrip/expanded.jsonld` and `roundtrip/compacted.jsonld` |
| **Action** | Compact the expanded fixture using the context in `compacted.jsonld`, compare output |
| **Expected Result** | Compacted output matches `compacted.jsonld` semantically |

---

### SER-005 — Flatten JSON-LD

| | |
|---|---|
| **ID** | SER-005 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `roundtrip/source.jsonld` and `roundtrip/flattened.jsonld` |
| **Action** | Flatten the source fixture and compare against the expected flattened form |
| **Expected Result** | Flattened output matches `flattened.jsonld`; all blank nodes are consistently identified |

---

### SER-006 — Full round-trip fidelity (expand → compact)

| | |
|---|---|
| **ID** | SER-006 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `roundtrip/source.jsonld` |
| **Action** | Expand then compact the fixture using its own context |
| **Expected Result** | Output is semantically equivalent to the original source; no data is lost or mutated |

---

### SER-007 — Nested node objects

| | |
|---|---|
| **ID** | SER-007 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `valid/nested_nodes.jsonld` |
| **Action** | Parse and access a deeply nested node (3+ levels) |
| **Expected Result** | All nested `@id`, `@type`, and property values are accessible without error |

---

### SER-008 — Array-valued properties

| | |
|---|---|
| **ID** | SER-008 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `valid/array_values.jsonld` |
| **Action** | Parse and iterate over array-valued properties |
| **Expected Result** | All array elements are accessible; order is preserved |

---

### SER-009 — Multi-language strings (`@language`)

| | |
|---|---|
| **ID** | SER-009 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `valid/multilingual.jsonld` |
| **Action** | Parse a document with `@language` tags on string values |
| **Expected Result** | Language tags are preserved and accessible per value |

---

### SER-010 — Numeric and boolean value types

| | |
|---|---|
| **ID** | SER-010 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `valid/full_context.jsonld` |
| **Action** | Deserialize integer, float, and boolean typed values; re-serialize and compare |
| **Expected Result** | Types are preserved through the round-trip; no coercion to strings |

---

## 2. Schema Validation

### SCH-001 — Accept document conforming to context

| | |
|---|---|
| **ID** | SCH-001 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `valid/full_context.jsonld` |
| **Action** | Validate the fixture against its declared `@context` |
| **Expected Result** | Validation passes; zero errors or warnings |

---

### SCH-002 — Reject document with missing `@context`

| | |
|---|---|
| **ID** | SCH-002 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `invalid/missing_context.jsonld` |
| **Action** | Attempt to validate or process the fixture |
| **Expected Result** | Platform raises a specific, catchable error indicating missing context; does not silently succeed |

---

### SCH-003 — Reject malformed IRI

| | |
|---|---|
| **ID** | SCH-003 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `invalid/broken_iri.jsonld` |
| **Action** | Attempt to process the fixture; observe IRI resolution behaviour |
| **Expected Result** | Platform raises an error or warning for the malformed IRI; it MUST NOT silently resolve it to a relative path |

---

### SCH-004 — Reject type mismatch

| | |
|---|---|
| **ID** | SCH-004 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `invalid/type_mismatch.jsonld` |
| **Action** | Validate the fixture where a property value has the wrong `@type` |
| **Expected Result** | Validation raises an error referencing the specific property; does not silently coerce the value |

---

### SCH-005 — Resolve remote context (optional)

| | |
|---|---|
| **ID** | SCH-005 |
| **Category** | schema |
| **Priority** | optional |
| **Fixture** | `valid/minimal.jsonld` (uses `https://schema.org/`) |
| **Action** | Fetch and resolve the remote context at `https://schema.org/` |
| **Expected Result** | Context is resolved and terms are correctly mapped; network errors are caught and surfaced cleanly |

> **Note:** Platforms operating in air-gapped environments MAY skip SCH-005 and mark it `skipped` in their JUnit output.

---

## 3. Edge Cases & Error Handling

### EDG-001 — Malformed JSON (not valid JSON at all)

| | |
|---|---|
| **ID** | EDG-001 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `invalid/malformed_json.jsonld` |
| **Action** | Attempt to parse the fixture |
| **Expected Result** | A JSON parse error is raised before any JSON-LD processing; error message is human-readable |

---

### EDG-002 — Empty document `{}`

| | |
|---|---|
| **ID** | EDG-002 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline — no fixture file required)* `{}` |
| **Action** | Parse and expand an empty JSON object |
| **Expected Result** | Returns an empty array `[]` on expansion; no error is thrown |

---

### EDG-003 — Null property values

| | |
|---|---|
| **ID** | EDG-003 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse a document where a property value is explicitly `null` |
| **Input:** | `{ "@context": "https://schema.org/", "name": null }` |
| **Expected Result** | Null value is preserved and accessible; property is not silently dropped |

---

### EDG-004 — Unicode in string values

| | |
|---|---|
| **ID** | EDG-004 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `valid/multilingual.jsonld` |
| **Action** | Parse and re-serialize strings containing non-ASCII characters (CJK, Arabic, emoji) |
| **Expected Result** | Characters are preserved exactly through round-trip; no encoding errors |

---

### EDG-005 — Very large integer values

| | |
|---|---|
| **ID** | EDG-005 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Input** | `{ "@context": "https://schema.org/", "identifier": 9007199254740993 }` (> MAX_SAFE_INTEGER) |
| **Action** | Parse and re-serialize the value |
| **Expected Result** | Value is preserved without silent precision loss; platforms that cannot represent it exactly MUST raise an error rather than silently truncate |

---

### EDG-006 — Duplicate keys in JSON object

| | |
|---|---|
| **ID** | EDG-006 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* `{ "@context": "https://schema.org/", "name": "First", "name": "Second" }` |
| **Action** | Parse the document with a duplicate key |
| **Expected Result** | Either raises an error OR deterministically retains one value (last-wins is acceptable); behaviour MUST be documented by the platform; silent data loss is not acceptable |

---

### EDG-007 — Circular `@context` reference

| | |
|---|---|
| **ID** | EDG-007 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Attempt to process a context that references itself (simulated via a local mock context server or inline context with a cyclic `@import`) |
| **Expected Result** | Platform detects the cycle and raises a specific error; does not hang or exhaust memory |

---

### EDG-008 — `@graph` container

| | |
|---|---|
| **ID** | EDG-008 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `valid/full_context.jsonld` (must include a `@graph` node) |
| **Action** | Parse a document with a top-level `@graph` array and access individual nodes |
| **Expected Result** | All nodes within `@graph` are accessible; graph container is not flattened or dropped |

---

### EDG-009 — Deeply nested blank nodes

| | |
|---|---|
| **ID** | EDG-009 |
| **Category** | edge-case |
| **Priority** | optional |
| **Fixture** | `valid/nested_nodes.jsonld` |
| **Action** | Parse a document with blank nodes nested 5+ levels deep |
| **Expected Result** | All nodes reachable without stack overflow or memory error on typical hardware |

---

## Reporting Requirements

### JUnit XML format

All platforms MUST emit results as JUnit XML. The `classname` attribute of each `<testcase>` MUST match the test ID from this spec (e.g. `SER-001`). This enables automated cross-platform result aggregation.

Example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="jsonld-interop" time="1.234">
  <testsuite name="serialization" tests="10" failures="0" errors="0" skipped="0">
    <testcase classname="SER-001" name="Parse minimal valid JSON-LD" time="0.012"/>
    <testcase classname="SER-002" name="Serialise native object to JSON-LD string" time="0.008"/>
    <!-- ... -->
  </testsuite>
  <testsuite name="schema" tests="5" failures="1" errors="0" skipped="1">
    <testcase classname="SCH-001" name="Accept document conforming to context" time="0.015"/>
    <testcase classname="SCH-005" name="Resolve remote context">
      <skipped message="Air-gapped environment"/>
    </testcase>
    <testcase classname="SCH-004" name="Reject type mismatch" time="0.011">
      <failure message="No error raised for type mismatch" type="AssertionError">
        Expected validation error, got success.
      </failure>
    </testcase>
  </testsuite>
</testsuites>
```

### Result submission

Place results at `/results/{platform-name}/results.xml` in the shared repository. Use a consistent, lowercase hyphenated platform name (e.g. `python-rdflib`, `java-titanium`, `node-jsonld`).

---

## Versioning & Change Control

| Version | Change |
|---|---|
| 1.0.0 | Initial release — 19 test cases across 3 categories |

New test IDs will be added monotonically. Existing IDs will never be reassigned. Mandatory/optional status will not be downgraded without a major version bump and 4-week notice to all implementing platforms.

---

## Contact

Raise questions or propose new test cases via the shared repository's issue tracker. Tag issues with `test-spec` for routing.
