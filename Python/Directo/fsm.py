import json
import re
from pathlib import Path

from functions import cryypt, dwn, eps

infos_path = Path("/home/mohamed/Documents/datas/infos.json")
info_path = Path("infos.json")

us = [
    "https://shahhid4u.com/watch/%D9%81%D9%8A%D9%84%D9%85-lyle,-lyle,-crocodile-2022-%D9%85%D8%AA%D8%B1%D8%AC%D9%85-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86"
]
with info_path.open("r") as e:
    us += json.load(e)

doom = "https://shahhid4u.com"
try:
    with infos_path.open("r") as e:
        links = json.load(e)
except FileNotFoundError:
    links = {"mvs": [], "shvip": []}

liens = [re.findall(r"[^/]+", u)[-1] for u in links["mvs"]]
liens = [f"{doom}/watch/{u}" for u in liens]
links["mvs"] = liens
us += links["mvs"]

uniques = [f.name for f in Path("/home/mohamed/Documents/datas/Backups").glob("*")]

uniques += [f.stem.split(".")[-1][1:-1] for f in Path("Library").rglob("*).mp4")]
uniques += [
    f.stem.split(".")[-1][1:-1]
    for f in Path("/home/mohamed/Downloads/Library").rglob("*).mp4")
]

liens = [re.findall(r"[^/]+", u)[-1] for u in links["shvip"]]
liens = [f"{doom}/watch/{u}" for u in liens]
links["shvip"] = liens
with infos_path.open("w") as e:
    json.dump(links, e, indent=2)

for link in liens:
    if link:
        print(link)
        us += eps(link)

liens = [re.findall(r"[^/]+", u)[-1] for u in us]
us = [f"{doom}/watch/{u}" for u in set(liens)]

nb = len(us)
for u in us:
    print(cryypt(u), ":", u.split("/")[-1])

print("*****************************")

us = [u for u in dict.fromkeys(us) if u and cryypt(u) not in uniques]
print(nb, "items !")
with info_path.open("w") as fl:
    json.dump(us, fl, indent=2)

cc = 2
while nb:
    nb = 0
    uniques += [f.stem.split(".")[-1][1:-1] for f in Path("Library").rglob("*).mp4")]
    for u in us:
        c = cryypt(u)
        fn = Path(f"/home/mohamed/Documents/datas/Backups/{c}")
        if fn.exists() or c in uniques:
            continue
        v = dwn(u)

# for f in Path("Library").rglob("*).mp4"):
#     if not f.is_file():
#         continue
#     fn = Path("/home/mohamed/Downloads") / f
#     fn.parent.mkdir(exist_ok=True, parents=True)
#     f.rename(fn)

# nb = 1
# while nb:
#     nb = 0
#     for doc in Path("Library").rglob("*"):
#         try:
#             doc.rmdir()
#             nb += 1
#         except:
#             pass
