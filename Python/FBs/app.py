

import json
from pathlib import Path
from time import sleep
import webbrowser


def gop(k):
    url = f"https://www.facebook.com/photo/?fbid={k}"
    webbrowser.open(url)
    return None


nb = 1


uns = []

ids = [
    f.stem.split("_")[1]
    for f in Path('/home/mohamed/Documents/.Socials/Facebooks/Vides').rglob("*.jpg")
    if f.stat().st_size < 10
]
pt = "/home/mohamed/Documents/Stuff/Jups"
for f in Path(pt).rglob("*.json"):
    with open(f, "r") as file:
        data = json.load(file)
    ids += [e[1:] for e in data["IDs"] if e[0] not in "0123456789"]

uns = [
    f.stem.split("_")[1]
    for f in Path('/home/mohamed/Documents/.Socials').rglob("*.jpg")
    if f.parent.name != "Vides"
]

IDs = [e for e in set(ids) if e not in uns]


print(len(IDs), "items !", " "*20, end="\r")
i = 0
while IDs:
    for k in IDs[:10]:
        gop(k)
        sleep(1)

    IDs = IDs[10:]
    files = 0
    while not files:
        files = list(Path("/home/mohamed/Downloads").glob("*json"))
    sleep(2)
    while files:
        files = list(Path("/home/mohamed/Downloads").glob("*json"))
        sleep(2)
    print(len(IDs), "items !", " "*20, end="\r")
# os.system("clear")

# print(uns)
