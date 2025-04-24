
import pytesseract
from PIL import Image
import re

def extract_ingredients_from_image(image_path):
    """
    Extracts text from an image and searches for ingredients block.
    Returns cleaned list of ingredients (if found).
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Look for line starting with 'Ingredients' or 'Composition'
        ingredients_text = ""
        for line in text.split("\n"):
            if re.search(r"(?i)ingredients|composition", line):
                ingredients_text = line
                break

        if not ingredients_text:
            return {"error": "Ingredients not found"}

        ingredients_list = re.split(r",|•|-|–", ingredients_text.split(":")[-1])
        cleaned = [i.strip().lower() for i in ingredients_list if len(i.strip()) > 1]
        return cleaned

    except Exception as e:
        return {"error": str(e)}
