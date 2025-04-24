
from blinkit_real_scraper import scrape_blinkit_product_real
from zepto_real_scraper import scrape_zepto_product_real
from swiggy_real_scraper import scrape_swiggy_product_real
from amazon_real_scraper import scrape_amazon_product_real
from price_comparator import compare_prices

def compare_prices_live(product_name):
    sources = []

    try:
        b = scrape_blinkit_product_real(product_name)
        if "price" in b:
            sources.append({"source": "Blinkit", "price": b["price"]})
    except:
        pass

    try:
        z = scrape_zepto_product_real(product_name)
        if "price" in z:
            sources.append({"source": "Zepto", "price": z["price"]})
    except:
        pass

    try:
        s = scrape_swiggy_product_real(product_name)
        if "price" in s:
            sources.append({"source": "Swiggy", "price": s["price"]})
    except:
        pass

    try:
        a = scrape_amazon_product_real(product_name)
        if "price" in a:
            sources.append({"source": "Amazon", "price": a["price"]})
    except:
        pass

    return compare_prices(product_name, *sources)
