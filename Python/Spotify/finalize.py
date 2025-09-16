from pathlib import Path
import pickle
import os
import re
from mutagen.id3 import ID3
from mutagen.id3._frames import TPE1, TCON, COMM
from gadhom import remove_empties


def mesdatas(n="", r=""):
    p = "/home/mohamed/Documents/datas/Spotify"
    infos = {}
    names = {}
    for f in os.listdir(p):
        if f.endswith("plsptf"):
            continue
        if not f.endswith("sptf"):
            continue
        fn = os.path.join(p, f)
        with open(fn, "rb") as e:
            datas = pickle.load(e)
        if f.endswith(".albsptf"):
            for k, v in datas.items():
                if k not in infos:
                    if (
                        n.lower() in v["title"].lower()
                        and r.lower() in v["album"].lower()
                    ):
                        infos[k] = v
        elif f.endswith(".arsptf"):
            k = f.rsplit(".", 1)[0]
            names[k] = datas["name"]
    return infos, names


infos, names = mesdatas()

# ====================================================


parent = Path("/home/mohamed/Music/Spotify/Finals")
musique = Path("/home/mohamed/Music")

for f in parent.rglob("*.mp3"):
    k = f.parts[-3]
    if info := infos.get(k):
        ar = names[info["artist"][0]]
    else:
        ar = f.stem.split("-")[0].split(",")[0]
    doc = musique / f"tmp/Arabic/{ar}"
    doc.mkdir(parents=True, exist_ok=True)
    to = doc / f"{k}.mp3"
    f.rename(to)


for f in musique.glob("tmp/*/*/*.mp3"):
    gr, ar, fn = f.parts[-3:]
    k = fn.rsplit(".", 1)[0]
    audio = ID3(f)
    audio["COMM"] = COMM(encoding=3, text=k)
    audio["TPE1"] = TPE1(encoding=3, text=ar)
    audio["TCON"] = TCON(encoding=3, text=gr)
    audio.save()
    doc = musique / f"tmp/{gr}/{ar}"
    doc.mkdir(parents=True, exist_ok=True)
    to = doc / fn
    f.rename(to)

remove_empties("/home/mohamed/Music")
