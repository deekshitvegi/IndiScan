
import re

# Define risk dictionaries separately for food and cosmetic items
FOOD_RISKS = {
    "high fructose corn syrup": -200,
    "palm oil": -150,
    "sodium benzoate": -180,
    "msg": -150,
    "artificial flavor": -120,
    "sodium nitrite": -200,
    "refined flour": -130,
    "sugar": -100,
    "salt": -70,
    "color": -60,
    "preservative": -90
}

COSMETIC_RISKS = {
    "paraben": -200,
    "sodium lauryl sulfate": -150,
    "sodium laureth sulfate": -130,
    "fragrance": -120,
    "alcohol denat": -110,
    "triclosan": -180,
    "polyethylene glycol": -100,
    "dimethicone": -90,
    "silicone": -80,
    "formaldehyde": -220
}

def calculate_position_weighted_score(ingredients_list, mode="food"):
    """
    Compute a health score based on position-aware ingredient risk penalties.
    Mode can be 'food' or 'cosmetic'.
    """
    risk_dict = FOOD_RISKS if mode == "food" else COSMETIC_RISKS
    score = 1000

    for i, ingredient in enumerate(ingredients_list):
        ingredient = ingredient.strip().lower()
        for risk_item, penalty in risk_dict.items():
            if risk_item in ingredient:
                # Apply position-based scaling (early ingredients are more impactful)
                position_factor = max(1.0 - (i / len(ingredients_list)), 0.3)
                score += int(penalty * position_factor)

    return max(0, min(score, 1000))
