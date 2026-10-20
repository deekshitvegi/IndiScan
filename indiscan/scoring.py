"""IndiScan score: a 0-1000 rating from nutrition facts and ingredients.

All nutrition inputs are per 100 g (solids) or per 100 ml (beverages).

Breakdown (max points)
  Penalties (start full, lose points as the nutrient rises):
    energy 100 | sugar 150 | saturated fat 100 | trans fat 50 | sodium 150  = 550
  Rewards (earn points as the nutrient rises):
    protein 100 | fibre 100 | wholesome ingredients 50                       = 250
  Additives & ingredient quality (start full, lose points per risk)          = 200
                                                                      total = 1000

Each nutrient is scored linearly between a "best" and a "worst" threshold,
tighter for beverages. Thresholds follow FSSAI/ICMR-NIN guidance and WHO limits.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict

from .additives import ADDITIVE_RISK, INGREDIENT_FLAGS, INS_RE, WHOLESOME

MAX_SCORE = 1000

# name: (max_points, best, worst) -- best -> full points, worst -> 0
_PENALTY = {
    "food": {
        "energy_kcal": (100, 100, 550),
        "sugar_g": (150, 2, 25),
        "saturated_fat_g": (100, 1, 10),
        "trans_fat_g": (50, 0, 1),
        "sodium_mg": (150, 100, 900),
    },
    "beverage": {
        "energy_kcal": (100, 10, 60),
        "sugar_g": (150, 0.5, 11),
        "saturated_fat_g": (100, 0.5, 3),
        "trans_fat_g": (50, 0, 0.5),
        "sodium_mg": (150, 20, 300),
    },
}
# name: (max_points, zero_at, full_at)
_REWARD = {
    "food": {"protein_g": (100, 1, 15), "fibre_g": (100, 1, 8)},
    "beverage": {"protein_g": (100, 0, 4), "fibre_g": (100, 0, 2)},
}
WHOLESOME_MAX = 50
ADDITIVE_MAX = 200
ADDITIVE_COST = {1: 15, 2: 40, 3: 80}

GRADES = [(800, "A", "Excellent"), (600, "B", "Good"), (400, "C", "Mediocre"),
          (200, "D", "Poor"), (0, "E", "Avoid")]


@dataclass
class Nutrition:
    energy_kcal: float = 0.0
    sugar_g: float = 0.0
    saturated_fat_g: float = 0.0
    trans_fat_g: float = 0.0
    sodium_mg: float = 0.0
    protein_g: float = 0.0
    fibre_g: float = 0.0


@dataclass
class ScoreResult:
    score: int
    grade: str
    label: str
    components: dict = field(default_factory=dict)
    flags: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def _linear(value: float, lo: float, hi: float) -> float:
    """0..1 position of value between lo and hi (clamped)."""
    if hi == lo:
        return 0.0
    return min(1.0, max(0.0, (value - lo) / (hi - lo)))


def find_additives(ingredients: str) -> list[tuple[str, int]]:
    """Return [(label, risk)] for INS codes and flagged ingredients."""
    found: dict[str, int] = {}
    text = ingredients or ""
    for code in INS_RE.findall(text):
        code = code.lower()
        found[f"INS {code}"] = ADDITIVE_RISK.get(code, ADDITIVE_RISK.get(code[:3], 1))
    low = text.lower()
    for pattern, risk, label in INGREDIENT_FLAGS:
        if re.search(pattern, low):
            found[label] = risk
    return list(found.items())


def wholesome_fraction(ingredients: str) -> float:
    """Share of the first five listed ingredients that are wholesome (0..1).

    Ingredients are listed by descending weight, so only the head counts.
    """
    parts = [p.strip() for p in (ingredients or "").replace(";", ",").split(",") if p.strip()]
    head = parts[:5]
    if not head:
        return 0.0
    return sum(1 for p in head if WHOLESOME.search(p)) / len(head)


def score_product(nutrition: Nutrition, ingredients: str = "", category: str = "food") -> ScoreResult:
    if category not in _PENALTY:
        raise ValueError(f"category must be one of {sorted(_PENALTY)}")
    for k, v in asdict(nutrition).items():
        if v < 0:
            raise ValueError(f"{k} cannot be negative")

    comp: dict[str, float] = {}
    for name, (pts, best, worst) in _PENALTY[category].items():
        comp[name] = round(pts * (1 - _linear(getattr(nutrition, name), best, worst)), 1)
    for name, (pts, zero, full) in _REWARD[category].items():
        comp[name] = round(pts * _linear(getattr(nutrition, name), zero, full), 1)
    comp["wholesome"] = round(WHOLESOME_MAX * min(1.0, wholesome_fraction(ingredients) / 0.6), 1)

    adds = find_additives(ingredients)
    comp["additives"] = float(max(0, ADDITIVE_MAX - sum(ADDITIVE_COST[r] for _, r in adds)))

    total = round(sum(comp.values()))
    flags = [f"{n} (risk {r})" for n, r in adds]
    # A product cannot rate "Good" with a high-risk additive or heavy trans fat.
    if (any(r == 3 for _, r in adds) or nutrition.trans_fat_g >= 2) and total > 599:
        total = 599
        flags.append("score capped at 599: high-risk additive or trans fat >= 2 g")
    total = max(0, min(MAX_SCORE, total))
    grade, label = next((g, l) for floor, g, l in GRADES if total >= floor)
    return ScoreResult(total, grade, label, comp, flags)
