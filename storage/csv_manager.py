
import pandas as pd
import os
from datetime import datetime, timedelta

CSV_PATH = "product_data.csv"
FRESHNESS_DAYS = 60

def load_csv():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame(columns=["barcode", "product_name", "category", "ingredients", "nutrition", "price", "score", "last_updated"])
    return pd.read_csv(CSV_PATH)

def save_csv(df):
    df.to_csv(CSV_PATH, index=False)

def upsert_product(barcode, product_name, category, ingredients, nutrition, price, score):
    df = load_csv()
    now = datetime.now().strftime("%Y-%m-%d")

    # Convert to string for consistency
    ingredients_str = ", ".join(ingredients) if isinstance(ingredients, list) else ingredients
    nutrition_str = str(nutrition) if isinstance(nutrition, dict) else nutrition

    match = df[df["barcode"] == barcode]
    if not match.empty:
        df.loc[df["barcode"] == barcode, ["product_name", "category", "ingredients", "nutrition", "price", "score", "last_updated"]] = [
            product_name, category, ingredients_str, nutrition_str, price, score, now
        ]
    else:
        df.loc[len(df.index)] = [barcode, product_name, category, ingredients_str, nutrition_str, price, score, now]

    save_csv(df)

def is_product_fresh(barcode):
    df = load_csv()
    match = df[df["barcode"] == barcode]
    if match.empty:
        return False
    last_updated = pd.to_datetime(match.iloc[0]["last_updated"])
    return (datetime.now() - last_updated) <= timedelta(days=FRESHNESS_DAYS)
