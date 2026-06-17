import { fixture, dfcSpec } from './helpers';

describe('DFC Serialization', () => {
  describe('SER-001', () => {
    it('parses a DFC Organization document', () => {
      const data = fixture('organization/organization_full.jsonld');

      expect(data).toHaveProperty('@graph');
      const org = data['@graph'][0];
      expect(org['@type']).toBe('dfc-b:Organization');
      expect(org['dfc-b:name']).toBe("Fred's Farm");
      expect(org).toHaveProperty('dfc-b:supplies');
      expect(org).toHaveProperty('dfc-b:hasAddress');
    });
  });

  describe('SER-002', () => {
    it('parses a SuppliedProduct with QuantitativeValue', () => {
      const data = fixture('supplied-product/supplied_product_full.jsonld');

      expect(data['@type']).toBe('dfc-b:SuppliedProduct');
      const quantity = data['dfc-b:hasQuantity'];
      expect(quantity['@type']).toBe('dfc-b:QuantitativeValue');
      expect(quantity['dfc-b:hasUnit']).toBe('dfc-m:Gram');
      expect(quantity['dfc-b:value']).toBe(100.0);
    });
  });

  describe('SER-003', () => {
    it('parses a CatalogItem linked to an Offer with Price', () => {
      const data = fixture('catalog/catalog_item.jsonld');

      expect(data).toHaveProperty('@graph');
      const catalogItem = data['@graph'][0];
      expect(catalogItem['@type']).toBe('dfc-b:CatalogItem');

      const offer = data['@graph'][1];
      expect(offer['@type']).toBe('dfc-b:Offer');
      const price = offer['dfc-b:hasPrice'];
      expect(price['dfc-b:value']).toBe(4.95);
      expect(price['dfc-b:VATrate']).toBe(5.0);
      expect(price['dfc-b:hasUnit']).toBe('dfc-m:GBP');
    });
  });

  describe('SER-012', () => {
    it('parses a DFC Organization document (renamed from Enterprise)', () => {
      const data = fixture('organization/organization_full.jsonld');

      expect(data).toHaveProperty('@graph');
      const org = data['@graph'][0];
      expect(org['@type']).toBe('dfc-b:Organization');
      expect(org['dfc-b:name']).toBe("Fred's Farm");
    });
  });

  describe('SER-013', () => {
    it('parses Variant with ProductOption and VariantCaracteristic', () => {
      const data = fixture('variant/variant_with_options.jsonld');

      expect(data).toHaveProperty('@graph');
      const variant = data['@graph'][1];
      expect(variant['@type']).toBe('dfc-b:Variant');
      expect(variant).toHaveProperty('dfc-b:hasVariantCaracteristic');

      const char = data['@graph'][3];
      expect(char['@type']).toBe('dfc-b:VariantCaracteristic');
      expect(char).toHaveProperty('dfc-b:hasProductOption');
      expect(char).toHaveProperty('dfc-b:hasProductOptionValue');
    });
  });

  describe('SER-014', () => {
    it('parses TemplateSaleSession with iCal Vevent', () => {
      const data = fixture('sale-session/template_sale_session.jsonld');

      expect(data).toHaveProperty('@graph');
      const org = data['@graph'][0];
      expect(org['@type']).toBe('dfc-b:Organization');
      expect(org).toHaveProperty('dfc-b:hasTemplateSaleSession');

      const session = data['@graph'][1];
      expect(session['@type']).toBe('dfc-b:TemplateSaleSession');
      expect(session).toHaveProperty('dfc-b:occursAt');
    });
  });

  describe('SER-015', () => {
    it('parses Organization with certifies/isCertifiedBy', () => {
      const data = fixture('organization/organization_certified.jsonld');

      expect(data).toHaveProperty('@graph');
      const org = data['@graph'][0];
      expect(org['@type']).toBe('dfc-b:Organization');
      expect(org).toHaveProperty('dfc-b:certifies');

      const cert = data['@graph'][1];
      expect(cert['@type']).toBe('dfc-b:Certification');
      expect(cert['dfc-b:operatorid']).toBe('CERT-AB-2026-001');
      expect(cert['dfc-b:certificationScore']).toBe('A+');
      expect(cert).toHaveProperty('dfc-b:isCertifiedBy');
    });
  });

  describe('SER-016', () => {
    it('parses PhysicalPlace with GeoJSON feature', () => {
      const data = fixture('physical-place/place_with_geojson.jsonld');

      expect(data['@type']).toBe('dfc-b:PhysicalPlace');
      expect(data).toHaveProperty('dfc-b:hasGeoJsonFeature');
      const feature = data['dfc-b:hasGeoJsonFeature'];
      expect(feature).toHaveProperty('https://purl.org/geojson/vocab#geometry');
    });
  });
});
