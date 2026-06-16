# DFC Standard — Interoperability Test Specification

**Version:** 2.0.0
**Status:** Draft
**Last Updated:** 2026-06-17
**Ontology version tested:** 2.0.0
**Context URL:** `https://w3id.org/dfc/ontology/context/context_2.0.0.json`

---

## Purpose

This document defines the canonical test suite for platforms implementing the Data Food Consortium (DFC) Standard. All participating platforms MUST pass mandatory tests and report results in JUnit XML format. The spec covers:

- JSON-LD serialization & deserialization of DFC ontology types
- Schema validation against the DFC business ontology (`dfc-b:`)
- Edge cases & error handling specific to DFC data structures
- Cross-platform identifier reconciliation

---

## Conventions

- **MUST** — mandatory; failure counts as non-compliance
- **SHOULD** — strongly recommended
- **MAY** — optional; mark as `skipped` rather than omitting from results
- All fixture files live in `/fixtures/` in the shared repository
- Test IDs are stable and permanent; they are never reused or reassigned
- Platforms MUST use the shared fixture files exactly as provided

---

## DFC Ontology Prefixes

All test fixtures use these namespace prefixes, as defined in `context_2.0.0.json`:

| Prefix | Namespace |
|---|---|
| `dfc-b:` | `http://w3id.org/dfc/ontology/v2.0.0/src/DFC_BusinessOntology.owl#` |
| `dfc-p:` | `http://w3id.org/dfc/ontology/v2.0.0/src/DFC_ProductOntology.owl#` |
| `dfc-t:` | `http://w3id.org/dfc/ontology/v2.0.0/src/DFC_TechnicalOntology.owl#` |
| `dfc-m:` | `http://w3id.org/dfc/taxonomies/v2.0.0/measures.rdf#` |
| `dfc-pt:` | `http://w3id.org/dfc/taxonomies/v2.0.0/productTypes.rdf#` |
| `dfc-f:` | `http://w3id.org/dfc/taxonomies/v2.0.0/facets.rdf#` |

---

## Repository Structure

```
/spec
  dfc_interop_test_spec.md       ← this document
/fixtures
  /enterprise
    enterprise_full.jsonld       ← Enterprise with address, products, catalog
    enterprise_minimal.jsonld    ← Enterprise with required fields only
    enterprise_list.jsonld       ← @graph with multiple Enterprises
  /supplied-product
    supplied_product_full.jsonld ← SuppliedProduct with all optional fields
    supplied_product_variant.jsonld ← Product with isVariantOf / hasVariant
    supplied_product_transformation.jsonld ← Product with AsPlannedTransformation
  /catalog
    catalog_item.jsonld          ← CatalogItem with linked Offer
    catalog_list.jsonld          ← @graph list of CatalogItems
  /offer
    offer_with_price.jsonld      ← Offer with Price and VATrate
    offer_with_customer_category.jsonld ← Offer scoped to CustomerCategory
  /order
    order_pickup.jsonld          ← Order with PickUpOption
    order_delivery.jsonld        ← Order with DeliveryOption
    order_with_payment.jsonld    ← Order with PaymentMethod
  /person
    person.jsonld
  /invalid
    missing_context.jsonld
    wrong_type_for_price.jsonld
    missing_required_field.jsonld
    malformed_iri.jsonld
/results
  /{platform-name}/results.xml
```

---

## Test Case Format

| Field | Description |
|---|---|
| **ID** | Stable unique identifier |
| **Category** | `serialization`, `schema`, or `edge-case` |
| **Priority** | `mandatory` or `optional` |
| **Fixture** | Path relative to `/fixtures/` |
| **Action** | What the platform must do |
| **Expected Result** | Pass/fail criteria |

---

## 1. Serialization & Deserialization

### SER-001 — Parse a DFC Enterprise document

| | |
|---|---|
| **ID** | SER-001 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `enterprise/enterprise_full.jsonld` |
| **Action** | Parse the fixture; access `@type`, `dfc-b:name`, `dfc-b:supplies`, and the nested `dfc-b:Address` |
| **Expected Result** | All fields accessible without error; `@type` resolves to `dfc-b:Enterprise` |

**Fixture** (`enterprise/enterprise_full.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@graph": [
    {
      "@id": "http://example.org/api/dfc/Enterprises/10000",
      "@type": "dfc-b:Enterprise",
      "dfc-b:name": "Fred's Farm",
      "dfc-b:hasDescription": "A wonderful organic farm",
      "dfc-b:email": "hello@fredsfarm.example",
      "dfc-b:VATnumber": "123 456",
      "dfc-b:hasAddress": "http://example.org/api/dfc/Addresses/40000",
      "dfc-b:supplies": [
        "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001"
      ],
      "dfc-b:manages": [
        "http://example.org/api/dfc/Enterprises/10000/CatalogItems/10001"
      ]
    },
    {
      "@id": "http://example.org/api/dfc/Addresses/40000",
      "@type": "dfc-b:Address",
      "dfc-b:street": "42 Doveton Street",
      "dfc-b:postcode": "SW1A 1AA",
      "dfc-b:city": "London",
      "dfc-b:hasCountry": "GB",
      "dfc-b:latitude": 51.5014,
      "dfc-b:longitude": -0.1419
    }
  ]
}
```

---

### SER-002 — Parse a SuppliedProduct with QuantitativeValue

| | |
|---|---|
| **ID** | SER-002 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Parse the fixture; access `dfc-b:hasQuantity`, including its nested `dfc-b:hasUnit` and `dfc-b:value` |
| **Expected Result** | `dfc-b:hasUnit` resolves to `dfc-m:Gram`; `dfc-b:value` is accessible as a numeric or string value without error |

**Fixture** (`supplied-product/supplied_product_full.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@id": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001",
  "@type": "dfc-b:SuppliedProduct",
  "dfc-b:name": "Basil Pesto",
  "dfc-b:description": "Fresh basil pesto, 100g jar",
  "dfc-b:hasType": "dfc-pt:processed-vegetable",
  "dfc-b:hasQuantity": {
    "@type": "dfc-b:QuantitativeValue",
    "dfc-b:hasUnit": "dfc-m:Gram",
    "dfc-b:value": 100.0
  },
  "dfc-b:alcoholPercentage": 0.0,
  "dfc-b:lifetime": "12 months",
  "dfc-b:totalTheoreticalStock": 50.0,
  "dfc-b:hasCertification": "dfc-f:Organic-AB",
  "dfc-b:refrigerated": true,
  "dfc-b:frozen": false,
  "dfc-b:hasTemperature": {
    "@type": "dfc-b:Temperature",
    "dfc-b:hasUnit": "dfc-m:Celsius",
    "dfc-b:minValue": 2,
    "dfc-b:maxValue": 8
  }
}
```

---

### SER-003 — Parse a CatalogItem linked to an Offer with Price

| | |
|---|---|
| **ID** | SER-003 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `catalog/catalog_item.jsonld` |
| **Action** | Parse the `@graph`; navigate from `dfc-b:CatalogItem` → `dfc-b:offeredThrough` → `dfc-b:Offer` → `dfc-b:hasPrice` |
| **Expected Result** | `dfc-b:value`, `dfc-b:VATrate`, and `dfc-b:hasUnit` on the Price are all accessible |

**Fixture** (`catalog/catalog_item.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@graph": [
    {
      "@id": "http://example.org/api/dfc/Enterprises/10000/CatalogItems/10001",
      "@type": "dfc-b:CatalogItem",
      "dfc-b:references": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001",
      "dfc-b:sku": "PESTO-100",
      "dfc-b:stockLimitation": 20,
      "dfc-b:offeredThrough": "http://example.org/api/dfc/Enterprises/10000/customerCategories/10005/Offers/10001"
    },
    {
      "@id": "http://example.org/api/dfc/Enterprises/10000/customerCategories/10005/Offers/10001",
      "@type": "dfc-b:Offer",
      "dfc-b:offersTo": "http://example.org/api/dfc/Enterprises/10000/customerCategories/10005",
      "dfc-b:stockLimitation": 20,
      "dfc-b:hasPrice": {
        "@type": "dfc-b:Price",
        "dfc-b:value": 4.95,
        "dfc-b:VATrate": 5.0,
        "dfc-b:hasUnit": "dfc-m:GBP"
      }
    }
  ]
}
```

---

### SER-004 — Parse an Order with OrderLines and PickUpOption

| | |
|---|---|
| **ID** | SER-004 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `order/order_pickup.jsonld` |
| **Action** | Parse the `@graph`; navigate from `dfc-b:Order` → `dfc-b:hasPart` (array) → `dfc-b:OrderLine`, and `dfc-b:selects` → `dfc-b:PickUpOption` → `dfc-b:pickedUpAt` → `dfc-b:PhysicalPlace` |
| **Expected Result** | All nested objects accessible; `dfc-b:date` on Order is parseable as an ISO 8601 datetime |

**Fixture** (`order/order_pickup.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@graph": [
    {
      "@id": "http://example.org/api/dfc/order/order1",
      "@type": "dfc-b:Order",
      "dfc-b:orderNumber": "0001",
      "dfc-b:date": "2024-06-01T10:00:00+01:00",
      "dfc-b:discount": 0,
      "dfc-b:hasPart": ["http://example.org/api/dfc/orderline/line1"],
      "dfc-b:orderedBy": "http://example.org/api/dfc/persons/person1",
      "dfc-b:selects": "http://example.org/api/dfc/pickupOption/pickup1"
    },
    {
      "@id": "http://example.org/api/dfc/orderline/line1",
      "@type": "dfc-b:OrderLine",
      "dfc-b:quantity": 4,
      "dfc-b:concerns": "http://example.org/api/dfc/Enterprises/10000/customerCategories/10005/Offers/10001",
      "dfc-b:partOf": "http://example.org/api/dfc/order/order1"
    },
    {
      "@id": "http://example.org/api/dfc/pickupOption/pickup1",
      "@type": "dfc-b:PickUpOption",
      "dfc-b:pickedUpAt": "http://example.org/api/dfc/physicalPlace/place1"
    },
    {
      "@id": "http://example.org/api/dfc/physicalPlace/place1",
      "@type": "dfc-b:PhysicalPlace",
      "dfc-b:hasAddress": {
        "@type": "dfc-b:Address",
        "dfc-b:street": "10 Market Lane",
        "dfc-b:city": "Bristol",
        "dfc-b:postcode": "BS1 1AA",
        "dfc-b:hasCountry": "GB"
      }
    }
  ]
}
```

---

### SER-005 — Parse a Person document

| | |
|---|---|
| **ID** | SER-005 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `person/person.jsonld` |
| **Action** | Parse the fixture; access `dfc-b:firstName`, `dfc-b:familyName`, and `dfc-b:hasAddress` |
| **Expected Result** | All fields accessible; `@type` resolves to `dfc-b:Person` |

**Fixture** (`person/person.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@id": "http://example.org/api/dfc/Persons/10000",
  "@type": "dfc-b:Person",
  "dfc-b:firstName": "Ali",
  "dfc-b:familyName": "Khan",
  "dfc-b:hasEmail": "ali.khan@example.org",
  "dfc-b:hasAddress": "http://example.org/api/dfc/Addresses/40000"
}
```

---

### SER-006 — Parse a paginated `@graph` list of Enterprises

| | |
|---|---|
| **ID** | SER-006 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `enterprise/enterprise_list.jsonld` |
| **Action** | Parse the `@graph` array; iterate over all nodes and verify each is typed `dfc-b:Enterprise` |
| **Expected Result** | Three Enterprise nodes retrieved; all `@id` values are absolute IRIs |

**Fixture** (`enterprise/enterprise_list.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@graph": [
    { "@id": "http://example.org/api/dfc/Enterprises/10000", "@type": "dfc-b:Enterprise" },
    { "@id": "http://example.org/api/dfc/Enterprises/20000", "@type": "dfc-b:Enterprise" },
    { "@id": "http://example.org/api/dfc/Enterprises/30000", "@type": "dfc-b:Enterprise" }
  ]
}
```

---

### SER-007 — Round-trip a SuppliedProduct (deserialize → serialize → deserialize)

| | |
|---|---|
| **ID** | SER-007 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Parse the fixture into a native object, serialize it back to JSON-LD, then parse again |
| **Expected Result** | Second parse yields semantically equivalent data; no fields dropped, no types coerced, `dfc-b:refrigerated` remains a boolean |

---

### SER-008 — Parse product with `hasVariant` / `isVariantOf` relationships

| | |
|---|---|
| **ID** | SER-008 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_variant.jsonld` |
| **Action** | Parse the `@graph`; navigate from the parent product's `dfc-b:hasVariant` array to each variant, and from a variant's `dfc-b:isVariantOf` back to the parent |
| **Expected Result** | Bidirectional links are accessible; the `@id` values match correctly across directions |

**Fixture** (`supplied-product/supplied_product_variant.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@graph": [
    {
      "@id": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001",
      "@type": "dfc-b:SuppliedProduct",
      "dfc-b:name": "Basil Pesto",
      "dfc-b:hasVariant": [
        "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10002",
        "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10003"
      ]
    },
    {
      "@id": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10002",
      "@type": "dfc-b:SuppliedProduct",
      "dfc-b:name": "Basil Pesto - 100g",
      "dfc-b:isVariantOf": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001",
      "dfc-b:hasQuantity": {
        "@type": "dfc-b:QuantitativeValue",
        "dfc-b:hasUnit": "dfc-m:Gram",
        "dfc-b:value": 100.0
      }
    },
    {
      "@id": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10003",
      "@type": "dfc-b:SuppliedProduct",
      "dfc-b:name": "Basil Pesto - Case of 12",
      "dfc-b:isVariantOf": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001",
      "dfc-b:hasQuantity": {
        "@type": "dfc-b:QuantitativeValue",
        "dfc-b:hasUnit": "dfc-m:pack",
        "dfc-b:value": 12.0
      }
    }
  ]
}
```

---

### SER-009 — Parse AsPlannedTransformation flow

| | |
|---|---|
| **ID** | SER-009 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_transformation.jsonld` |
| **Action** | Parse the `@graph`; navigate the transformation chain: `SuppliedProduct` → `asPlannedProductionFlow` → `AsPlannedTransformation` → `hasInput` / `hasOutput` |
| **Expected Result** | All transformation nodes accessible and correctly typed; `dfc-b:hasTransformationType` resolves to a valid vocabulary term |

---

### SER-010 — Parse an Order with DeliveryOption

| | |
|---|---|
| **ID** | SER-010 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `order/order_delivery.jsonld` |
| **Action** | Parse the fixture; confirm `dfc-b:selects` points to a `dfc-b:DeliveryOption`, and that option has `dfc-b:deliveredAt` pointing to a `dfc-b:PhysicalPlace` with a full `dfc-b:Address` |
| **Expected Result** | All nodes accessible; delivery address fields (street, city, postcode, country) present |

---

### SER-011 — Parse an Order with PaymentMethod

| | |
|---|---|
| **ID** | SER-011 |
| **Category** | serialization |
| **Priority** | mandatory |
| **Fixture** | `order/order_with_payment.jsonld` |
| **Action** | Parse the fixture; access `dfc-b:hasPaymentMethod` on the Order, and navigate to its nested `dfc-b:Price` |
| **Expected Result** | `dfc-b:paymentMethodType`, `dfc-b:value`, `dfc-b:VATrate`, and `dfc-b:hasUnit` on the price are all accessible |

---

## 2. Schema Validation

### SCH-001 — Accept valid Enterprise with all required fields

| | |
|---|---|
| **ID** | SCH-001 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `enterprise/enterprise_full.jsonld` |
| **Action** | Validate the fixture against the DFC context and ontology |
| **Expected Result** | Zero validation errors; all `dfc-b:` terms are recognised from the ontology |

---

### SCH-002 — Accept a minimal Enterprise (only required fields)

| | |
|---|---|
| **ID** | SCH-002 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `enterprise/enterprise_minimal.jsonld` |
| **Action** | Validate a document with only `@id`, `@type`, and `dfc-b:name` |
| **Expected Result** | Passes validation; optional fields MUST NOT be required by the platform |

**Fixture** (`enterprise/enterprise_minimal.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@id": "http://example.org/api/dfc/Enterprises/99999",
  "@type": "dfc-b:Enterprise",
  "dfc-b:name": "Minimal Farm"
}
```

---

### SCH-003 — Reject a document with wrong `@type` for a Price value

| | |
|---|---|
| **ID** | SCH-003 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `invalid/wrong_type_for_price.jsonld` |
| **Action** | Attempt to validate a document where `dfc-b:hasPrice` is a plain string instead of a `dfc-b:Price` object |
| **Expected Result** | Validation raises an error or warning identifying `dfc-b:hasPrice`; the platform MUST NOT silently accept the value |

**Fixture** (`invalid/wrong_type_for_price.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@id": "http://example.org/api/dfc/Enterprises/10000/customerCategories/10005/Offers/99999",
  "@type": "dfc-b:Offer",
  "dfc-b:hasPrice": "19.99"
}
```

---

### SCH-004 — Reject a document missing the DFC `@context`

| | |
|---|---|
| **ID** | SCH-004 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `invalid/missing_context.jsonld` |
| **Action** | Attempt to process a `dfc-b:` document with no `@context` |
| **Expected Result** | A specific, catchable error is raised before processing; terms MUST NOT be silently treated as relative IRIs |

---

### SCH-005 — Reject a SuppliedProduct missing `dfc-b:name`

| | |
|---|---|
| **ID** | SCH-005 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `invalid/missing_required_field.jsonld` |
| **Action** | Validate a `dfc-b:SuppliedProduct` with no `dfc-b:name` |
| **Expected Result** | Platform raises a validation error identifying the missing field; does not silently produce an anonymous product |

**Fixture** (`invalid/missing_required_field.jsonld`):
```json
{
  "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json",
  "@id": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/99998",
  "@type": "dfc-b:SuppliedProduct",
  "dfc-b:description": "A product with no name"
}
```

---

### SCH-006 — Accept valid `dfc-pt:` product type term

| | |
|---|---|
| **ID** | SCH-006 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Validate that `dfc-b:hasType` resolves to a known term in the `dfc-pt:` taxonomy (e.g. `dfc-pt:processed-vegetable`) |
| **Expected Result** | Term is accepted; no error about unrecognised product type |

---

### SCH-007 — Accept valid `dfc-f:` certification facet

| | |
|---|---|
| **ID** | SCH-007 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Validate that `dfc-b:hasCertification` value `dfc-f:Organic-AB` resolves against the DFC facets vocabulary |
| **Expected Result** | Term accepted; no unknown IRI error |

---

### SCH-008 — Validate `dfc-m:` unit term on QuantitativeValue

| | |
|---|---|
| **ID** | SCH-008 |
| **Category** | schema |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Validate that `dfc-b:hasUnit` on the `QuantitativeValue` resolves to a `dfc-m:` term (e.g. `dfc-m:Gram`) |
| **Expected Result** | Term accepted; value is not treated as a raw string |

---

### SCH-009 — Validate context version matches ontology version

| | |
|---|---|
| **ID** | SCH-009 |
| **Category** | schema |
| **Priority** | optional |
| **Fixture** | All fixtures |
| **Action** | Confirm the `@context` URL in each fixture references the same ontology version the platform was built against (currently `context_2.0.0.json`) |
| **Expected Result** | No version mismatch detected; or platform raises a meaningful warning if context versions differ |

---

## 3. Edge Cases & Error Handling

### EDG-001 — `dfc-b:supplies` as a single IRI vs array

| | |
|---|---|
| **ID** | EDG-001 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse one document where `dfc-b:supplies` is a single IRI string, and another where it is a JSON array of IRIs |
| **Input A** | `"dfc-b:supplies": "http://example.org/api/dfc/Enterprises/10000/SuppliedProducts/10001"` |
| **Input B** | `"dfc-b:supplies": ["http://...10001", "http://...10002"]` |
| **Expected Result** | Both forms are handled without error; the platform normalises to an iterable collection in both cases |

---

### EDG-002 — Price value as numeric vs string

| | |
|---|---|
| **ID** | EDG-002 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse an Offer where `dfc-b:value` inside `dfc-b:hasPrice` is the JSON number `4.95`, and separately where it is the string `"4.95"` |
| **Expected Result** | Platform accepts both forms without error; numeric value is preserved without floating-point distortion (i.e. 4.95 must not become 4.950000001) |

> **Note:** The DFC standard and API examples show both forms in different versions. Platforms MUST handle both.

---

### EDG-003 — `@id` using relative IRI with `@base`

| | |
|---|---|
| **ID** | EDG-003 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse a document using a relative `@id` such as `"suppliedProduct/item1"` with `"@base": "http://myplatform.example/"` declared in the `@context` array |
| **Expected Result** | `@id` resolves to the absolute IRI `http://myplatform.example/suppliedProduct/item1`; no error is thrown |

---

### EDG-004 — `@id` value of `"#"` (blank node placeholder)

| | |
|---|---|
| **ID** | EDG-004 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse a `POST` request body where the object uses `"@id": "#"` as a client-assigned placeholder |
| **Input** | `{ "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json", "@id": "#", "@type": "dfc-b:CatalogItem", "dfc-b:sku": "TEST" }` |
| **Expected Result** | Document is accepted for write operations; platform assigns a real IRI before storing; `"#"` is not persisted as the object's identifier |

---

### EDG-005 — Inline nested object vs IRI reference for the same relation

| | |
|---|---|
| **ID** | EDG-005 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse two documents: one where `dfc-b:hasAddress` is an inline object, another where it is an IRI reference to a separate node |
| **Expected Result** | Both forms produce the same accessible address data; the inline form is not rejected, and the IRI form does not silently lose address fields |

---

### EDG-006 — Refrigeration flags (`dfc-b:refrigerated`, `dfc-b:frozen`) as booleans vs strings

| | |
|---|---|
| **ID** | EDG-006 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse a `SuppliedProduct` with `"dfc-b:refrigerated": true` (JSON boolean), and separately `"dfc-b:refrigerated": "true"` (string, as seen in v1.9 examples) |
| **Expected Result** | Both forms evaluate to a truthy boolean in the platform's native representation; `false` / `"false"` evaluate as falsy |

---

### EDG-007 — Temperature range with min/max values

| | |
|---|---|
| **ID** | EDG-007 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Parse `dfc-b:hasTemperature` with `dfc-b:minValue` and `dfc-b:maxValue`; verify min < max |
| **Expected Result** | Both values accessible as comparable numerics; platform does not reject negative temperature values (e.g. -5°C) |

---

### EDG-008 — Order date as ISO 8601 with timezone offset

| | |
|---|---|
| **ID** | EDG-008 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `order/order_pickup.jsonld` |
| **Action** | Parse `dfc-b:date` value `"2024-06-01T10:00:00+01:00"` |
| **Expected Result** | Date is parsed as a timezone-aware datetime; timezone offset is preserved, not silently converted to UTC or dropped |

---

### EDG-009 — Identifier reconciliation: `owl:sameAs` in `/linkSimple` response

| | |
|---|---|
| **ID** | EDG-009 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse the DFC prototype's `linkSimple` API response, which attaches `owl:sameAs` to a platform's data URI |
| **Input** | `{ "@id": "http://platform-a.example/products/123", "owl:sameAs": ["http://platform-b.example/products/456"] }` |
| **Expected Result** | `owl:sameAs` is parsed and the linked IRI is accessible; the platform's internal object is enriched with the cross-platform link |

---

### EDG-010 — Empty `@graph` array

| | |
|---|---|
| **ID** | EDG-010 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse `{ "@context": "https://w3id.org/dfc/ontology/context/context_2.0.0.json", "@graph": [] }` |
| **Expected Result** | Returns an empty collection; no error thrown; platform does not interpret this as a malformed document |

---

### EDG-011 — `dfc-b:totalTheoreticalStock` of zero

| | |
|---|---|
| **ID** | EDG-011 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(inline)* |
| **Action** | Parse a `SuppliedProduct` with `"dfc-b:totalTheoreticalStock": 0.0` |
| **Expected Result** | Zero is preserved as a numeric zero; it MUST NOT be treated as `null`, omitted, or silently dropped (zero stock is a meaningful state) |

---

### EDG-012 — `dfc-b:stockLimitation` of zero on CatalogItem and Offer

| | |
|---|---|
| **ID** | EDG-012 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `catalog/catalog_item.jsonld` (fixture should include `stockLimitation: 0`) |
| **Action** | Parse both `dfc-b:CatalogItem` and `dfc-b:Offer` with `dfc-b:stockLimitation` set to `0` |
| **Expected Result** | Zero is preserved; not interpreted as unlimited stock or treated as absent |

---

### EDG-013 — Malformed IRI in `dfc-b:supplies`

| | |
|---|---|
| **ID** | EDG-013 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | `invalid/malformed_iri.jsonld` |
| **Action** | Attempt to resolve an IRI that is syntactically invalid (e.g. contains spaces or illegal characters) |
| **Expected Result** | Platform raises a specific error naming the invalid IRI; does not silently treat it as a relative path or blank node |

---

### EDG-014 — OIDC token absent or expired

| | |
|---|---|
| **ID** | EDG-014 |
| **Category** | edge-case |
| **Priority** | mandatory |
| **Fixture** | *(runtime test — no fixture file)* |
| **Action** | Issue a request to the platform's DFC user data endpoint with no Bearer token; then with an expired/invalid token |
| **Expected Result** | Both cases return HTTP 401; response body MUST NOT contain any user data |

---

### EDG-015 — Cross-platform product type matching via `dfc-pt:` taxonomy

| | |
|---|---|
| **ID** | EDG-015 |
| **Category** | edge-case |
| **Priority** | optional |
| **Fixture** | `supplied-product/supplied_product_full.jsonld` |
| **Action** | Confirm that two platforms independently parsing the same `dfc-pt:processed-vegetable` term both resolve it to the same IRI from the shared DFC taxonomy |
| **Expected Result** | Both platforms expand the term to the same absolute IRI; no platform-local rewriting occurs |

---

## 4. Reporting Requirements

### JUnit XML format

All platforms MUST emit results as JUnit XML. The `classname` attribute of each `<testcase>` MUST match the test ID from this spec (e.g. `SER-001`). This enables automated cross-platform aggregation.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="dfc-interop" time="2.345">
  <testsuite name="serialization" tests="11" failures="0" errors="0" skipped="0">
    <testcase classname="SER-001" name="Parse a DFC Enterprise document" time="0.021"/>
    <testcase classname="SER-002" name="Parse a SuppliedProduct with QuantitativeValue" time="0.018"/>
    <!-- ... -->
  </testsuite>
  <testsuite name="schema" tests="9" failures="0" errors="0" skipped="1">
    <testcase classname="SCH-009" name="Validate context version matches ontology version">
      <skipped message="Version pinning not yet implemented"/>
    </testcase>
  </testsuite>
  <testsuite name="edge-case" tests="15" failures="1" errors="0" skipped="0">
    <testcase classname="EDG-006" name="Refrigeration flags as booleans vs strings" time="0.009">
      <failure message="String 'true' not accepted" type="AssertionError">
        Expected truthy result for dfc-b:refrigerated = "true", got parsing error.
      </failure>
    </testcase>
  </testsuite>
</testsuites>
```

### Result submission

Place results at `/results/{platform-name}/results.xml`. Use a consistent lowercase hyphenated name (e.g. `ruby-ofn`, `typescript-dfc-connector`, `php-connector`). Results without a recognisable platform name will not be included in the aggregated compliance report.

---

## 5. Versioning & Change Control

| Version | Change |
|---|---|
| 2.0.0 | Aligned with DFC ontology v2.0.0 — namespace migration, Enterprise→Organization rename, new test cases for Variant, ProductOption, TemplateSaleSession |
| 1.0.0 | Initial release — 35 test cases across 3 categories, aligned with DFC ontology v1.16.0 |

Test IDs are permanent and will never be reassigned. When the DFC ontology version increments, a new spec version will be issued. Platforms will have a minimum 4-week migration window before new tests become mandatory.

---

## 6. References

- DFC Standard Documentation: https://docs.dfc-standard.org/dfc-standard-documentation
- DFC Business Ontology: https://lov.linkeddata.es/dataset/lov/vocabs/dfc-b
- DFC API Example (OpenAPI): https://app.swaggerhub.com/apis-docs/food-data-collab/dfc-sample_api/
- DFC Connector libraries (TypeScript, Ruby, PHP): https://github.com/datafoodconsortium
- Practical examples (v1.9): https://docs.dfc-standard.org/dfc-standard-documentation/appendixes/practical-examples/version-1.9
