"""DFC serialization and deserialization tests."""

import pytest


class TestDFCSerialization:
    """SER-001 to SER-011 tests for DFC interop."""

    def test_ser001_parse_enterprise(self, load_fixture):
        """SER-001: Parse a DFC Organization document."""
        data = load_fixture("organization/organization_full.jsonld")

        assert "@graph" in data
        enterprise = data["@graph"][0]
        assert enterprise["@type"] == "dfc-b:Organization"
        assert enterprise["dfc-b:name"] == "Fred's Farm"
        assert "dfc-b:supplies" in enterprise
        assert "dfc-b:hasAddress" in enterprise

    def test_ser002_parse_supplied_product(self, load_fixture):
        """SER-002: Parse a SuppliedProduct with QuantitativeValue."""
        data = load_fixture("supplied-product/supplied_product_full.jsonld")

        assert data["@type"] == "dfc-b:SuppliedProduct"
        quantity = data["dfc-b:hasQuantity"]
        assert quantity["@type"] == "dfc-b:QuantitativeValue"
        assert quantity["dfc-b:hasUnit"] == "dfc-m:Gram"
        assert quantity["dfc-b:value"] == 100.0

    def test_ser003_parse_catalog_item(self, load_fixture):
        """SER-003: Parse a CatalogItem linked to an Offer with Price."""
        data = load_fixture("catalog/catalog_item.jsonld")

        assert "@graph" in data
        catalog_item = data["@graph"][0]
        assert catalog_item["@type"] == "dfc-b:CatalogItem"

        offer = data["@graph"][1]
        assert offer["@type"] == "dfc-b:Offer"
        price = offer["dfc-b:hasPrice"]
        assert price["dfc-b:value"] == 4.95
        assert price["dfc-b:VATrate"] == 5.0
        assert price["dfc-b:hasUnit"] == "dfc-m:GBP"

    def test_ser004_parse_order_pickup(self, load_fixture):
        """SER-004: Parse an Order with OrderLines and PickUpOption."""
        data = load_fixture("order/order_pickup.jsonld")

        assert "@graph" in data
        order = data["@graph"][0]
        assert order["@type"] == "dfc-b:Order"
        assert "dfc-b:date" in order
        assert "2024-06-01T10:00:00+01:00" == order["dfc-b:date"]

    def test_ser005_parse_person(self, load_fixture):
        """SER-005: Parse a Person document."""
        data = load_fixture("person/person.jsonld")

        assert data["@type"] == "dfc-b:Person"
        assert data["dfc-b:firstName"] == "Ali"
        assert data["dfc-b:familyName"] == "Khan"
        assert "dfc-b:hasAddress" in data

    def test_ser006_parse_enterprise_list(self, load_fixture):
        """SER-006: Parse a paginated @graph list of Organizations."""
        data = load_fixture("organization/organization_list.jsonld")

        assert "@graph" in data
        assert len(data["@graph"]) == 3
        for node in data["@graph"]:
            assert node["@type"] == "dfc-b:Organization"
            assert node["@id"].startswith("http://")

    def test_ser008_parse_variant(self, load_fixture):
        """SER-008: Parse product with hasVariant/isVariantOf."""
        data = load_fixture("supplied-product/supplied_product_variant.jsonld")

        assert "@graph" in data
        parent = data["@graph"][0]
        assert "dfc-b:hasVariant" in parent
        assert len(parent["dfc-b:hasVariant"]) == 2

        variant = data["@graph"][1]
        assert variant["dfc-b:isVariantOf"] == parent["@id"]

    def test_ser009_parse_transformation(self, load_fixture):
        """SER-009: Parse AsPlannedTransformation flow."""
        data = load_fixture("supplied-product/supplied_product_transformation.jsonld")

        assert "@graph" in data
        product = data["@graph"][0]
        assert "dfc-b:asPlannedProductionFlow" in product

        transformation = data["@graph"][1]
        assert transformation["@type"] == "dfc-b:AsPlannedTransformation"
        assert "dfc-b:hasInput" in transformation
        assert "dfc-b:hasOutput" in transformation

    def test_ser010_parse_order_delivery(self, load_fixture):
        """SER-010: Parse an Order with DeliveryOption."""
        data = load_fixture("order/order_delivery.jsonld")

        assert "@graph" in data
        order = data["@graph"][0]
        assert order["@type"] == "dfc-b:Order"
        assert "dfc-b:selects" in order

    def test_ser011_parse_order_payment(self, load_fixture):
        """SER-011: Parse an Order with PaymentMethod."""
        data = load_fixture("order/order_with_payment.jsonld")

        assert "@graph" in data
        payment = data["@graph"][2]
        assert payment["@type"] == "dfc-b:PaymentMethod"
        assert "dfc-b:hasPrice" in payment

    def test_ser012_parse_organization(self, load_fixture):
        """SER-012: Parse a DFC Organization document (renamed from Enterprise)."""
        data = load_fixture("organization/organization_full.jsonld")

        assert "@graph" in data
        org = data["@graph"][0]
        assert org["@type"] == "dfc-b:Organization"
        assert org["dfc-b:name"] == "Fred's Farm"
        assert "dfc-b:supplies" in org
        assert "dfc-b:hasAddress" in org

    def test_ser013_parse_variant_with_options(self, load_fixture):
        """SER-013: Parse Variant with ProductOption and VariantCaracteristic."""
        data = load_fixture("variant/variant_with_options.jsonld")

        assert "@graph" in data
        variant = data["@graph"][1]
        assert variant["@type"] == "dfc-b:Variant"
        assert "dfc-b:hasVariantCaracteristic" in variant

        char = data["@graph"][3]
        assert char["@type"] == "dfc-b:VariantCaracteristic"
        assert "dfc-b:hasProductOption" in char
        assert "dfc-b:hasProductOptionValue" in char

    def test_ser014_parse_template_sale_session(self, load_fixture):
        """SER-014: Parse TemplateSaleSession with iCal Vevent."""
        data = load_fixture("sale-session/template_sale_session.jsonld")

        assert "@graph" in data
        org = data["@graph"][0]
        assert org["@type"] == "dfc-b:Organization"
        assert "dfc-b:hasTemplateSaleSession" in org

        session = data["@graph"][1]
        assert session["@type"] == "dfc-b:TemplateSaleSession"
        assert "dfc-b:occursAt" in session

    def test_ser015_parse_organization_certified(self, load_fixture):
        """SER-015: Parse Organization with certifies/isCertifiedBy."""
        data = load_fixture("organization/organization_certified.jsonld")

        assert "@graph" in data
        org = data["@graph"][0]
        assert org["@type"] == "dfc-b:Organization"
        assert "dfc-b:certifies" in org

        cert = data["@graph"][1]
        assert cert["@type"] == "dfc-b:Certification"
        assert cert["dfc-b:operatorid"] == "CERT-AB-2026-001"
        assert cert["dfc-b:certificationScore"] == "A+"
        assert "dfc-b:isCertifiedBy" in cert

    def test_ser016_parse_physical_place_geojson(self, load_fixture):
        """SER-016: Parse PhysicalPlace with GeoJSON feature."""
        data = load_fixture("physical-place/place_with_geojson.jsonld")

        assert data["@type"] == "dfc-b:PhysicalPlace"
        assert "dfc-b:hasGeoJsonFeature" in data
        feature = data["dfc-b:hasGeoJsonFeature"]
        assert "https://purl.org/geojson/vocab#geometry" in feature
        assert "https://purl.org/geojson/vocab#coordinates" in feature["https://purl.org/geojson/vocab#geometry"]
