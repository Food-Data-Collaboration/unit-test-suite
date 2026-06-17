# AGENTS.md

## What this repo is

Language-agnostic interoperability test suite for the DFC (Data Food Consortium) standard. Tests JSON-LD serialization, schema validation, and edge cases against DFC ontology v2.0.0.

**This is a spec repo, not application code.** The canonical source of truth is `spec/tests.yaml`.

## Key files

| Path | Purpose |
|------|---------|
| `spec/tests.yaml` | Canonical test definitions (47 tests across 3 categories) |
| `fixtures/**/*.jsonld` | Shared JSON-LD test data |
| `dfc_interop_test_spec.md` | Human-readable DFC test spec |
| `jsonld_interop_test_spec.md` | Human-readable generic JSON-LD test spec |
| `implementations/python/` | Reference Python implementation |
| `implementations/CONTRACT.md` | Spec for new platform implementations |
| `scripts/validate_results.py` | Cross-platform JUnit XML comparator |

## Running tests

```bash
cd implementations/python
./run_tests.sh
# or manually:
pip install -e . && pytest tests/ -v --junitxml=../../results/python-rdflib/results.xml
```

## Branching

- `main` — current development (DFC v2.0.0)
- `v1.16.0` — legacy release (old namespaces)
- `v2.0.0` — release branch for current version

When updating ontology versions: update `spec/tests.yaml` version fields, all fixture `@context` URLs, and namespace references in `dfc_interop_test_spec.md`.

## Test ID conventions

- IDs like `SER-001`, `SCH-003`, `EDG-012` are **permanent and never reassigned**
- New tests get the next sequential number in their category
- `classname` in JUnit XML must match the test ID exactly

## Adding a new platform

1. Create `implementations/{platform-name}/`
2. Implement the adapter interface (see `implementations/CONTRACT.md`)
3. Load fixtures from `/fixtures/`, execute tests from `spec/tests.yaml`
4. Output JUnit XML to `/results/{platform-name}/results.xml`

## DFC ontology v2.0.0 changes from v1.16.0

- `Enterprise` renamed to `Organization`
- All namespaces moved from `static.datafoodconsortium.org` to `w3id.org/dfc/ontology/v2.0.0/`
- Context URL: `https://w3id.org/dfc/ontology/context/context_2.0.0.json`
- New classes: `Variant`, `ProductOption`, `TemplateSaleSession`, `Certification`
- New properties: `certifies`/`isCertifiedBy`, `hasGeoJsonFeature`, `occursAt` (iCal)

## Gotchas

- `fixtures/invalid/malformed_json.jsonld` is intentionally invalid JSON — don't "fix" it
- Some test inputs are inline in `tests.yaml` (`fixture: null` with `inline_inputs`), not fixture files
- The JSON-LD interop tests (`jsonld_interop_test_spec.md`) are generic — they don't use DFC namespaces
- `results/` directory is empty until platform implementations run and emit JUnit XML
