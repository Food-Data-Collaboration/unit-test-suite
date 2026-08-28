# Demo UK Local Food — Fixtures

Plausible but **non-genuine** demo data for 10 UK local food producers.
Generated deterministically (seed 42) for the Food Data Collaboration
federation. All enterprise names, addresses, postcodes, emails, and prices
are invented — postcodes are plausible but not tied to real businesses.
**Do not use for deliveries.**

## What is included

| File | @type | Count | Notes |
|------|-------|-------|-------|
| `organizations.jsonld` | `dfc-b:Organization` | 10 | v2 ontology (`Enterprise` in v1). Includes `hasAddress`, `supplies`, `manages` links |
| `addresses.jsonld` | `dfc-b:Address` | 10 | `GB`/`United Kingdom`, UK postcode regex, lat/long in GB bbox |
| `supplied_products.jsonld` | `dfc-b:SuppliedProduct` | 42 | `hasType` = `dfc-pt:*` full taxonomy URI, `hasQuantity` with `dfc-m:` unit |
| `catalog_items.jsonld` | `dfc-b:CatalogItem` + `dfc-b:Offer` (nested `dfc-b:Price`) | 42+42 | Price is via `Offer → hasPrice` (`value` GBP + `VATrate` + `hasUnit`). ~76% of CatalogItems omit `dfc-b:sku` (realistic for small veg producers) |
| `demo_uk_local_food.jsonld` | `@graph` combined | 126+ | Single file containing all above + `CustomerCategory` (Retail). Same sku sparsity as above |
| `csv/*.csv` | 7 files | 10/10/42/10/42/42/42 | Derived CSVs importable via `djangoldp_csv` (see `csv/IMPORT_ORDER.md`) |

Context: `https://w3id.org/dfc/ontology/context/context_2.0.0.json`.
Base IRI for JSON-LD: `http://example.org/api/dfc/...` (matches existing fixtures).
CSV urlids use `https://demo.fooddatacollaboration.org.uk/api/dfc/...`.

## Producers

- Bramble Hill Market Garden (Lewes, East Sussex)
- Wye Valley Pastures (Bristol, Somerset)
- Moorland Field Farm (Totnes, Devon)
- Cotswold Edge Dairy (Stroud, Gloucestershire)
- Blackdown Hills Orchard (Bath, Somerset)
- Severn Vale style held by others — see `organizations.jsonld` for full list.

All 10 cover: Somerset, Devon, Gloucestershire, Kent, Norfolk, Cornwall,
North Yorkshire, Herefordshire, East Sussex, Northumberland.

Products sampled from `data_food_consortium/enums.py:ProductType` UK basket:
`vegetable, carrot, potato, onion, leek, kale, spinach, beetroot, cucumber, strawberry,
raspberry, apples, pear, plum, tomato, herbs, egg, milk, butter, mature-cheese, bread,
honey, beef, lamb, pork, chicken, etc.`  Full URIs like
`https://github.com/datafoodconsortium/taxonomies/releases/latest/download/productTypes.rdf#carrot`.

Prices in GBP (`dfc-m:GBP`), stockLimitation 0–100, VAT 0/5/20 (organic).
Quantities use `dfc-m:Kilogram/Gram/Litre/Piece` per product.
SKUs are present on only ~15% of CatalogItems (preserved/packed lines); most
veg/box items omit `dfc-b:sku` to reflect small-scale producers without stock control.

## Regenerating

```bash
# from repo root
python scripts/generate_demo_uk_local_food.py --seed 42 --producers 10
python scripts/generate_demo_uk_local_food.py --seed 99 --producers 5 --output /tmp/demo
```

Stdlib only — no faker dependency. Deterministic: same seed → same output.
Edit `PRODUCT_POOL` / `LOCATIONS` / price ranges in the script to customise.

## Using the JSON-LD

```bash
# validate parses
python -m json.tool fixtures/demo_uk_local_food/demo_uk_local_food.jsonld > /dev/null
python -m json.tool fixtures/demo_uk_local_food/organizations.jsonld > /dev/null

# python rdflib example
python -c "from rdflib import Graph; g=Graph(); g.parse('fixtures/demo_uk_local_food/demo_uk_local_food.jsonld', format='json-ld'); print(len(g))"
```

Works with `spec/tests.yaml` patterns (SER-001/002/003 — parse `@type`, `hasQuantity`, `offeredThrough→hasPrice`).

## Using the CSVs (Central Directory)

See [`csv/IMPORT_ORDER.md`](csv/IMPORT_ORDER.md) for the 7-step import order and
`DJANGOLDP_CSV_MODELS` extension required:

```yaml
DJANGOLDP_CSV_MODELS:
  - 'dfc-b:Enterprise'
  - 'dfc-b:Address'
  - 'dfc-b:SuppliedProduct'
  - 'dfc-b:CatalogItem'
  - 'dfc-b:CustomerCategory'
  - 'dfc-b:Price'
  - 'dfc-b:Offer'
```

Then `djangoldp configure` + `POST /djangoldp-csv/import/?model-type=dfc-b:<Type>` per file.

## License / disclaimer

Synthetic demo data only — no real trader data. Names like “Fred’s Farm” style
are retained for compatibility with `organization/organization_full.jsonld`.
If a name coincidentally matches a real business, it is unintentional.
