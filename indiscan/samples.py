"""Illustrative profiles of common Indian packaged foods (generic types, not brands).

Values are approximate per 100 g (or 100 ml for beverages) and meant for demos,
tests and tuning the formula. Replace with real label data when available.
"""
from .scoring import Nutrition

# key: (category, Nutrition(energy, sugar, sat fat, trans fat, sodium, protein, fibre), ingredients)
SAMPLES = {
    "instant-noodles": ("food", Nutrition(450, 3, 8, 0.1, 1500, 9, 3),
                        "refined wheat flour, palm oil, salt, flavour enhancer INS 627, INS 631, INS 330"),
    "glucose-biscuit": ("food", Nutrition(450, 22, 4, 0.1, 250, 7, 1),
                        "refined wheat flour, sugar, palm oil, invert syrup, INS 500, INS 503"),
    "bhujia-namkeen": ("food", Nutrition(560, 2, 12, 0.2, 900, 18, 6),
                       "besan, palmolein oil, moth dal, salt, spices"),
    "rolled-oats": ("food", Nutrition(380, 1, 1.3, 0, 5, 13, 10), "whole oats"),
    "roasted-chana": ("food", Nutrition(360, 2, 0.6, 0, 20, 20, 15), "roasted chana, salt"),
    "plain-curd": ("food", Nutrition(60, 4, 1.8, 0, 45, 3.5, 0), "toned milk, curd culture"),
    "cola": ("beverage", Nutrition(42, 10.6, 0, 0, 10, 0, 0),
             "carbonated water, sugar, INS 150d, INS 338, caffeine, added flavour"),
    "fruit-drink": ("beverage", Nutrition(55, 12, 0, 0, 15, 0, 0),
                    "water, sugar, mango pulp, acidity regulator INS 330, INS 211, artificial flavour"),
    "buttermilk": ("beverage", Nutrition(25, 2.5, 0.8, 0, 120, 1.7, 0), "curd, water, salt, jeera"),
}


def score_sample(key: str):
    from .scoring import score_product
    category, nutrition, ingredients = SAMPLES[key]
    return score_product(nutrition, ingredients, category)
