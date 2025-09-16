import hashlib
from datetime import datetime, timezone
from time import sleep

import notify2
import redis
import requests
from bs4 import BeautifulSoup


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


def send_notification(head, title, message, img):
    dt = datetime.now(timezone.utc).strftime("%H:%M:%S")
    notify2.init(f"{head} {dt}")
    img = f"/home/mohamed/Pictures/Notications/{img}.png"
    n = notify2.Notification(title, message, img)
    n.set_timeout(300)
    n.show()


try:
    rds = redis.Redis(host="localhost", port=6379, decode_responses=True)
except:
    send_notification("Redis Error", "Unable to connect to Redis Server")
    exit()


# qs = [
#     "sakamoto-days",
#     "nihon-e-youkoso-elf-san",
#     "kusuriya-no-hitorigoto",
#     "class-no-daikirai-na-joshi-to-kekkon-suru-koto-ni-natta",
#     "reacher",
#     "invincible",
#     "severance",
#     "daredevil-born-again",
#     "ao-no-hako",
#     "ore-dake-level-up-na-ken",
#     "douse-koishite-shimaunda",
#     "zenshuu",
#     "amagami",
# ]


# r = requests.get(
#     "https://web2.topcinema.cam/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d9%86%d9%85%d9%8a/?key=episodes"
# )
# soup = BeautifulSoup(r.text, "html.parser")
# links = soup.select("a.recent--block")

# for link in links:
#     u = link.get("href").strip()
#     if rds.sismember("notifs:topcima", u):
#         continue
#     # print(u)
#     for q in qs:
#         if q not in u:
#             continue
#         img = "topcima"
#         tt = link.h3.text.strip().split(" ", 1)[-1][:64]
#         send_notification("TopCima Item", tt, u, img)
#         rds.sadd("notifs:topcima", u)


r = requests.get("https://www.footarchives.com/search")
soup = BeautifulSoup(r.text, "html.parser")

articles = soup.select(".Posts-byCategory article")

for article in articles:
    link = article.a
    u = link.get("href")
    if rds.sismember("notifs:footarchives", u):
        continue
    imgSrc = article.select_one("img.post-thumb")
    if not imgSrc:
        continue
    tt = link.get("title")

    ext = imgSrc.get("data-src").split(".")[-1]
    cimg = "footarcheive"

    rds.sadd("notifs:footarchives", u)
    send_notification("Foot Item", tt, u, cimg)
    sleep(1)
