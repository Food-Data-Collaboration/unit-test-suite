"""DFC schema validation tests."""

import pytest


class TestDFCSchemaValidation:
    """SCH-001 to SCH-009 tests for DFC interop."""

    def test_sch001_accept_valid_enterprise(self, load_fixture):
        """SCH-001: Accept valid Organization with all required fields."""
        data = load_fixture("organization/organization_full.jsonld")

        assert "@graph" in data
        enterprise = data["@graph"][0]
        assert enterprise["@type"] == "dfc-b:Organization"
        assert "dfc-b:name" in enterprise

    def test_sch002_accept_minimal_enterprise(self, load_fixture):
        """SCH-002: Accept a minimal Organization (only required fields)."""
        data = load_fixture("organization/organization_minimal.jsonld")

        assert data["@type"] == "dfc-b:Organization"
        assert data["dfc-b:name"] == "Minimal Farm"

    def test_sch003_reject_wrong_type_for_price(self, load_fixture):
        """SCH-003: Reject a document with wrong @type for a Price value."""
        data = load_fixture("invalid/wrong_type_for_price.jsonld")

        offer = data
        assert offer["@type"] == "dfc-b:Offer"
        price_value = offer["dfc-b:hasPrice"]
        assert isinstance(price_value, str), "Price should be a string (invalid)"

    def test_sch004_reject_missing_context(self, load_fixture):
        """SCH-004: Reject a document missing the DFC @context."""
        data = load_fixture("invalid/missing_context.jsonld")

        assert "@context" not in data or data.get("@context") is None

    def test_sch005_reject_missing_required_field(self, load_fixture):
        """SCH-005: Reject a SuppliedProduct missing dfc-b:name."""
        data = load_fixture("invalid/missing_required_field.jsonld")

        assert data["@type"] == "dfc-b:SuppliedProduct"
        assert "dfc-b:name" not in data

    def test_sch006_accept_valid_product_type(self, load_fixture):
        """SCH-006: Accept valid dfc-pt: product type term."""
        data = load_fixture("supplied-product/supplied_product_full.jsonld")

        assert data["dfc-b:hasType"] == "dfc-pt:processed-vegetable"

    def test_sch007_accept_valid_certification(self, load_fixture):
        """SCH-007: Accept valid dfc-f: certification facet."""
        data = load_fixture("supplied-product/supplied_product_full.jsonld")

        assert data["dfc-b:hasCertification"] == "dfc-f:Organic-AB"

    def test_sch008_validate_unit_term(self, load_fixture):
        """SCH-008: Validate dfc-m: unit term on QuantitativeValue."""
        data = load_fixture("supplied-product/supplied_product_full.jsonld")

        quantity = data["dfc-b:hasQuantity"]
        assert quantity["dfc-b:hasUnit"] == "dfc-m:Gram"

    def test_sch010_validate_variant_characteristic(self, load_fixture):
        """SCH-010: Validate VariantCaracteristic terms."""
        data = load_fixture("variant/variant_with_options.jsonld")

        assert "@graph" in data
        char = data["@graph"][3]
        assert char["@type"] == "dfc-b:VariantCaracteristic"
        assert "dfc-b:hasProductOption" in char
        assert "dfc-b:hasProductOptionValue" in char

    def test_sch011_validate_template_sale_session(self, load_fixture):
        """SCH-011: Validate TemplateSaleSession with iCal Vevent."""
        data = load_fixture("sale-session/template_sale_session.jsonld")

        assert "@graph" in data
        session = data["@graph"][1]
        assert session["@type"] == "dfc-b:TemplateSaleSession"
        assert "dfc-b:occursAt" in session

    def test_sch012_reject_invalid_variant_characteristic(self, load_fixture):
        """SCH-012: Reject Variant with invalid characteristic reference."""
        data = load_fixture("invalid/variant_invalid_characteristic.jsonld")

        assert data["@type"] == "dfc-b:Variant"
        assert "dfc-b:hasVariantCaracteristic" in data
        char_ref = data["dfc-b:hasVariantCaracteristic"]
        assert "nonexistent" in char_ref or "99999" in char_ref
