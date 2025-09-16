import pickle
import json
from pathlib import Path

from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, COMM, TALB, TCON, TIT2, TPE1, TPE2, USLT


Lyrics = Path("/home/mohamed/Documents/Lyrics/Deemix_utf")
parent = Path("/home/mohamed/Documents/datas/Deemix")
to = Path("/home/mohamed/Documents/Projects/Backups")
doc = to / "Lyrics"
doc.mkdir(parents=True, exist_ok=True)
for fn in Lyrics.glob("*.lrc"):
    f = parent / f"{fn.stem}.dmx"
    if not f.exists():
        continue
    with f.open("rb") as fl:
        audio = pickle.load(fl)
    with fn.open("r") as fl:
        lrcs = [e.strip() for e in fl.readlines() if e.strip()][::-1]

    if not lrcs[-1].startswith("[00:00.00]"):
        lrcs.append("[00:00.00]")
    tt = f"{audio.getall("TIT2")[0].text[0]}".rsplit(" ", 1)[0]
    lrcs += [
        f"[Title: {tt}]",
        f"[Genre: {audio.getall("TCON")[0].text[0]}]",
        f"[Artist: {audio.getall("TPE1")[0].text[0]}]",
        f"[ID: {fn.stem}]",
    ]
    data = "\n".join(lrcs[::-1])
    to_path = doc / f"{fn.stem}.lrc"
    with to_path.open("w") as fl:
        fl.write(data)

parent = Path("/home/mohamed/Documents/datas/Docker")
doc = to / "Docker"
doc.mkdir(parents=True, exist_ok=True)
files = sorted(parent.glob("*.json"))
for fn in files:
    with fn.open("r") as fl:
        data = json.load(fl)
    name = fn.stem.split("_")[0]
    to_path = doc / f"{name}.json"
    with to_path.open("w") as fl:
        json.dump(data, fl)
