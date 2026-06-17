# frozen_string_literal: true

require "spec_helper"

RSpec.describe "DFC Serialization" do
  describe "SER-001" do
    it "parses a DFC Organization document" do
      data = load_fixture("organization/organization_full.jsonld")

      expect(data).to have_key("@graph")
      org = data["@graph"][0]
      expect(org["@type"]).to eq("dfc-b:Organization")
      expect(org["dfc-b:name"]).to eq("Fred's Farm")
      expect(org).to have_key("dfc-b:supplies")
      expect(org).to have_key("dfc-b:hasAddress")
    end
  end

  describe "SER-002" do
    it "parses a SuppliedProduct with QuantitativeValue" do
      data = load_fixture("supplied-product/supplied_product_full.jsonld")

      expect(data["@type"]).to eq("dfc-b:SuppliedProduct")
      quantity = data["dfc-b:hasQuantity"]
      expect(quantity["@type"]).to eq("dfc-b:QuantitativeValue")
      expect(quantity["dfc-b:hasUnit"]).to eq("dfc-m:Gram")
      expect(quantity["dfc-b:value"]).to eq(100.0)
    end
  end

  describe "SER-003" do
    it "parses a CatalogItem linked to an Offer with Price" do
      data = load_fixture("catalog/catalog_item.jsonld")

      expect(data).to have_key("@graph")
      catalog_item = data["@graph"][0]
      expect(catalog_item["@type"]).to eq("dfc-b:CatalogItem")

      offer = data["@graph"][1]
      expect(offer["@type"]).to eq("dfc-b:Offer")
      price = offer["dfc-b:hasPrice"]
      expect(price["dfc-b:value"]).to eq(4.95)
      expect(price["dfc-b:VATrate"]).to eq(5.0)
      expect(price["dfc-b:hasUnit"]).to eq("dfc-m:GBP")
    end
  end

  describe "SER-004" do
    it "parses an Order with OrderLines and PickUpOption" do
      data = load_fixture("order/order_pickup.jsonld")

      expect(data).to have_key("@graph")
      order = data["@graph"][0]
      expect(order["@type"]).to eq("dfc-b:Order")
      expect(order).to have_key("dfc-b:date")
      expect(order["dfc-b:date"]).to eq("2024-06-01T10:00:00+01:00")
    end
  end

  describe "SER-005" do
    it "parses a Person document" do
      data = load_fixture("person/person.jsonld")

      expect(data["@type"]).to eq("dfc-b:Person")
      expect(data["dfc-b:firstName"]).to eq("Ali")
      expect(data["dfc-b:familyName"]).to eq("Khan")
      expect(data).to have_key("dfc-b:hasAddress")
    end
  end

  describe "SER-006" do
    it "parses a paginated @graph list of Organizations" do
      data = load_fixture("organization/organization_list.jsonld")

      expect(data).to have_key("@graph")
      expect(data["@graph"].length).to eq(3)
      data["@graph"].each do |node|
        expect(node["@type"]).to eq("dfc-b:Organization")
        expect(node["@id"]).to start_with("http://")
      end
    end
  end

  describe "SER-012" do
    it "parses a DFC Organization document (renamed from Enterprise)" do
      data = load_fixture("organization/organization_full.jsonld")

      expect(data).to have_key("@graph")
      org = data["@graph"][0]
      expect(org["@type"]).to eq("dfc-b:Organization")
      expect(org["dfc-b:name"]).to eq("Fred's Farm")
      expect(org).to have_key("dfc-b:supplies")
      expect(org).to have_key("dfc-b:hasAddress")
    end
  end

  describe "SER-013" do
    it "parses Variant with ProductOption and VariantCaracteristic" do
      data = load_fixture("variant/variant_with_options.jsonld")

      expect(data).to have_key("@graph")
      variant = data["@graph"][1]
      expect(variant["@type"]).to eq("dfc-b:Variant")
      expect(variant).to have_key("dfc-b:hasVariantCaracteristic")

      char = data["@graph"][3]
      expect(char["@type"]).to eq("dfc-b:VariantCaracteristic")
      expect(char).to have_key("dfc-b:hasProductOption")
      expect(char).to have_key("dfc-b:hasProductOptionValue")
    end
  end

  describe "SER-014" do
    it "parses TemplateSaleSession with iCal Vevent" do
      data = load_fixture("sale-session/template_sale_session.jsonld")

      expect(data).to have_key("@graph")
      org = data["@graph"][0]
      expect(org["@type"]).to eq("dfc-b:Organization")
      expect(org).to have_key("dfc-b:hasTemplateSaleSession")

      session = data["@graph"][1]
      expect(session["@type"]).to eq("dfc-b:TemplateSaleSession")
      expect(session).to have_key("dfc-b:occursAt")
    end
  end

  describe "SER-015" do
    it "parses Organization with certifies/isCertifiedBy" do
      data = load_fixture("organization/organization_certified.jsonld")

      expect(data).to have_key("@graph")
      org = data["@graph"][0]
      expect(org["@type"]).to eq("dfc-b:Organization")
      expect(org).to have_key("dfc-b:certifies")

      cert = data["@graph"][1]
      expect(cert["@type"]).to eq("dfc-b:Certification")
      expect(cert["dfc-b:operatorid"]).to eq("CERT-AB-2026-001")
      expect(cert["dfc-b:certificationScore"]).to eq("A+")
      expect(cert).to have_key("dfc-b:isCertifiedBy")
    end
  end

  describe "SER-016" do
    it "parses PhysicalPlace with GeoJSON feature" do
      data = load_fixture("physical-place/place_with_geojson.jsonld")

      expect(data["@type"]).to eq("dfc-b:PhysicalPlace")
      expect(data).to have_key("dfc-b:hasGeoJsonFeature")
      feature = data["dfc-b:hasGeoJsonFeature"]
      expect(feature).to have_key("https://purl.org/geojson/vocab#geometry")
    end
  end
end
