
from playwright.sync_api import sync_playwright
import re

def scrape_zepto_product_real(product_name):
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
            # Search for product
            query = product_name.replace(" ", "%20")
            page.goto(f"https://www.zepto.app/search?q={query}", timeout=20000)
            page.wait_for_selector("a[href*='/product/']", timeout=10000)
            product_link = page.locator("a[href*='/product/']").first.get_attribute("href")

            if not product_link:
                return {"error": "No matching product found."}

            # Visit product page
            page.goto(f"https://www.zepto.app{product_link}", timeout=10000)

            # Get title
            result["name"] = page.locator("h1").first.inner_text()

            # Price
            price_text = page.locator("span[class*=Price]").first.inner_text()
            result["price"] = int(re.sub(r"[^\d]", "", price_text))

            # Category breadcrumb (if present)
            if page.locator("nav").count():
                crumbs = page.locator("nav").all_inner_texts()
                if crumbs:
                    result["category"] = crumbs[-1].split(">")[-1].strip().lower()

            # Ingredients or Composition or Nutrition
            page_content = page.content()
            ingredients_match = re.search(r"(?i)(ingredients|composition)</strong>.*?</p><p.*?>(.*?)</p>", page_content)
            if ingredients_match:
                raw_ingredients = ingredients_match.group(2)
                result["ingredients"] = [i.strip().lower() for i in raw_ingredients.split(",") if i.strip()]

            # Nutrition facts table
            facts_matches = re.findall(r"<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>", page_content)
            if facts_matches:
                for key, val in facts_matches:
                    clean_key = re.sub(r"<.*?>", "", key).strip().lower()
                    clean_val = re.sub(r"<.*?>", "", val).strip()
                    result["nutrition_facts"][clean_key] = clean_val

        except Exception as e:
            result = {"error": str(e)}

        finally:
            browser.close()

    return result
