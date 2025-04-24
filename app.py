import gradio as gr
import pandas as pd
from scoring.risk_model import calculate_risk_score
from scoring.explain_score import explain_ingredient_risks, format_explanation
from scoring.score_recommender import get_recommendations
from smart_fill.openfoodfacts_api import fetch_openfoodfacts_data
from smart_fill.amazon_real_scraper import scrape_amazon_product
from smart_fill.blinkit_real_scraper import scrape_blinkit_product
from smart_fill.zepto_real_scraper import scrape_zepto_product
from smart_fill.swiggy_real_scraper import scrape_swiggy_product
from storage.csv_manager import load_data, save_product
from utils.ocr_utils import extract_text_from_image
from utils.price_comparator import compare_prices

product_df = load_data()

def process_product(image, name, category, nutrition, ingredients, admin_mode, smart_autofill):
    barcode = "Simulated1234567890"
    
    if smart_autofill and not ingredients:
        fetched = fetch_openfoodfacts_data(barcode)
        if not fetched:
            fetched = scrape_amazon_product(name) or scrape_blinkit_product(name) or scrape_zepto_product(name)
        if fetched:
            name = fetched.get("name", name)
            category = fetched.get("category", category)
            ingredients = ", ".join(fetched.get("ingredients", []))
            nutrition = nutrition or "Not provided"

    ingredients_list = [i.strip().lower() for i in ingredients.split(",")]
    
    score = calculate_risk_score(ingredients_list)
    explanation = format_explanation(explain_ingredient_risks(ingredients_list))
    
    best_deal = compare_prices(name)
    price_info = f"Best Price: ₹{best_deal['best_price']} on {best_deal['best_source']}" if best_deal else "Price info unavailable"

    status = "Cannot add product."
    if admin_mode:
        save_product(name, category, nutrition, ingredients_list, barcode, score)
        status = "✅ Product added to database."

    similar = get_recommendations(product_df, ingredients_list, category)

    return (
        f"Health Score: {score}/1000\n{price_info}",
        explanation,
        status,
        similar
    )

image_input = gr.Image(label="Upload or Take a Picture of Product")
text_name = gr.Text(label="Product Name")
dropdown_category = gr.Dropdown(["Food", "Bath & Beauty"], label="Category")
text_nutrition = gr.Text(label="Nutrition (e.g., 2g protein, 110 cal, 135mg sodium)")
text_ingredients = gr.Text(label="Ingredients (comma separated)")
admin_check = gr.Checkbox(label="👑 Admin Mode (Allow Product Additions)")
smart_fill_check = gr.Checkbox(label="Use Smart Auto-Fill", value=True)

output_score = gr.Textbox(label="Score")
output_explanation = gr.Textbox(label="Risk Breakdown")
output_status = gr.Textbox(label="Status")
output_recommendation = gr.Textbox(label="Recommended Alternatives")

app = gr.Interface(
    fn=process_product,
    inputs=[image_input, text_name, dropdown_category, text_nutrition, text_ingredients, admin_check, smart_fill_check],
    outputs=[output_score, output_explanation, output_status, output_recommendation],
    title="IndiScan: Indian Product Health Analyzer",
    description="Scan food or cosmetic products, analyze ingredients, and find healthier options!"
)

if __name__ == "__main__":
    app.launch()
