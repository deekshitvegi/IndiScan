"""CLI: python -m indiscan --sugar 12 --sodium 400 --protein 5 -i "wheat flour, palm oil, INS 330" """
import argparse
import json

from . import Nutrition, score_product

FLAGS = {"energy_kcal": "--energy", "sugar_g": "--sugar", "saturated_fat_g": "--sat-fat",
         "trans_fat_g": "--trans-fat", "sodium_mg": "--sodium", "protein_g": "--protein",
         "fibre_g": "--fibre"}

p = argparse.ArgumentParser(prog="indiscan", description="Rate a product out of 1000 (per 100 g / 100 ml).")
for dest, flag in FLAGS.items():
    p.add_argument(flag, dest=dest, type=float, default=0.0)
p.add_argument("-i", "--ingredients", default="")
p.add_argument("-c", "--category", choices=["food", "beverage"], default="food")
a = p.parse_args()
n = Nutrition(**{k: getattr(a, k) for k in FLAGS})
print(json.dumps(score_product(n, a.ingredients, a.category).to_dict(), indent=2))
