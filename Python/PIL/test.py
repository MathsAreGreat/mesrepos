# Import the Image and ImageFilter modules from PIL
from PIL import Image
import os

# Open an image file
def convert(fn, to="jpg"):
    name, ex= fn.rsplit('.',1)
    image = Image.open(f"{name}.{ex}").convert("RGB")
    image.save(f"{name}.{to}")
    print(">", f"{name}.{to}")
    os.remove(f"{name}.{ex}")
