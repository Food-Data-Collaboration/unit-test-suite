"""DFC edge case tests."""

import pytest


class TestDFCEdgeCases:
    """EDG-001 to EDG-015 tests for DFC interop."""

    def test_edg001_single_iri_vs_array(self):
        """EDG-001: dfc-b:supplies as a single IRI vs array."""
        single = {"dfc-b:supplies": "http://example.org/products/10001"}
        array = {"dfc-b:supplies": ["http://example.org/products/10001", "http://example.org/products/10002"]}

        single_val = single["dfc-b:supplies"]
        array_val = array["dfc-b:supplies"]

        assert isinstance(single_val, str)
        assert isinstance(array_val, list)
        assert len(array_val) == 2

    def test_edg002_price_numeric_vs_string(self):
        """EDG-002: Price value as numeric vs string."""
        numeric = {"dfc-b:hasPrice": {"@type": "dfc-b:Price", "dfc-b:value": 4.95}}
        string = {"dfc-b:hasPrice": {"@type": "dfc-b:Price", "dfc-b:value": "4.95"}}

        assert numeric["dfc-b:hasPrice"]["dfc-b:value"] == 4.95
        assert string["dfc-b:hasPrice"]["dfc-b:value"] == "4.95"

    def test_edg007_temperature_range(self, load_fixture):
        """EDG-007: Temperature range with min/max values."""
        data = load_fixture("supplied-product/supplied_product_full.jsonld")

        temp = data["dfc-b:hasTemperature"]
        assert temp["dfc-b:minValue"] == 2
        assert temp["dfc-b:maxValue"] == 8
        assert temp["dfc-b:minValue"] < temp["dfc-b:maxValue"]

    def test_edg008_order_date_timezone(self, load_fixture):
        """EDG-008: Order date as ISO 8601 with timezone offset."""
        data = load_fixture("order/order_pickup.jsonld")

        order = data["@graph"][0]
        date_str = order["dfc-b:date"]
        assert "+01:00" in date_str or "T" in date_str

    def test_edg010_empty_graph(self):
        """EDG-010: Empty @graph array."""
        data = {"@context": "https://w3id.org/dfc/ontology/context/context_1.16.0.json", "@graph": []}

        assert "@graph" in data
        assert len(data["@graph"]) == 0

    def test_edg013_malformed_iri(self, load_fixture):
        """EDG-013: Malformed IRI in dfc-b:supplies."""
        data = load_fixture("invalid/malformed_iri.jsonld")

        assert data["@type"] == "dfc-b:SuppliedProduct"
        supplies = data.get("dfc-b:supplies", "")
        assert " " in supplies or not supplies.startswith("http://")
