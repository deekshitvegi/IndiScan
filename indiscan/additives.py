"""Additive / ingredient risk table (INS numbers as printed on Indian labels).

risk: 1 = low concern, 2 = moderate, 3 = high. Based on FSSAI permitted-additive
lists plus common consumer-health concerns; edit freely, it is plain data.
"""
import re

ADDITIVE_RISK = {
    # colours
    "102": 3, "110": 3, "122": 3, "123": 3, "124": 3, "129": 3, "133": 2,
    "150d": 2, "150c": 2, "160a": 1, "160b": 1, "101": 1, "100": 1,
    # preservatives
    "211": 2, "212": 2, "202": 1, "200": 1, "223": 2, "250": 3, "251": 3,
    "220": 2, "221": 2, "222": 2, "224": 2,
    # sweeteners
    "951": 2, "950": 2, "955": 2, "954": 2, "952": 3, "962": 2,
    # flavour enhancers
    "621": 2, "627": 2, "631": 2,
    # antioxidants / emulsifiers / misc
    "320": 3, "321": 3, "319": 2, "310": 2, "471": 1, "322": 1, "407": 1,
    "412": 1, "415": 1, "330": 1, "300": 1, "500": 1, "503": 1, "508": 1,
    "450": 2, "452": 2, "339": 2, "341": 2,
}

# Non-INS ingredient red flags: (regex, risk, label)
INGREDIENT_FLAGS = [
    (r"palm\s*(oil|olein)|palmolein", 2, "palm oil"),
    (r"hydrogenated|vanaspati|shortening|margarine", 3, "hydrogenated fat"),
    (r"refined wheat flour|maida", 1, "maida"),
    (r"high fructose|invert syrup|liquid glucose|glucose syrup", 2, "added sugar syrup"),
    (r"artificial (flavou?r|color|colour)|nature identical|added flavou?r", 1, "artificial flavour/colour"),
    (r"monosodium glutamate|\bmsg\b", 2, "MSG"),
]

# Ingredients that count towards "wholesome content"
WHOLESOME = re.compile(
    r"\b(whole wheat|atta|oats?|ragi|millet|jowar|bajra|dal|lentil|chana|besan|"
    r"almonds?|cashews?|peanuts?|nuts?|walnuts?|pista|raisins?|dates?|fruits?|vegetables?|"
    r"tomato|spinach|milk|curd|paneer|yogh?urt|seeds?|flax|quinoa|brown rice)\b", re.I)

INS_RE = re.compile(r"\b(?:INS|E)\s*[-:]?\s*(\d{3}[a-z]?)", re.I)
