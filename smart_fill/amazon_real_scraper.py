
from playwright.sync_api import sync_playwright
import re

def scrape_amazon_product_real(product_name):
    result = {
        "name": "",
        "ingredients": [],
        "nutrition_facts": {},
        "category": "",
        "price": 0
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            query = product_name.replace(" ", "+")
            search_url = f"https://www.amazon.in/s?k={query}"
            page.goto(search_url, timeout=20000)

            # Click first product result
            page.wait_for_selector("div.s-result-item[data-component-type='s-search-result'] h2 a", timeout=10000)
            product_link = page.locator("div.s-result-item[data-component-type='s-search-result'] h2 a").first.get_attribute("href")
            if not product_link:
                return {"error": "No product link found"}

            page.goto(f"https://www.amazon.in{product_link}", timeout=15000)

            # Title
            result["name"] = page.locator("#productTitle").first.inner_text().strip()

            # Price
            price_text = page.locator("span.a-price-whole").first.inner_text()
            result["price"] = int(re.sub(r"[^\d]", "", price_text))

            # Ingredients/Composition parsing
            content = page.content()
            ingredients_match = re.search(r"(?i)(ingredients|composition).*?:</b>\s*(.*?)<", content)
            if ingredients_match:
                raw = ingredients_match.group(2)
                result["ingredients"] = [i.strip().lower() for i in raw.split(",") if i.strip()]

            # Nutrition facts table (if food)
            nutrition_matches = re.findall(r"<th.*?>(.*?)</th>\s*<td.*?>(.*?)</td>", content)
            for key, val in nutrition_matches:
                clean_key = re.sub(r"<.*?>", "", key).strip().lower()
                clean_val = re.sub(r"<.*?>", "", val).strip()
                result["nutrition_facts"][clean_key] = clean_val

            # Category from breadcrumbs
            crumbs = page.locator("#wayfinding-breadcrumbs_feature_div ul li span.a-list-item").all_inner_texts()
            if crumbs:
                result["category"] = crumbs[-1].strip().lower()

        except Exception as e:
            result = {"error": str(e)}

        finally:
            browser.close()

    return result
