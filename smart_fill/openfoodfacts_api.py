
import requests

def fetch_openfoodfacts(barcode):
    """
    Query OpenFoodFacts for product data using barcode.
    Returns: dict with product name, ingredients (split), nutriments, and category
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code != 200:
            return None
        data = res.json()
        if not data.get("product"):
            return None

        product = data["product"]
        ingredients_text = product.get("ingredients_text", "") or ""
        ingredients = [i.strip() for i in ingredients_text.split(",") if i.strip()]

        return {
            "name": product.get("product_name", ""),
            "ingredients": ingredients,
            "nutriments": product.get("nutriments", {}),
            "category": product.get("categories", "").split(",")[0].strip() if product.get("categories") else "unknown"
        }

    except Exception as e:
        return {"error": str(e)}
