---
title: IndiScan
emoji: 🧃
colorFrom: indigo
colorTo: pink
sdk: gradio
sdk_version: "4.15.0"
app_file: app.py
pinned: false
---

# IndiScan

A Yuka-style health rating for Indian packaged foods and drinks, scored **out of 1000**.

```
python -m indiscan --energy 450 --sugar 12 --sodium 400 --protein 5 -i "wheat flour, palm oil, INS 330"
python app.py          # Gradio UI
python -m indiscan --barcode 8901058852387   # Open Food Facts lookup
python -m pytest tests
```

## The 1000-point formula (per 100 g, or per 100 ml for beverages)

| Part | Max | How it scores |
|---|---|---|
| Energy | 100 | full at ≤100 kcal, 0 at ≥550 (beverage: 10 / 60) |
| Sugar | 150 | full at ≤2 g, 0 at ≥25 g (beverage: 0.5 / 11) |
| Saturated fat | 100 | full at ≤1 g, 0 at ≥10 g (beverage: 0.5 / 3) |
| Trans fat | 50 | full at 0, 0 at ≥1 g (beverage: 0.5) |
| Sodium | 150 | full at ≤100 mg, 0 at ≥900 mg (beverage: 20 / 300) |
| Protein | 100 | 0 at ≤1 g, full at ≥15 g (beverage: 4) |
| Fibre | 100 | 0 at ≤1 g, full at ≥8 g (beverage: 2) |
| Wholesome ingredients | 50 | share of top-5 ingredients that are whole grains, pulses, nuts, fruit, veg, dairy |
| Additives & ingredient quality | 200 | 200 minus 15/40/80 per low/moderate/high-risk INS code or red-flag ingredient (palm oil, hydrogenated fat, maida, MSG…) |

Each nutrient is linear between its best and worst threshold. A high-risk additive or ≥2 g trans fat caps the score at 599.

Grades: **A** ≥800 Excellent · **B** ≥600 Good · **C** ≥400 Mediocre · **D** ≥200 Poor · **E** <200 Avoid.

Thresholds and the additive table (`indiscan/additives.py`) are plain data meant to be tuned.

## Roadmap
Label OCR, product database, Indian-brand price comparison.
