import hashlib
import os
from bs4 import BeautifulSoup
from plyer import notification
import redis
import requests
from PIL import Image


def cryypt(k, c=10):
    if not isinstance(c, int) or c <= 0:
        return cryypt(k)
    salt = "https://www.google.com"
    url = "https://live.cima4u.live/Episode" + k
    while c:
        url += salt
        url = hashlib.md5(url.encode()).hexdigest()
        c -= 1
    return url


def send_notification(title, message, icone="image"):
    notification.notify(
        title=title,
        message=message,
        app_name="MyApp",
        app_icon="/home/mohamed/Pictures/Notications/"+icone+".ico",
        # Replace with your own icon path
        timeout=5  # Duration in seconds
    )


try:
    rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
except:
    send_notification("Redis Error", "Unable to connect to Redis Server")
    exit()

rds.sadd("notifs:topcima", "delete")
rds.sadd("notifs:footarchives", "delete")

qs = [
    "sakamoto-days",
    "nihon-e-youkoso-elf-san",
    "kusuriya-no-hitorigoto",
    "class-no-daikirai-na-joshi-to-kekkon-suru-koto-ni-natta",
    "reacher",
    "invincible",
    "severance",
    "daredevil-born-again",
    "ao-no-hako",
    "ore-dake-level-up-na-ken",
    "douse-koishite-shimaunda",
    "zenshuu",
    "amagami"
]


r = requests.get(
    "https://web2.topcinema.cam/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d9%86%d9%85%d9%8a/?key=episodes")
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.select("a.recent--block")

for link in links:
    u = link.get("href").strip()
    if rds.sismember("notifs:topcima", u):
        continue
    # print(u)
    for q in qs:
        if q not in u:
            continue
        imgSrc = link.select_one("img")["data-src"]
        img = f'{cryypt(imgSrc)}.jpg'
        # print('>', img)

        with open("/home/mohamed/Pictures/Notications/"+img, "wb") as iml:
            iml.write(requests.get(imgSrc).content)
        imgs = Image.open(
            f"/home/mohamed/Pictures/Notications/{img}")
        imgs.save(
            f"/home/mohamed/Pictures/Notications/{img.rsplit('.', 1)[0]}.ico", format="ICO")

        tt = link.h3.text.strip().split(" ", 1)[-1][:64]
        rds.sadd("notifs:topcima", u)
        send_notification(
            tt,
            u,
            img.rsplit('.', 1)[0]
        )


r = requests.get("https://www.footarchives.com")
soup = BeautifulSoup(r.text, 'html.parser')

articles = soup.select(".Posts-byCategory > article")

for article in articles:
    link = article.a
    u = link.get('href')
    if rds.sismember("notifs:footarchives", u):
        continue
    imgSrc = article.select_one("img.post-thumb").get('data-src')
    tt = link.get('title')

    ext = imgSrc.split(".")[-1]
    cimg = cryypt(imgSrc)
    img = f"{cimg}.{ext}"
    # print('>', img)

    if not os.path.exists("/home/mohamed/Pictures/Notications/"+img):
        with open("/home/mohamed/Pictures/Notications/"+img, "wb") as iml:
            iml.write(requests.get(imgSrc).content)
        imgs = Image.open(
            f"/home/mohamed/Pictures/Notications/{img}")
        imgs.save(
            f"/home/mohamed/Pictures/Notications/{cimg}.ico", format="ICO")

    rds.sadd("notifs:footarchives", u)
    send_notification(
        tt,
        u,
        cimg
    )
