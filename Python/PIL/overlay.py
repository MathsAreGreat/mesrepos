import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont


def titre(k, message, width=1280, height=720):
    fn = f"{k}.jpg"
    name = "result"
    reshaped_p = arabic_reshaper.reshape(message)
    message = get_display(reshaped_p)
    font = ImageFont.truetype("arial.ttf", size=30)
    img = Image.open(fn)
    tt = ImageDraw.Draw(img)
    *_, textWidth, textHeight = tt.textbbox((0, 0), message, font=font)
    xText = (width - textWidth) / 2
    yText = height - textHeight - 20
    tt.text((xText, yText), message, font=font, fill="#fff")
    img.save(f"{name}.jpg")
    return 1
