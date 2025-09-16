from PIL import ExifTags, Image


def resize(name):
    image = Image.open(f"{name}.png")
    w, h = image.size
    if w == h == 512:
        print(name, "is indeed", w, "x", h)
    else:
        new_image = image.resize((512, 512))
        new_image.save(f"{name}.png")


def i_rotate(name, angle=90):
    im = Image.open(f"{name}.png")
    out = im.rotate(angle, expand=True)
    out.save(f"rotate_{name}.png")


def nobg(name, ex=".png"):
    img = Image.open(f"{name}{ex}")
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(f"{name}.png", "PNG")


name = r"C:\wamp64\www\mathematics\public\imgs\exp1"
image = Image.open(f"{name}.png")

exif = {ExifTags.TAGS[k]:v for k,v in image._getexif().items()}