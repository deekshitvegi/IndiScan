
from playwright.sync_api import sync_playwright
import re

def scrape_blinkit_product_real(product_name):
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
            search_url = f"https://blinkit.com/s/?q={product_name.replace(' ', '%20')}"
            page.goto(search_url, timeout=20000)
            page.wait_for_selector(".ProductCard__Container-sc-__sc-1lwz2hl-0", timeout=10000)
            product_link = page.locator(".ProductCard__Container-sc-__sc-1lwz2hl-0 a").first.get_attribute("href")

            if not product_link:
                return {"error": "No product link found"}

            # Visit product page
            page.goto(f"https://blinkit.com{product_link}", timeout=10000)

            # Extract name
            result["name"] = page.locator("h1").first.inner_text()

            # Price
            price_text = page.locator(".Price__StyledPrice-sc-1ruxxnv-0").first.inner_text()
            result["price"] = int(re.sub(r"[^\d]", "", price_text))

            # Category (breadcrumb)
            breadcrumbs = page.locator(".Breadcrumbs__StyledBreadcrumbs-sc-1v4mt1p-0").all_inner_texts()
            if breadcrumbs:
                result["category"] = breadcrumbs[-1].split(">")[-1].strip().lower()
            else:
                result["category"] = "unknown"

            # Ingredients or Composition
            all_html = page.content()
            ingredients_match = re.search(r"Ingredients.*?</strong>(.*?)<", all_html, re.IGNORECASE)
            if not ingredients_match:
                ingredients_match = re.search(r"Composition.*?</strong>(.*?)<", all_html, re.IGNORECASE)

            if ingredients_match:
                raw = ingredients_match.group(1)
                result["ingredients"] = [i.strip().lower() for i in raw.split(",") if i.strip()]

            # Nutrition facts table
            facts_matches = re.findall(r"<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>", all_html)
            for key, val in facts_matches:
                clean_key = re.sub(r"<.*?>", "", key).strip().lower()
                clean_val = re.sub(r"<.*?>", "", val).strip()
                result["nutrition_facts"][clean_key] = clean_val

        except Exception as e:
            result = {"error": str(e)}

        finally:
            browser.close()

    return result
