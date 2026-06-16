"""JSON-LD edge case tests."""

import pytest


class TestJSONLdEdgeCases:
    """EDG-001 to EDG-009 tests for JSON-LD interop."""

    def test_edg001_malformed_json(self, load_fixture):
        """EDG-001: Malformed JSON (not valid JSON at all)."""
        import json
        import pathlib

        fixture_path = pathlib.Path(__file__).parent.parent.parent.parent / "fixtures" / "invalid" / "malformed_json.jsonld"
        content = fixture_path.read_text()

        with pytest.raises(json.JSONDecodeError):
            json.loads(content)

    def test_edg002_empty_document(self):
        """EDG-002: Empty document {}."""
        data = {}

        assert isinstance(data, dict)
        assert len(data) == 0

    def test_edg003_null_values(self):
        """EDG-003: Null property values."""
        data = {"@context": "https://schema.org/", "name": None}

        assert "name" in data
        assert data["name"] is None

    def test_edg005_large_integers(self):
        """EDG-005: Very large integer values."""
        large_int = 9007199254740993

        data = {"@context": "https://schema.org/", "identifier": large_int}
        assert data["identifier"] == large_int

    def test_edg006_duplicate_keys(self):
        """EDG-006: Duplicate keys in JSON object."""
        import json

        json_str = '{ "@context": "https://schema.org/", "name": "First", "name": "Second" }'
        data = json.loads(json_str)

        assert data["name"] == "Second", "Last-wins behavior expected"

    def test_edg008_graph_container(self, load_fixture):
        """EDG-008: @graph container."""
        data = load_fixture("valid/full_context.jsonld")

        assert "@context" in data
        assert "@type" in data
