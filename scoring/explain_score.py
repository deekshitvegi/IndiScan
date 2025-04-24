
import re

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

def explain_ingredient_risks(ingredients_list, mode="food"):
    risk_dict = FOOD_RISKS if mode == "food" else COSMETIC_RISKS
    risky_found = {}
    unknown = []

    for ingredient in ingredients_list:
        match = False
        for risk_item in risk_dict:
            if risk_item in ingredient.lower():
                risky_found[ingredient.strip()] = risk_dict[risk_item]
                match = True
                break
        if not match:
            unknown.append(ingredient.strip())

    return risky_found, unknown

def format_explanation(risky_dict, unknown_list):
    """
    Converts the risk and unknown data into user-facing text.
    """
    output = []
    if not risky_dict:
        output.append("✅ No risky ingredients detected!")

    else:
        output.append("⚠️ **Risky Ingredients Detected:**")
        for ing, penalty in risky_dict.items():
            output.append(f"- **{ing}** → {penalty}")

    if unknown_list:
        output.append("\n🔍 **Unknown Ingredients (unscored):**")
        for u in unknown_list:
            output.append(f"- {u}")

    return "\n".join(output)
