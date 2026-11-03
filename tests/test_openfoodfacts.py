import pytest
from indiscan.openfoodfacts import parse_product


def test_parse_converts_units_and_category():
    data = {"status": 1, "product": {
        "product_name": "Masala Oats", "brands": "Saffola",
        "ingredients_text": "oats, spices, INS 621",
        "categories_tags": ["en:breakfast-cereals"],
        "nutriments": {"energy_100g": 1674, "sugars_100g": 3, "salt_100g": 2.5,
                       "proteins_100g": 10, "fiber_100g": 9}}}
    p = parse_product("123", data)
    assert round(p.nutrition.energy_kcal) == 400
    assert p.nutrition.sodium_mg == pytest.approx(1000)
    assert p.category == "food"
    assert "saturated_fat_g" in p.missing and "sugar_g" not in p.missing


def test_beverage_detected():
    p = parse_product("1", {"status": 1, "product": {"categories_tags": ["en:fruit-juices"]}})
    assert p.category == "beverage"


def test_not_found():
    with pytest.raises(LookupError):
        parse_product("1", {"status": 0})
