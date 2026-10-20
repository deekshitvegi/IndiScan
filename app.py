"""Gradio UI for IndiScan: enter nutrition per 100 g / 100 ml, get a 0-1000 rating."""
import gradio as gr

from indiscan import Nutrition, score_product


def rate(category, energy, sugar, sat_fat, trans_fat, sodium, protein, fibre, ingredients):
    r = score_product(Nutrition(energy, sugar, sat_fat, trans_fat, sodium, protein, fibre),
                      ingredients, category)
    rows = [[k, v] for k, v in r.components.items()]
    return f"{r.score} / 1000  —  Grade {r.grade} ({r.label})", rows, "\n".join(r.flags) or "None"


demo = gr.Interface(
    rate,
    [gr.Radio(["food", "beverage"], value="food", label="Category"),
     gr.Number(label="Energy (kcal)", value=0), gr.Number(label="Sugar (g)", value=0),
     gr.Number(label="Saturated fat (g)", value=0), gr.Number(label="Trans fat (g)", value=0),
     gr.Number(label="Sodium (mg)", value=0), gr.Number(label="Protein (g)", value=0),
     gr.Number(label="Fibre (g)", value=0),
     gr.Textbox(label="Ingredients (as printed on label)", lines=3)],
    [gr.Textbox(label="IndiScan score"),
     gr.Dataframe(headers=["Component", "Points"], label="Breakdown"),
     gr.Textbox(label="Flags")],
    title="IndiScan", description="Indian product health rating out of 1000 (values per 100 g / 100 ml).")

if __name__ == "__main__":
    demo.launch()
