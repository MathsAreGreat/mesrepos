import os
import re
import gadhom

uniques = {f: "Backups" for f in os.listdir("/home/mohamed/Documents/datas/Backups")}
dpath = "/home/mohamed/Music/Spotify/Finals/Indefined"
os.makedirs(dpath, exist_ok=True)
dpath = "/home/mohamed/Music/MesSongs"
os.makedirs(dpath, exist_ok=True)
os.chdir(dpath)
infos_dossier = {}
# uniques = {}

for doc in os.listdir():
    for c, _, files in os.walk(doc):
        cs = c.split("/")
        d = cs[-1]
        if files:
            g, r, *_ = cs[-3:]
            infos_dossier[r] = g

dpath = "/home/mohamed/Music"
os.chdir(dpath)

for doc in os.listdir():
    for c, _, files in os.walk(doc):
        cs = c.rsplit("/", 1)
        d = cs[-1]
        unique = {
            f.split("(")[-1].split(")")[0].rsplit(".", 1)[0]: d
            for f in files
            if f.endswith(".mp3")
        }
        unique[d] = d
        unique = {k: v for k, v in unique.items() if k not in uniques}
        uniques.update(unique)

dpath = "/home/mohamed/Music/Spotify/Finals"
os.chdir(dpath)

ARTSs, IDs, urls = [], [], []
PID = ["2BPrppGi0FYYRihrkIVsS2"]
for ID in PID:
    ar, ids, us = gadhom.playlists(ID)
    ARTSs += ar
    IDs += ids
    urls += us

gadhom.artists(ARTSs)
IDs = [e for e in set(IDs)]
gadhom.albums(IDs)
ids = [e for e in set(urls) if e not in uniques]
gadhom.dwnld(ids)
gadhom.restore(dpath, infos_dossier)
gadhom.remove_empties("/home/mohamed/Music/Spotify")

uniques = {}
for c, _, files in os.walk("/home/mohamed/Music"):
    unique = {
        f.split("(")[-1].split(")")[0]: c
        for f in files
        if "(" in f and f.endswith(".mp3")
    }
    unique = {k: v for k, v in unique.items() if k not in uniques}
    uniques.update(unique)

for k in uniques:
    fn = os.path.join("/home/mohamed/Documents/datas/Backups", k)
    with open(fn, "w") as e:
        e.write("")
