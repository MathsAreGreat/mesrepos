import json
from pathlib import Path
import re

import requests

from Mido.variables import aria_dwn, egybest, monhtml

u = "https://us.soccerway.com/v1/english/participant/soccer/full/2017/"
u = "https://us.soccerway.com/v1/english/stage/soccer/spain/primera-division/20242025/r82318/"
u = "https://us.soccerway.com/legacy/v1/english/matches/?stageId=r18&limit=10000"
# r = requests.get(u)

# with Path("soccerway_r.json").open("w") as f:
#     json.dump(r.json(), f)

# t = "Tensei shitara Dainana Ouji Datta node, Kimama ni Majutsu wo Kiwamemasu 2nd Season الحلقة 1"

# dd = egybest("c", t, "1080", "Wits")
# print(dd)

ref = "https://ak.sv"
cle = "10141"
url = f"{ref}/movie/{cle}"
soup = monhtml(url)

tt = soup.h1.text.strip()

print("> Titre :", tt)
print("=" * 50)
print("=" * 50)

# print(soup.find("a", download=True).get("href"))

tags = [li.text.strip() for li in soup.find(class_="header-tabs").select("li")]

links = [
    (
        re.findall(r"[0-9-a-z\s\.]+", link.text, flags=re.IGNORECASE)[-1].strip(),
        link.get("href").split("/")[-1],
    )
    for link in soup.select("a.link-download")
]

for tag, (size, key) in zip(tags, links):
    dl = f"{ref}/download/{key}/10141"
    soup = monhtml(dl)
    uri = soup.find("a", download=True).get("href")
    aria_dwn(
        url,
        "/home/mohamed/Downloads/Library/Movies",
        uri,
        f"[Akwam].{tt}.({key}-{cle}).mp4",
        False,
    )
    break
