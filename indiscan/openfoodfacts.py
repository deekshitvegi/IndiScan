"""Barcode lookup via Open Food Facts (https://world.openfoodfacts.org).

`parse_product` is pure (easy to test offline); `lookup` does the HTTP call.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

import requests

from .scoring import Nutrition

API = "https://world.openfoodfacts.org/api/v2/product/{code}.json"
FIELDS = "product_name,brands,ingredients_text,nutriments,categories_tags"
HEADERS = {"User-Agent": "IndiScan/0.1 (https://github.com/deekshitvegi/IndiScan)"}
_BEVERAGE = re.compile(r"beverage|drink|juice|soda|water|lassi|buttermilk|tea|coffee", re.I)


@dataclass
class Product:
    barcode: str
    name: str
    brand: str
    ingredients: str
    category: str
    nutrition: Nutrition
    missing: list


def parse_product(code: str, data: dict) -> Product:
    """Convert an Open Food Facts API payload into a Product. Raises LookupError if not found."""
    if data.get("status") not in (1, "1") or not data.get("product"):
        raise LookupError(f"Product {code} not found on Open Food Facts")
    p = data["product"]
    n = p.get("nutriments") or {}
    missing: list[str] = []

    def get(key: str) -> float | None:
        v = n.get(key)
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    energy = get("energy-kcal_100g")
    if energy is None and get("energy_100g") is not None:
        energy = get("energy_100g") / 4.184  # kJ -> kcal
    sodium_g = get("sodium_100g")
    if sodium_g is None and get("salt_100g") is not None:
        sodium_g = get("salt_100g") / 2.5  # salt -> sodium
    vals = {
        "energy_kcal": energy,
        "sugar_g": get("sugars_100g"),
        "saturated_fat_g": get("saturated-fat_100g"),
        "trans_fat_g": get("trans-fat_100g"),
        "sodium_mg": None if sodium_g is None else sodium_g * 1000,
        "protein_g": get("proteins_100g"),
        "fibre_g": get("fiber_100g"),
    }
    missing = [k for k, v in vals.items() if v is None]
    nutrition = Nutrition(**{k: max(0.0, v or 0.0) for k, v in vals.items()})
    tags = " ".join(p.get("categories_tags") or [])
    return Product(code, p.get("product_name", ""), p.get("brands", ""),
                   p.get("ingredients_text", ""),
                   "beverage" if _BEVERAGE.search(tags) else "food", nutrition, missing)


def lookup(code: str, timeout: float = 10.0) -> Product:
    code = code.strip()
    if not code.isdigit():
        raise ValueError("barcode must be digits only")
    r = requests.get(API.format(code=code), params={"fields": FIELDS},
                     headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return parse_product(code, r.json())
