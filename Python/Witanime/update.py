from datetime import datetime
import json
from pathlib import Path
import re
import requests
from Mido.variables import monhtml, run_tasks


frn = Path("/home/mohamed/Documents/datas/Daily/dailymotion.json")
with frn.open("r") as el:
    keys = json.load(el)

us = []


def got(u):
    r = requests.get(u)
    return r.json()


fields = ["recent", "old", "random", "id-asc", "visited", "least-visited"]


def save_user(user, fields=None):
    daily_path = Path(f"/home/mohamed/Documents/datas/Daily/Dailymotion/{user}.json")
    if daily_path.exists():
        with daily_path.open("r") as el:
            infos = json.load(el)
    else:
        infos = {}
    us = [
        (
            f"https://api.dailymotion.com/user/{user}/videos?limit=100&page={i + 1}&fields=title,id,duration,thumbnail_url,created_time",
        )
        for i in range(10)
    ]
    if fields:
        us = [
            (
                f"https://api.dailymotion.com/user/{user}/videos?limit=100&page={i + 1}&sort={field}&fields=title,id,duration,thumbnail_url,created_time",
            )
            for i in range(10)
            for field in fields
        ]

    datas = run_tasks(got, us, 10)

    ds = {
        e["id"]: {
            k: (
                v
                if k != "created_time"
                else datetime.fromtimestamp(v).strftime("%Y%m%d_%H%M%S")
            )
            for k, v in e.items()
            if k != "id"
        }
        for info in datas
        for e in info["list"]
        if e["id"] not in infos
    }

    infos.update(ds)

    datas = sorted(infos.items(), key=lambda e: e[-1]["created_time"], reverse=True)
    infos = {k: v for k, v in datas}

    with daily_path.open("w") as el:
        json.dump(infos, el, indent=4)


users = [
    "wsfm99",
]
for user in users:
    print(f"Full : {user}")
    save_user(user, fields=fields)

users = [
    "ahaspoorts",
    "cartoonprofr",
    "naruhinamov",
    "wsfm99",
    "witpaly_tv",
    "Anime4up",
    "king-riad-7",
    "olaoemanga",
    "Ubnkllpzmp2261c3eakoplm",
    "wsfm",
]
for user in users:
    print(f"Latest : {user}")
    save_user(user)

print("Done with users !")


def get_keys(nb):
    u = f"https://witanime.uno/episode/page/{nb}/"
    soup = monhtml(u)
    anime_cards = soup.select(".anime-card-container")
    links = [anime.select("h3") for anime in anime_cards]
    links = [
        (link.a.get("href").split("/")[-2].split("-"), titre.a.text)
        for link, titre in links
        if link.a and titre.a
    ]
    keys = {}
    for link, titre in links:
        ks = [e[0] for e in link if e and not re.findall(r"[^0-9a-z]", e)]
        k = "".join(ks[:-1]).lower()
        if k in keys:
            continue
        ts = re.findall(r"[0-9a-z]+", titre.lower())
        t = " ".join(ts)
        keys[k] = t.title()
    return list(keys.items())


datas = run_tasks(get_keys, [(i + 1,) for i in range(10)])

keys = keys | {k: v for items in datas for k, v in items}

with frn.open("w") as el:
    json.dump(keys, el, indent=4)
