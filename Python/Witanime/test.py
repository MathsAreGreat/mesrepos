import json
import re
from pathlib import Path
from urllib.parse import urljoin
from Mido.variables import print, download_m3u8_with_aria2c, aria_dwn, get_m3u8


infos = {}

names = {}


def no_found(t, arr):
    for e in arr:
        if e in t:
            return 0
    return 1


ds = ["Grand Blue"]

pr = Path("/home/mohamed/Documents/datas/Witanimes")
vr = Path("/home/mohamed/Documents/Files")
for f in pr.glob("*.json"):
    with f.open("r") as fl:
        dt = json.load(fl)
    t = dt["titre"]
    ep = re.findall(r"حلق", t)
    end = re.findall(r"خير", t)
    if no_found(t, ds):
        continue
    ts = [
        e.title() if re.findall(r"[a-z]", e) else e.zfill(2)
        for e in re.sub(r"[^a-z0-9]", r" ", t.lower()).split(" ")
        if e
    ]
    doc = "Movies"
    if ep:
        *ns, ep = ts
        tire = " ".join(ns)
        doc = f"Animes/{tire}"
        ts = [*ns, f"E{ep}"]
    if end:
        ts.append("END")
    name = ".".join(["[Witanime]", *ts])
    names[f.stem] = {"name": name, "doc": doc}
    infos[f.stem] = {}
    fmax = 0
    for c, v in dt["iframes"].items():
        key = v.split("/")[-1].split("=")[-1]
        fn = vr / f"{key}.json"
        if not fn.exists() or fn.stat().st_size < 10:
            continue
        with fn.open("r") as fl:
            vt = json.load(fl)
        sz = vt["tbr"]
        if sz > fmax:
            fmax = sz
            infos[f.stem]["dl"] = v
            infos[f.stem]["sz"] = sz


infos = {
    c: names[c] | v
    for c, v in infos.items()
    # if v and ("dailymotion.com" in v["dl"] or "ok.ru" in v["dl"])
}

links = sorted(infos.items(), key=lambda e: e[-1]["name"])

uns = [
    f.stem.split(".")[-1][1:-1]
    for f in Path("/home/mohamed/Downloads/Library").rglob("*.mp4")
]

for k, v in links:
    if k in uns:
        continue
    doc = f"/home/mohamed/Downloads/Library/{v["doc"]}"
    fname = f"{v["name"]}.({k}).mp4"
    uri = v["dl"]
    if "auvexiug." in uri:
        p = get_m3u8(uri)
        us = [e for e in re.findall(r"[^\"']+", p) if ".m3u8" in e]
        uri = urljoin(uri, max(us, key=len))
    print(uri)
    print("=" * 50)
    # download_m3u8_with_aria2c(uri, f"{doc}/{fname}")
