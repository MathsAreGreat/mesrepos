import json
import os
from pathlib import Path

from Mido.variables import run_tasks

DOM = "https://www.facebook.com/watch?v=1373925334045954"
DOM = "https://www.youtube.com"
parent = Path("/home/mohamed/.Kindas/Youtube")


def viding(nbr, nb=0):
    q = "bestaudio+bestvideo/best"
    dp = f"{parent}/%(uploader_id)s/%(upload_date)s_%(title)s (%(id)s).%(ext)s"
    url = f"{DOM}/watch?v={nbr}"
    sub = "--ignore-errors"
    if nb:
        sub = "--ignore-errors --cookies-from-browser firefox"
    cmd = f'yt-dlp -f "{q}" "{url}" -o "{dp}" {sub}'
    os.system(cmd)


def fetch(user):
    cmd = f'yt-dlp "https://www.youtube.com/@{user}" --cookies-from-browser firefox --flat-playlist --dump-json > {user}.txt'
    os.system(cmd)
    with Path(f"{user}.txt").open("r") as fl:
        data = fl.read()
    return [json.loads(e.strip())["id"] for e in data.split("\n") if e.strip()]


# uns = [
#     f.stem.split(" ")[-1][1:-1]
#     for f in parent.rglob("*")
#     if f.suffix in [".mp4", ".mkv"]
# ]
# ps = fetch("NeringaKriziute")
# ps = [(e, 1) for e in ps if e not in uns]
# run_tasks(viding, ps)

for doc in parent.glob("@*"):
    new_doc = doc.with_name(doc.name[1:])
    new_doc.mkdir(parents=True, exist_ok=True)
    for f in doc.rglob("*"):
        f.rename(new_doc / f.name)

while True:
    nb = 0
    for doc in parent.rglob("*"):
        if doc.is_file():
            continue
        if len(list(doc.glob("*"))) > 0:
            continue
        doc.rmdir()
        print(doc.name)
        nb += 1
    if nb < 1:
        break
