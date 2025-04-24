
from playwright.sync_api import sync_playwright
import re

def scrape_swiggy_product_real(product_name):
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
            # Navigate to Swiggy Instamart search
            query = product_name.replace(" ", "%20")
            search_url = f"https://www.swiggy.com/instamart/search?query={query}"
            page.goto(search_url, timeout=20000)

            # Wait for product link
            page.wait_for_selector("a[href*='/instamart/product/']", timeout=10000)
            product_link = page.locator("a[href*='/instamart/product/']").first.get_attribute("href")
            if not product_link:
                return {"error": "No product found"}

            # Navigate to product page
            page.goto(f"https://www.swiggy.com{product_link}", timeout=10000)

            # Product title
            result["name"] = page.locator("h1").first.inner_text()

            # Price
            price_text = page.locator("div[class*=price]").first.inner_text()
            result["price"] = int(re.sub(r"[^\d]", "", price_text))

            # Extract raw HTML for ingredient and nutrition info
            html = page.content()

            # Ingredients or Composition
            ingredients_match = re.search(r"(ingredients|composition).*?</strong>(.*?)<", html, re.IGNORECASE)
            if ingredients_match:
                raw = ingredients_match.group(2)
                result["ingredients"] = [i.strip().lower() for i in raw.split(",") if i.strip()]

            # Nutrition Facts
            facts_matches = re.findall(r"<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>", html)
            for key, val in facts_matches:
                clean_key = re.sub(r"<.*?>", "", key).strip().lower()
                clean_val = re.sub(r"<.*?>", "", val).strip()
                result["nutrition_facts"][clean_key] = clean_val

            # Category from breadcrumb (if exists)
            crumbs = page.locator("nav").all_inner_texts()
            if crumbs:
                result["category"] = crumbs[-1].split(">")[-1].strip().lower()
            else:
                result["category"] = "unknown"

        except Exception as e:
            result = {"error": str(e)}

        finally:
            browser.close()

    return result
