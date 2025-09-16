from PIL import Image
from pathlib import Path


def white(f, *tos):
    img = Image.open(f)
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    threshold = 150
    for pixel in data:
        if pixel[0] > threshold and pixel[1] > threshold and pixel[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(pixel)

    img.putdata(new_data)
    for to in tos:
        fn = to / f.name
        if fn.exists():
            fn.unlink()
        img.save(fn)
    if fn.exists():
        f.unlink()
    return 1


lr = Path("/var/www/html/laralil/public/images")
ph = Path("/var/www/html/Tailwins/images")
parent = Path("/home/mohamed/Pictures/Screenshots")
for f in parent.glob("*png"):
    white(f, lr, ph)
