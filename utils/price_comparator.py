
def compare_prices(product_name, *sources):
    """
    Compare product prices from multiple sources.
    Input: product_name (string), sources (list of dicts)
    Each source should be a dict like:
    {"source": "Blinkit", "price": 50}
    
    Returns the cheapest source and a sorted list.
    """
    valid_sources = [s for s in sources if "price" in s and isinstance(s["price"], (int, float))]
    
    if not valid_sources:
        return {"error": "No valid price data provided"}
    
    sorted_sources = sorted(valid_sources, key=lambda x: x["price"])
    best = sorted_sources[0]
    
    return {
        "product": product_name,
        "best_price": best["price"],
        "best_source": best["source"],
        "comparison": sorted_sources
    }
