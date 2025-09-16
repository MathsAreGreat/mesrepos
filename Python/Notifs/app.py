import os
from bs4 import BeautifulSoup
import requests


def send_notification(title, message, img):
    os.system(
        f'notify-send -i "{img}" "{title}" "{message}"')


r = requests.get("https://web2.topcinema.cam/recent/")
soup = BeautifulSoup(r.text, 'html.parser')
link = soup.select_one("a.recent--block")
u = link.get("href")
imgSrc = link.select_one("img")["data-src"]
img = "/home/mohamed/Pictures/Notications/" + \
    imgSrc.split('/')[-1]

if not os.path.exists(img):
    with open(img, "wb") as iml:
        iml.write(requests.get(imgSrc).content)


if link:
    tt = link.h3.text.strip()
    send_notification(
        tt,
        u,
        img
    )
