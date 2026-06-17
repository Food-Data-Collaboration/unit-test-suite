<?php

declare(strict_types=1);

namespace DfcTest\Tests;

class DfcSerializationTest extends BaseTestCase
{
    /** @test SER-001 */
    public function test_SER001_parses_dfc_organization_document(): void
    {
        $data = $this->loadFixture('organization/organization_full.jsonld');

        $this->assertArrayHasKey('@graph', $data);
        $org = $data['@graph'][0];
        $this->assertSame('dfc-b:Organization', $org['@type']);
        $this->assertSame("Fred's Farm", $org['dfc-b:name']);
        $this->assertArrayHasKey('dfc-b:supplies', $org);
        $this->assertArrayHasKey('dfc-b:hasAddress', $org);
    }

    /** @test SER-002 */
    public function test_SER002_parses_supplied_product_with_quantitative_value(): void
    {
        $data = $this->loadFixture('supplied-product/supplied_product_full.jsonld');

        $this->assertSame('dfc-b:SuppliedProduct', $data['@type']);
        $quantity = $data['dfc-b:hasQuantity'];
        $this->assertSame('dfc-b:QuantitativeValue', $quantity['@type']);
        $this->assertSame('dfc-m:Gram', $quantity['dfc-b:hasUnit']);
        $this->assertSame(100.0, $quantity['dfc-b:value']);
    }

    /** @test SER-003 */
    public function test_SER003_parses_catalog_item_with_offer_and_price(): void
    {
        $data = $this->loadFixture('catalog/catalog_item.jsonld');

        $this->assertArrayHasKey('@graph', $data);
        $catalogItem = $data['@graph'][0];
        $this->assertSame('dfc-b:CatalogItem', $catalogItem['@type']);

        $offer = $data['@graph'][1];
        $this->assertSame('dfc-b:Offer', $offer['@type']);
        $price = $offer['dfc-b:hasPrice'];
        $this->assertSame(4.95, $price['dfc-b:value']);
        $this->assertSame(5.0, $price['dfc-b:VATrate']);
        $this->assertSame('dfc-m:GBP', $price['dfc-b:hasUnit']);
    }

    /** @test SER-012 */
    public function test_SER012_parses_organization_document_v2(): void
    {
        $data = $this->loadFixture('organization/organization_full.jsonld');

        $this->assertArrayHasKey('@graph', $data);
        $org = $data['@graph'][0];
        $this->assertSame('dfc-b:Organization', $org['@type']);
        $this->assertSame("Fred's Farm", $org['dfc-b:name']);
    }

    /** @test SER-013 */
    public function test_SER013_parses_variant_with_product_option(): void
    {
        $data = $this->loadFixture('variant/variant_with_options.jsonld');

        $this->assertArrayHasKey('@graph', $data);
        $variant = $data['@graph'][1];
        $this->assertSame('dfc-b:Variant', $variant['@type']);
        $this->assertArrayHasKey('dfc-b:hasVariantCaracteristic', $variant);

        $char = $data['@graph'][3];
        $this->assertSame('dfc-b:VariantCaracteristic', $char['@type']);
        $this->assertArrayHasKey('dfc-b:hasProductOption', $char);
        $this->assertArrayHasKey('dfc-b:hasProductOptionValue', $char);
    }

    /** @test SER-014 */
    public function test_SER014_parses_template_sale_session_with_ical(): void
    {
        $data = $this->loadFixture('sale-session/template_sale_session.jsonld');

        $this->assertArrayHasKey('@graph', $data);
        $org = $data['@graph'][0];
        $this->assertSame('dfc-b:Organization', $org['@type']);
        $this->assertArrayHasKey('dfc-b:hasTemplateSaleSession', $org);

        $session = $data['@graph'][1];
        $this->assertSame('dfc-b:TemplateSaleSession', $session['@type']);
        $this->assertArrayHasKey('dfc-b:occursAt', $session);
    }

    /** @test SER-015 */
    public function test_SER015_parses_organization_with_certification(): void
    {
        $data = $this->loadFixture('organization/organization_certified.jsonld');

        $this->assertArrayHasKey('@graph', $data);
        $org = $data['@graph'][0];
        $this->assertSame('dfc-b:Organization', $org['@type']);
        $this->assertArrayHasKey('dfc-b:certifies', $org);

        $cert = $data['@graph'][1];
        $this->assertSame('dfc-b:Certification', $cert['@type']);
        $this->assertSame('CERT-AB-2026-001', $cert['dfc-b:operatorid']);
        $this->assertSame('A+', $cert['dfc-b:certificationScore']);
        $this->assertArrayHasKey('dfc-b:isCertifiedBy', $cert);
    }

    /** @test SER-016 */
    public function test_SER016_parses_physical_place_with_geojson(): void
    {
        $data = $this->loadFixture('physical-place/place_with_geojson.jsonld');

        $this->assertSame('dfc-b:PhysicalPlace', $data['@type']);
        $this->assertArrayHasKey('dfc-b:hasGeoJsonFeature', $data);
        $feature = $data['dfc-b:hasGeoJsonFeature'];
        $this->assertArrayHasKey('https://purl.org/geojson/vocab#geometry', $feature);
    }
}
