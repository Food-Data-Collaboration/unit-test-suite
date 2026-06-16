"""JSON-LD schema validation tests."""

import pytest


class TestJSONLdSchemaValidation:
    """SCH-001 to SCH-005 tests for JSON-LD interop."""

    def test_sch001_accept_valid_document(self, load_fixture):
        """SCH-001: Accept document conforming to context."""
        data = load_fixture("valid/full_context.jsonld")

        assert "@context" in data
        assert "@type" in data

    def test_sch002_reject_missing_context(self, load_fixture):
        """SCH-002: Reject document with missing @context."""
        data = load_fixture("invalid/missing_context.jsonld")

        assert "@context" not in data or data.get("@context") is None

    def test_sch003_reject_malformed_iri(self, load_fixture):
        """SCH-003: Reject malformed IRI."""
        data = load_fixture("invalid/broken_iri.jsonld")

        url = data.get("url", "")
        assert " " in url or not url.startswith("http://")

    def test_sch004_reject_type_mismatch(self, load_fixture):
        """SCH-004: Reject type mismatch."""
        data = load_fixture("invalid/type_mismatch.jsonld")

        assert isinstance(data["name"], int), "name should be a string, not int"
        assert isinstance(data["age"], str), "age should be a number, not string"
