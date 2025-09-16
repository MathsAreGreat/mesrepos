from pathlib import Path
import pickle
import os
import re
from mutagen.id3 import ID3
from mutagen.id3._frames import TPE1, TCON, COMM


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


def remove_empties(*paths):
    for p in paths:
        c = 1
        z = "download_list.log"
        while c > 0:
            c = 0
            for current, dirs, files in os.walk(p):
                current = re.sub(r"\\", r"/", current)
                if len(dirs) + len(files) == 0:
                    c += 1
                    print(current, "is an empty folder !")
                    os.rmdir(current)
                elif z in files:
                    os.remove(os.path.join(current, z))
                    c += 1


infos, names = mesdatas()

# with open("infos.json", "w") as fl:
#     json.dump(infos, fl)

# with open("names.json", "w") as fl:
#     json.dump(names, fl)

# /home/mohamed/Music/Spotify/Finals/Premp3

parent = Path("/home/mohamed/Music/Spotify/Finals")
musique = Path("/home/mohamed/Music")

for f in parent.rglob("*.mp3"):
    k = f.parts[-3]
    info = infos[k]
    ar = names[info["artist"][0]]
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
    doc = musique / f"Songs/{gr}/{ar}"
    doc.mkdir(parents=True, exist_ok=True)
    to = doc / fn
    f.rename(to)

remove_empties("/home/mohamed/Music")
