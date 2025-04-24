
import pandas as pd
from difflib import SequenceMatcher

def recommend_healthier_alternatives(current_product_name, current_score, category, ingredients, data_path="product_data.csv"):
    """
    Recommends two alternatives from the dataset:
    - One with better nutrition score in the same category
    - One with the most similar ingredients but better score
    """
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        return {"error": f"Failed to load data: {e}"}

    df = df[df["category"].str.lower() == category.lower()]
    df = df[df["score"] > current_score]

    if df.empty:
        return {"message": "No better alternatives found."}

    # Recommendation 1: Highest scoring product in category
    best_score_row = df.loc[df["score"].idxmax()]
    best_nutrition = {
        "name": best_score_row["name"],
        "score": best_score_row["score"]
    }

    # Recommendation 2: Most similar ingredients with better score
    def ingredient_similarity(row):
        return SequenceMatcher(None, str(row["ingredients"]).lower(), ",".join(ingredients).lower()).ratio()

    df["ingredient_similarity"] = df.apply(ingredient_similarity, axis=1)
    most_similar_row = df.sort_values(by="ingredient_similarity", ascending=False).iloc[0]

    most_similar = {
        "name": most_similar_row["name"],
        "score": most_similar_row["score"]
    }

    return {
        "better_nutrition": best_nutrition,
        "better_similarity": most_similar
    }
