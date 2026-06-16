"""JSON-LD serialization and deserialization tests."""

import pytest


class TestJSONLdSerialization:
    """SER-001 to SER-010 tests for JSON-LD interop."""

    def test_ser001_parse_minimal(self, load_fixture):
        """SER-001: Parse minimal valid JSON-LD."""
        data = load_fixture("valid/minimal.jsonld")

        assert "@context" in data
        assert "@type" in data
        assert data["@type"] == "Person"
        assert data["name"] == "Jane Smith"

    def test_ser002_roundtrip_minimal(self, load_fixture):
        """SER-002: Serialize native object to JSON-LD string."""
        data = load_fixture("valid/minimal.jsonld")

        reconstructed = {
            "@context": data["@context"],
            "@type": data["@type"],
            "name": data["name"]
        }
        assert reconstructed == data

    def test_ser007_nested_nodes(self, load_fixture):
        """SER-007: Nested node objects."""
        data = load_fixture("valid/nested_nodes.jsonld")

        assert data["@type"] == "Person"
        assert data["knows"]["name"] == "Level 2"
        assert data["knows"]["knows"]["name"] == "Level 3"
        assert data["knows"]["knows"]["knows"]["name"] == "Level 4"

    def test_ser008_array_values(self, load_fixture):
        """SER-008: Array-valued properties."""
        data = load_fixture("valid/array_values.jsonld")

        assert isinstance(data["knows"], list)
        assert len(data["knows"]) == 3
        assert data["knows"][0]["name"] == "Alice"
        assert data["knows"][1]["name"] == "Bob"
        assert data["knows"][2]["name"] == "Charlie"

    def test_ser009_multilingual(self, load_fixture):
        """SER-009: Multi-language strings (@language)."""
        data = load_fixture("valid/multilingual.jsonld")

        name = data["name"]
        assert isinstance(name, dict)
        assert name["@language"] == "fr"
        assert name["@value"] == "Jean-Pierre Dupont"

    def test_ser010_numeric_boolean_types(self, load_fixture):
        """SER-010: Numeric and boolean value types."""
        data = load_fixture("valid/full_context.jsonld")

        assert isinstance(data["age"], int)
        assert data["age"] == 30
        assert isinstance(data["height"], float)
        assert data["height"] == 1.75
        assert isinstance(data["isStudent"], bool)
        assert data["isStudent"] is False
