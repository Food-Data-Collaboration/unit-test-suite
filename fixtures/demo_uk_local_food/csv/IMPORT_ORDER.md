# CSV Import Order

Derived from `fixtures/demo_uk_local_food/` JSON-LD, importable via
`djangoldp_csv` (`POST /djangoldp-csv/import/?model-type=dfc-b:<Type>`).

## Required settings.yml extension

In `FDC-DjangoLDP-Central-Directory:settings.yml` (or any DjangoLDP server):

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

Run `djangoldp configure` after editing. Requires superuser (`user.is_superuser`).

## Order (FK-safe)

Import one file per request with `csv=<file>` multipart. Order matters because
FKs are resolved via `urlid` (`forms.py:74-91` get-or-create stub).

| Step | File | `model-type` | Rows | Key headers |
|------|------|--------------|------|-------------|
| 1 | `01_enterprises.csv` | `dfc-b:Enterprise` | 10 | `urlid, dfc-b:name, dfc-b:hasDescription, dfc-b:email, dfc-b:VATnumber, dfc-b:VATStatus, ofn:contact_name, dfc-b:hasPhoneNumber, dfc-b:websitePage` |
| 2 | `02_addresses.csv` | `dfc-b:Address` | 10 | `urlid, dfc-b:addressOf, dfc-b:hasStreet, dfc-b:hasPostalCode, dfc-b:hasCity, dfc-b:hasCountry, dfc-b:region, dfc-b:latitude, dfc-b:longitude` |
| 3 | `03_supplied_products.csv` | `dfc-b:SuppliedProduct` | 42 | `urlid, dfc-b:suppliedBy, dfc-b:hasType, dfc-b:name, dfc-b:description, dfc-b:URL` |
| 4 | `04_customer_categories.csv` | `dfc-b:CustomerCategory` | 10 | `urlid, dfc-b:name, dfc-b:definedBy` |
| 5 | `05_prices.csv` | `dfc-b:Price` | 42 | `urlid, dfc-b:value, dfc-b:hasUnit` |
| 6 | `06_catalog_items.csv` | `dfc-b:CatalogItem` | 42 | `urlid, dfc-b:references, dfc-b:managedBy, dfc-b:sku, dfc-b:stockLimitation` — `dfc-b:sku` blank for ~76% (small producers without SKUs) |
| 7 | `07_offers.csv` | `dfc-b:Offer` | 42 | `urlid, dfc-b:offers, dfc-b:offeredTo, dfc-b:hasPrice, dfc-b:stockLimitation` |

Re-upload is idempotent — same `urlid` upserts.

## Example

```bash
BASE=https://your-central-directory.example
for f in 01 02 03 04 05 06 07; do
  TYPE=$(case $f in 01) echo "dfc-b:Enterprise";; 02) echo "dfc-b:Address";; 03) echo "dfc-b:SuppliedProduct";; 04) echo "dfc-b:CustomerCategory";; 05) echo "dfc-b:Price";; 06) echo "dfc-b:CatalogItem";; 07) echo "dfc-b:Offer";; esac)
  curl -X POST "$BASE/djangoldp-csv/import/?model-type=$(python3 -c "import urllib.parse; print(urllib.parse.quote_plus('$TYPE'))")" \
    -H "Cookie: sessionid=YOURSESSION" \
    -F csv=@${f}_*.csv
done
```

Or via admin UI: visit `/djangoldp-csv/import/?model-type=dfc-b%3AEnterprise` etc.

## Gotchas

- Header bug in upstream example `catalog_items.csv:1` = `dfc-b:dfc-b:managedBy` — this dataset uses the correct `dfc-b:managedBy`.
- `dfc-b:hasType` must be full taxonomy URI (`https://github.com/.../productTypes.rdf#carrot`) — validated against `data_food_consortium/enums.py:ProductType`.
- `NULL` literal sentinel for empty fields — `dfc-b:sku` uses empty string for no-SKU items (import treats as blank/`None`); `NULL` also accepted.
- Price lives via `Offer` → `Price`, not directly on `CatalogItem` — that matches `data_food_consortium/models.py:572-630`.
- Validate locally before import:
  ```bash
  python -c "import csv, json; [print(r) for r in csv.DictReader(open('01_enterprises.csv'))]"
  python -m json.tool ../demo_uk_local_food.jsonld > /dev/null
  ```
