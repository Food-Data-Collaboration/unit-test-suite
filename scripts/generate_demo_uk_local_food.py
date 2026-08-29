#!/usr/bin/env python3
"""
Generate plausible but non-genuine UK local food demo data.

Produces:
  fixtures/demo_uk_local_food/*.jsonld  — DFC v2.0.0 JSON-LD graphs (primary)
  fixtures/demo_uk_local_food/csv/*.csv — Derived CSVs importable via djangoldp_csv

Deterministic with --seed (default 42). Stdlib only, no faker dependency.

10 fictional producers × ~4 SuppliedProducts each (~40) + Addresses,
CatalogItems, CustomerCategories, Offers, Prices.

All names/addresses are invented. Postcodes are plausible but not tied to
real businesses. Do not use for deliveries.

Usage:
  python scripts/generate_demo_uk_local_food.py
  python scripts/generate_demo_uk_local_food.py --seed 42 --producers 10
"""

import argparse
import csv
import json
import random
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONTEXT_V2 = "https://w3id.org/dfc/ontology/context/context_2.0.0.json"

BASE_IRI = "http://example.org/api/dfc"  # matches fixtures/* in spec
CSV_BASE = "https://demo.fooddatacollaboration.org.uk/api/dfc"

# UK-ish locations — cities/counties/postcode areas are real, combos are invented
LOCATIONS = [
    {"city": "Bristol", "region": "Somerset", "postcode_area": "BS", "lat": 51.45, "lon": -2.58},
    {"city": "Bath", "region": "Somerset", "postcode_area": "BA", "lat": 51.38, "lon": -2.36},
    {"city": "Totnes", "region": "Devon", "postcode_area": "TQ", "lat": 50.43, "lon": -3.68},
    {"city": "Stroud", "region": "Gloucestershire", "postcode_area": "GL", "lat": 51.74, "lon": -2.21},
    {"city": "Frome", "region": "Somerset", "postcode_area": "BA", "lat": 51.23, "lon": -2.32},
    {"city": "Canterbury", "region": "Kent", "postcode_area": "CT", "lat": 51.28, "lon": 1.08},
    {"city": "Norwich", "region": "Norfolk", "postcode_area": "NR", "lat": 52.63, "lon": 1.29},
    {"city": "Truro", "region": "Cornwall", "postcode_area": "TR", "lat": 50.26, "lon": -5.05},
    {"city": "York", "region": "North Yorkshire", "postcode_area": "YO", "lat": 53.96, "lon": -1.08},
    {"city": "Hereford", "region": "Herefordshire", "postcode_area": "HR", "lat": 52.06, "lon": -2.72},
    {"city": "Lewes", "region": "East Sussex", "postcode_area": "BN", "lat": 50.87, "lon": 0.01},
    {"city": "Hexham", "region": "Northumberland", "postcode_area": "NE", "lat": 54.97, "lon": -2.10},
]

PRODUCER_TEMPLATES = [
    ("Bramble Hill", "Market Garden"),
    ("Wye Valley", "Pastures"),
    ("Moorland Field", "Farm"),
    ("Cotswold Edge", "Dairy"),
    ("Blackdown Hills", "Orchard"),
    ("Severn Vale", "Growers"),
    ("Tamar Valley", "Smallholding"),
    ("Vale of York", "Heritage Farm"),
    ("Weald & Down", "Organics"),
    ("Northumbrian Moor", "Free Range"),
    ("Somerset Levels", "Collective"),
    ("Cornish Hedgerow", "Produce"),
]

STREETS = [
    "Farm Lane", "High Street", "Mill Lane", "Orchard Way",
    "Church Lane", "Green Lane", "Hollow Lane", "Barn Close",
    "The Green", "Station Road", "Old Orchard", "Meadow View",
]

CONTACT_FIRST = ["Aisha", "Tom", "Maya", "Huw", "Grace", "Owen", "Priya", "Sam", "Lena", "Jon", "Ffion", "Callum"]
CONTACT_LAST = ["Morgan", "Patel", "Hughes", "O'Leary", "Evans", "Khan", "Williams", "Davies", "Ahmed", "Brown"]

# Product pool — name, DFC product type slug, unit, price range (min, max GBP), quantity
PRODUCT_POOL = [
    ("Seasonal Veg Box - Small", "vegetable", "dfc-m:Piece", (11.5, 15.0), "1 box"),
    ("Carrots - Washed", "carrot", "dfc-m:Kilogram", (1.6, 2.4), "1 kg"),
    ("Potatoes - Maris Piper", "potato", "dfc-m:Kilogram", (1.4, 2.2), "1 kg"),
    ("Onions - Brown", "onion", "dfc-m:Kilogram", (1.8, 2.6), "1 kg"),
    ("Leeks - Trimmed", "leek", "dfc-m:Kilogram", (2.2, 3.5), "500 g"),
    ("Kale - Curly", "kale", "dfc-m:Gram", (1.8, 2.8), "200 g"),
    ("Spinach - Baby Leaf", "spinach", "dfc-m:Gram", (2.0, 3.0), "150 g"),
    ("Beetroot - Bunch", "beetroot", "dfc-m:Piece", (1.5, 2.5), "bunch"),
    ("Strawberries", "strawberry", "dfc-m:Gram", (3.0, 4.5), "250 g"),
    ("Raspberries", "raspberry", "dfc-m:Gram", (2.8, 4.2), "200 g"),
    ("Apples - Mixed Heritage", "apples", "dfc-m:Kilogram", (2.5, 4.0), "1 kg"),
    ("Pears - Conference", "pear", "dfc-m:Kilogram", (2.4, 3.8), "1 kg"),
    ("Plums - Victoria", "plum", "dfc-m:Kilogram", (3.0, 5.0), "500 g"),
    ("Free Range Eggs (6)", "egg", "dfc-m:Piece", (2.2, 3.4), "6 eggs"),
    ("Free Range Eggs (12)", "egg", "dfc-m:Piece", (3.8, 5.5), "12 eggs"),
    ("Whole Milk", "milk", "dfc-m:Litre", (1.1, 1.6), "1 L"),
    ("Butter - Salted Block", "butter", "dfc-m:Gram", (2.4, 3.6), "250 g"),
    ("Mature Cheddar (Cow)", "mature-cheese", "dfc-m:Gram", (3.5, 5.5), "250 g"),
    ("Fresh Goats Cheese", "goat-fresh-cheese", "dfc-m:Gram", (2.8, 4.5), "150 g"),
    ("Sourdough Loaf", "bread", "dfc-m:Piece", (3.2, 5.0), "1 loaf"),
    ("Rye Bread", "bread", "dfc-m:Piece", (3.0, 4.8), "1 loaf"),
    ("Raw Wildflower Honey", "honey", "dfc-m:Gram", (4.5, 7.5), "340 g"),
    ("Heritage Tomatoes", "tomato", "dfc-m:Gram", (2.6, 4.0), "500 g"),
    ("Courgettes", "courgette", "dfc-m:Kilogram", (2.0, 3.2), "500 g"),
    ("Cucumber", "cucumber", "dfc-m:Piece", (0.9, 1.6), "1 piece"),
    ("Lamb - Leg Joint", "lamb", "dfc-m:Kilogram", (14.0, 18.5), "1 kg"),
    ("Beef - Topside", "beef", "dfc-m:Kilogram", (16.0, 20.0), "1 kg"),
    ("Pork - Shoulder", "pork", "dfc-m:Kilogram", (9.0, 13.0), "1 kg"),
    ("Chicken - Whole", "chicken", "dfc-m:Kilogram", (7.5, 11.0), "1.5 kg"),
    ("Basil Pesto - 100g", "processed-vegetable", "dfc-m:Gram", (3.5, 5.2), "100 g"),
    ("Apple Juice - Cloudy", "fruit-juice", "dfc-m:Litre", (2.8, 4.2), "1 L"),
    ("Jam - Strawberry", "jam", "dfc-m:Gram", (3.2, 5.0), "340 g"),
]

DFC_PT_PREFIX = "https://github.com/datafoodconsortium/taxonomies/releases/latest/download/productTypes.rdf#"
# Also valid: dfc-pt: prefix via context, but we emit full URI for CSV compat
# For JSON-LD we use dfc-pt: short form which expands via context
DFC_M_PREFIX = "dfc-m:"

POSTCODE_RE = re.compile(r"^[A-Z]{1,2}[0-9][0-9A-Z]?\s[0-9][A-Z]{2}$")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def random_postcode(area: str, rng: random.Random) -> str:
    inward_num = rng.randint(1, 9)
    letters = "".join(rng.choice("ABDEFGHJLNPQRSTUWXYZ") for _ in range(2))
    outward_num = rng.randint(1, 9)
    if rng.random() < 0.3:
        outward = f"{area}{outward_num}{rng.choice('AB')}"
    else:
        outward = f"{area}{outward_num}"
    return f"{outward} {inward_num}{letters}"

def jitter(lat, lon, rng):
    return (
        round(lat + rng.uniform(-0.15, 0.15), 5),
        round(lon + rng.uniform(-0.15, 0.15), 5),
    )

def price_for(rng, low, high):
    v = rng.uniform(low, high)
    # round to .95/.50 pricing feel sometimes
    if rng.random() < 0.4:
        v = round(v) - 0.05 if round(v) > low else round(v * 2) / 2
        v = max(low, min(high, v))
    return round(v, 2)

def make_organization(idx, tmpl, loc, rng):
    name_core, suffix = tmpl
    name = f"{name_core} {suffix}"
    # avoid collision: if duplicate core, add location
    org_slug = slug(f"{name_core}-{suffix}-{loc['city']}".lower())
    # IDs — JSON-LD uses BASE_IRI, CSV uses CSV_BASE but we keep same slug
    base = f"{BASE_IRI}/Enterprises/{org_slug}"
    # also Enterprise id for CSV compat (same iri works, DFC v2 calls it Organization)
    vat_num = f"GB{''.join(str(rng.randint(0,9)) for _ in range(9))}"
    email = f"hello@{slug(name_core)}-{slug(loc['city'])}.example"
    phone = f"+44 1{''.join(str(rng.randint(0,9)) for _ in range(3))} {rng.randint(100000,999999)}"
    postcode = random_postcode(loc["postcode_area"], rng)
    assert POSTCODE_RE.match(postcode), postcode
    lat, lon = jitter(loc["lat"], loc["lon"], rng)
    street_num = rng.randint(1, 120)
    street = f"{street_num} {rng.choice(STREETS)}"
    contact = f"{rng.choice(CONTACT_FIRST)} {rng.choice(CONTACT_LAST)}"
    desc = rng.choice([
        f"Small agroecological farm supplying {loc['city']} and surrounds.",
        f"Family-run holding on the edge of {loc['region']}, organic since 2018.",
        f"Community market garden and orchard serving {loc['city']} box scheme.",
        f"Pasture-fed livestock and seasonal veg from the {loc['region']} hills.",
    ])
    return {
        "name": name,
        "slug": org_slug,
        "base_iri": base,
        "csv_iri": f"{CSV_BASE}/enterprises/{org_slug}/",
        "vat": vat_num,
        "email": email,
        "phone": phone,
        "website": f"https://www.{slug(name_core)}-{slug(loc['city'])}.example",
        "contact": contact,
        "desc": desc,
        "long_desc": desc + " Members collect on Fridays or opt for local delivery.",
        "loc": loc,
        "street": street,
        "postcode": postcode,
        "lat": str(lat),
        "lon": str(lon),
    }

def build(args):
    rng = random.Random(args.seed)
    out_root = Path(args.output)
    csv_root = out_root / "csv"
    out_root.mkdir(parents=True, exist_ok=True)
    csv_root.mkdir(parents=True, exist_ok=True)

    # Pick 10 producers deterministically
    producers = []
    templates = rng.sample(PRODUCER_TEMPLATES, k=args.producers)
    locs = rng.sample(LOCATIONS, k=args.producers) if args.producers <= len(LOCATIONS) else [rng.choice(LOCATIONS) for _ in range(args.producers)]
    for i in range(args.producers):
        producers.append(make_organization(i, templates[i], locs[i], rng))

    # Shuffle products pool deterministically and assign
    pool = PRODUCT_POOL[:]
    rng.shuffle(pool)
    # ensure each producer gets 3-5 products, total ~40
    # distribute round-robin
    assignments = {p["slug"]: [] for p in producers}
    # target per producer: 4, with variation
    per_producer = []
    for _ in range(args.producers):
        per_producer.append(rng.choice([3, 4, 4, 5]))
    # adjust to fit pool
    total_needed = sum(per_producer)
    # if pool smaller, cycle; if larger, trim
    idx = 0
    for pi, p in enumerate(producers):
        n = per_producer[pi]
        chosen = []
        for _ in range(n):
            if idx >= len(pool):
                rng.shuffle(pool)
                idx = 0
            chosen.append(pool[idx])
            idx += 1
        random.shuffle(chosen) if False else None
        assignments[p["slug"]] = chosen

    # Build JSON-LD graphs and CSV rows
    # JSON-LD collections
    org_graph = []
    addr_graph = []
    product_graph = []
    catalog_graph = []  # CatalogItems + Offers with nested Prices

    # CSV rows
    csv_enterprises = []
    csv_addresses = []
    csv_products = []
    csv_customer_cats = []
    csv_prices = []
    csv_catalog_items = []
    csv_offers = []

    for org in producers:
        org_iri = org["base_iri"]
        org_csv_iri = org["csv_iri"]
        addr_iri = f"{org_iri}/Addresses/1"
        addr_csv_iri = f"{org_csv_iri}addresses/1/"
        cat_iri = f"{org_iri}/customerCategories/retail"
        cat_csv_iri = f"{org_csv_iri}customer-categories/retail/"

        # Organization JSON-LD (DFC v2 uses dfc-b:Organization, CSV uses Enterprise but same IRI works)
        org_node = {
            "@id": org_iri,
            "@type": "dfc-b:Organization",
            "dfc-b:name": org["name"],
            "dfc-b:hasDescription": org["desc"],
            "dfc-b:email": org["email"],
            "dfc-b:hasPhoneNumber": org["phone"],
            "dfc-b:websitePage": org["website"],
            "dfc-b:VATnumber": org["vat"],
            "dfc-b:VATStatus": False,
            "ofn:contact_name": org["contact"],
            "ofn:long_description": org["long_desc"],
            "dfc-b:hasAddress": addr_iri,
        }
        # supplies & manages IRIs collected later
        supplies = []
        manages = []
        org_graph.append(org_node)

        addr_node = {
            "@id": addr_iri,
            "@type": "dfc-b:Address",
            "dfc-b:street": org["street"],
            "dfc-b:postcode": org["postcode"],
            "dfc-b:city": org["loc"]["city"],
            "dfc-b:hasCountry": "GB",
            "dfc-b:region": org["loc"]["region"],
            "dfc-b:latitude": float(org["lat"]) if rng.random() < 1 else org["lat"],
            "dfc-b:longitude": float(org["lon"]) if rng.random() < 1 else org["lon"],
        }
        addr_graph.append(addr_node)

        # CSV rows for org/address/category
        csv_enterprises.append({
            "urlid": org_csv_iri,
            "dfc-b:name": org["name"],
            "dfc-b:hasDescription": org["desc"],
            "dfc-b:email": org["email"],
            "dfc-b:VATnumber": org["vat"],
            "dfc-b:VATStatus": "False",
            "ofn:contact_name": org["contact"],
            "dfc-b:hasPhoneNumber": org["phone"],
            "dfc-b:websitePage": org["website"],
        })
        csv_addresses.append({
            "urlid": addr_csv_iri,
            "dfc-b:addressOf": org_csv_iri,
            "dfc-b:hasStreet": org["street"],
            "dfc-b:hasPostalCode": org["postcode"],
            "dfc-b:hasCity": org["loc"]["city"],
            "dfc-b:hasCountry": "United Kingdom",
            "dfc-b:region": org["loc"]["region"],
            "dfc-b:latitude": org["lat"],
            "dfc-b:longitude": org["lon"],
        })
        csv_customer_cats.append({
            "urlid": cat_csv_iri,
            "dfc-b:name": "Retail",
            "dfc-b:definedBy": org_csv_iri,
        })

        # Products / CatalogItems / Offers / Prices
        prods = assignments[org["slug"]]
        for j, (prod_name, prod_slug, unit, price_range, qty_label) in enumerate(prods):
            prod_iri = f"{org_iri}/SuppliedProducts/{slug(prod_name)}-{j+1}"
            prod_csv_iri = f"{CSV_BASE}/supplied-products/{org['slug']}-{slug(prod_name)}-{j+1}"
            # Also keep org-iri form for JSON-LD linkage
            catalog_iri = f"{org_iri}/CatalogItems/{slug(prod_name)}-{j+1}"
            catalog_csv_iri = f"{CSV_BASE}/catalog-items/{org['slug']}-{slug(prod_name)}-{j+1}"
            price_iri = f"{catalog_iri}/Prices/1"
            price_csv_iri = f"{CSV_BASE}/prices/{org['slug']}-{slug(prod_name)}-{j+1}"
            offer_iri = f"{org_iri}/Offers/{slug(prod_name)}-{j+1}"
            offer_csv_iri = f"{CSV_BASE}/offers/{org['slug']}-{slug(prod_name)}-{j+1}"

            has_type_short = f"dfc-pt:{prod_slug}"
            has_type_full = f"{DFC_PT_PREFIX}{prod_slug}"

            price_val = price_for(rng, price_range[0], price_range[1])
            vat_rate = rng.choice([0.0, 0.0, 5.0, 20.0]) if "cheese" in prod_slug or "honey" in prod_slug or "juice" in prod_slug else rng.choice([0.0, 0.0, 0.0, 5.0])
            # Quantity: we store as QuantitativeValue in JSON-LD, CSV has no direct columns (TODO hasUnit/hasQuantity)
            qty_value = 1.0
            # parse qty_label for numeric
            if "kg" in qty_label: qty_value = 1.0; qty_unit = "dfc-m:Kilogram"
            elif "g" in qty_label: qty_value = 200.0 if "200" in qty_label else 150.0 if "150" in qty_label else 100.0; qty_unit = "dfc-m:Gram"
            elif "L" in qty_label: qty_value = 1.0; qty_unit = "dfc-m:Litre"
            else: qty_value = 1.0; qty_unit = "dfc-m:Piece"

            # JSON-LD SuppliedProduct
            prod_node = {
                "@id": prod_iri,
                "@type": "dfc-b:SuppliedProduct",
                "dfc-b:name": prod_name,
                "dfc-b:description": f"{prod_name} from {org['name']} — {qty_label}. Grown/produced in {org['loc']['region']}.",
                "dfc-b:hasType": has_type_short,
                "dfc-b:hasQuantity": {
                    "@type": "dfc-b:QuantitativeValue",
                    "dfc-b:hasUnit": qty_unit,
                    "dfc-b:value": qty_value,
                },
                "dfc-b:suppliedBy": org_iri,
                "dfc-b:totalTheoreticalStock": rng.randint(20, 200),
            }
            product_graph.append(prod_node)
            supplies.append(prod_iri)

            # JSON-LD CatalogItem + nested Offer+Price graph style like catalog_item.jsonld
            # SKUs are unrealistic for most small-scale UK veg producers — only
            # ~15% get a SKU (e.g. preserved/packed lines). Others omit dfc-b:sku.
            has_sku = rng.random() < 0.15
            sku = f"{org['slug'][:4].upper()}-{slug(prod_name)[:6].upper()}-{j+1:02d}" if has_sku else ""
            stock_lim = rng.choice([20, 30, 50, 100, 0]) if rng.random() < 0.2 else rng.randint(10, 60)
            catalog_node = {
                "@id": catalog_iri,
                "@type": "dfc-b:CatalogItem",
                "dfc-b:references": prod_iri,
                "dfc-b:managedBy": org_iri,
                "dfc-b:stockLimitation": stock_lim,
                "dfc-b:offeredThrough": offer_iri,
            }
            if has_sku:
                catalog_node["dfc-b:sku"] = sku
            offer_node = {
                "@id": offer_iri,
                "@type": "dfc-b:Offer",
                "dfc-b:offersTo": cat_iri,
                "dfc-b:stockLimitation": stock_lim,
                "dfc-b:hasPrice": {
                    "@type": "dfc-b:Price",
                    "dfc-b:value": price_val,
                    "dfc-b:VATrate": vat_rate,
                    "dfc-b:hasUnit": "dfc-m:GBP",
                },
            }
            catalog_graph.extend([catalog_node, offer_node])
            manages.append(catalog_iri)

            # CSV rows
            csv_products.append({
                "urlid": prod_csv_iri,
                "dfc-b:suppliedBy": org_csv_iri,
                "dfc-b:hasType": has_type_full,
                "dfc-b:name": prod_name,
                "dfc-b:description": f"{prod_name} from {org['name']} — {qty_label}.",
                "dfc-b:URL": "",
            })
            csv_prices.append({
                "urlid": price_csv_iri,
                "dfc-b:value": str(price_val),
                "dfc-b:hasUnit": "dfc-m:GBP",
            })
            csv_catalog_items.append({
                "urlid": catalog_csv_iri,
                "dfc-b:references": prod_csv_iri,
                "dfc-b:managedBy": org_csv_iri,
                "dfc-b:sku": sku,
                "dfc-b:stockLimitation": str(stock_lim),
            })
            csv_offers.append({
                "urlid": offer_csv_iri,
                "dfc-b:offers": catalog_csv_iri,
                "dfc-b:offeredTo": cat_csv_iri,
                "dfc-b:hasPrice": price_csv_iri,
                "dfc-b:stockLimitation": str(stock_lim),
            })

        # patch org node with supplies/manages arrays
        org_node["dfc-b:supplies"] = supplies
        org_node["dfc-b:manages"] = manages

    # Write JSON-LD files
    def write_jsonld(path, graph, extra_context=False):
        doc = {"@context": CONTEXT_V2, "@graph": graph}
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_jsonld(out_root / "organizations.jsonld", org_graph)
    write_jsonld(out_root / "addresses.jsonld", addr_graph)
    write_jsonld(out_root / "supplied_products.jsonld", product_graph)
    # catalog split into catalog + offers combined
    write_jsonld(out_root / "catalog_items.jsonld", catalog_graph)

    # Also write a single combined graph for convenience
    combined = org_graph + addr_graph + product_graph + catalog_graph
    # Add customer categories as explicit nodes (for JSON-LD completeness)
    for org in producers:
        combined.append({
            "@id": f"{org['base_iri']}/customerCategories/retail",
            "@type": "dfc-b:CustomerCategory",
            "dfc-b:name": "Retail",
            "dfc-b:definedBy": org["base_iri"],
        })
    write_jsonld(out_root / "demo_uk_local_food.jsonld", combined)

    # Write CSVs
    def write_csv(path, rows, fieldnames):
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            w.writeheader()
            w.writerows(rows)

    write_csv(csv_root / "01_enterprises.csv", csv_enterprises,
              ["urlid", "dfc-b:name", "dfc-b:hasDescription", "dfc-b:email", "dfc-b:VATnumber", "dfc-b:VATStatus", "ofn:contact_name", "dfc-b:hasPhoneNumber", "dfc-b:websitePage"])
    write_csv(csv_root / "02_addresses.csv", csv_addresses,
              ["urlid", "dfc-b:addressOf", "dfc-b:hasStreet", "dfc-b:hasPostalCode", "dfc-b:hasCity", "dfc-b:hasCountry", "dfc-b:region", "dfc-b:latitude", "dfc-b:longitude"])
    write_csv(csv_root / "03_supplied_products.csv", csv_products,
              ["urlid", "dfc-b:suppliedBy", "dfc-b:hasType", "dfc-b:name", "dfc-b:description", "dfc-b:URL"])
    write_csv(csv_root / "04_customer_categories.csv", csv_customer_cats,
              ["urlid", "dfc-b:name", "dfc-b:definedBy"])
    write_csv(csv_root / "05_prices.csv", csv_prices,
              ["urlid", "dfc-b:value", "dfc-b:hasUnit"])
    write_csv(csv_root / "06_catalog_items.csv", csv_catalog_items,
              ["urlid", "dfc-b:references", "dfc-b:managedBy", "dfc-b:sku", "dfc-b:stockLimitation"])
    write_csv(csv_root / "07_offers.csv", csv_offers,
              ["urlid", "dfc-b:offers", "dfc-b:offeredTo", "dfc-b:hasPrice", "dfc-b:stockLimitation"])

    # Summary
    print(f"Wrote {len(org_graph)} organizations, {len(addr_graph)} addresses, {len(product_graph)} products, {len(catalog_graph)//2} catalog items (+ offers)")
    print(f"CSV files in {csv_root}")
    return {
        "organizations": len(org_graph),
        "addresses": len(addr_graph),
        "products": len(product_graph),
        "catalog_items": len(catalog_graph)//2,
        "out_root": str(out_root),
        "csv_root": str(csv_root),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--producers", type=int, default=10)
    ap.add_argument("--output", type=str, default="fixtures/demo_uk_local_food")
    args = ap.parse_args()
    # if run from repo root or scripts/
    # handle relative output
    # if script is scripts/generate... and output is relative, resolve vs cwd/repo root
    # we keep as given but if starts with fixtures and cwd is repo root, fine
    build(args)

if __name__ == "__main__":
    main()
