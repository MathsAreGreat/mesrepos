from PIL import Image
import os


def resize(name,nw=200):
    image = Image.open(f"test/{name}.png")
    w, h = image.size
    if w == h == nw:
        print(name, "is indeed", w, "x", h)
    else:
        new_image = image.resize((nw, nw))
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

os.chdir(r'C:\Users\hp\Documents\IMPORTANT\BeOut\Site\imgs')
for f in os.listdir("test"):
    name,ex=os.path.splitext(f)
    if ex == ".png":
        resize(name)
