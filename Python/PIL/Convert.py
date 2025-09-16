import codecs
from pathlib import Path
from PIL import Image
import os


def convert(f, lr, to="png"):
    image = Image.open(f).convert("RGB")
    image.save(lr / f"{f.stem}.{to}")
    print(">", f"{f.stem}.{to}")
    f.unlink()


def f_encode(monfile, full_path):
    BLOCKSIZE = 1048576  # or some other, desired size in bytes
    with codecs.open(monfile, "r", encoding="utf-16-le") as sourceFile:
        with codecs.open(f"{full_path}/{monfile}", "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)


def findItem(f):
    pth = r"C:\Users\hp\Music\deemix Music\Musics"
    for c, _, files in os.walk(pth):
        c = c.replace("\\", "/").split("/")[-2:]
        if f in files:
            return "/".join(c)
    return None


def redims(img, w, h, to):
    image = Image.open(img)
    new_image = image.resize((w, h))
    new_image.save(to)


def flip(img):
    with Image.open(f"{img}.jpg") as im:
        # Flip the image horizontally
        flipped_im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        # Save the flipped image
        flipped_im.save(f"flipped_{img}.jpg")


def mosaicing(img):
    with Image.open(f"{img}.jpg") as im:
        # Resize the image to a smaller size
        im = im.resize((100, 100))

        # Create an empty image with the same size
        mosaic = Image.new("RGB", im.size)

        # Divide the image into a grid of cells
        for i in range(0, im.size[0], 10):
            for j in range(0, im.size[1], 10):
                # Get the color of the pixel at the top left corner of the cell
                color = im.getpixel((i, j))

                # Fill the cell with the same color
                mosaic.paste(color, (i, j, i + 10, j + 10))

        # Save the mosaic image
        mosaic.save(f"{img}_mosaic.jpg")


# name = "/home/mohamed/Pictures/insta"
# convert(name, "jpg", "png")
# img = f"{name}.png"
# w = 16
# redims(img, w, w)
# w = 48
# redims(img, w, w)
# w = 128
# redims(img, w, w)

lr = Path("/home/mohamed/Downloads")
parent = Path("/home/mohamed/Pictures")
for f in parent.glob("*.png"):
    to = lr / f.name
    redims(f, 48, 48, to)
