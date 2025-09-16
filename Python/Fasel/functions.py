import json
import re
import webbrowser
from pathlib import Path
from time import sleep

import m3u8
from Mido.variables import download_m3u8_with_aria2c, upclear

from mesvariables import DOM, lib_path

# "spis16t3 bot 1.0"

cols = ["#00ff00", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def gop(k):
    fn = Path(f"/home/mohamed/Documents/datas/Fasel/Datas/{k}.json")
    tn = Path(f"temps/{k}")
    url = f"https://{DOM}/video_player?vid={k}"
    if not fn.exists():
        if tn.exists():
            return None
        tn.touch()
        webbrowser.get("firefox").open(url)
        return None
    with fn.open("r") as ef:
        data = json.load(ef)
    print(fn)
    return data


def show(f, uns):
    k = f.stem
    if k in uns:
        return None
    return f


def data_update(nbr=0):
    file_doc = Path("/home/mohamed/Documents/datas/Fasel")
    uns_doc = Path("/home/mohamed/Downloads")
    if nbr == 0:
        files = list(file_doc.glob("Seasons/*.json"))
        while files:
            nbr = 0
            for f in files[:5]:
                with f.open("r") as e:
                    data = json.load(e)
                u = data["eps"][0]
                webbrowser.get("firefox").open(u)
                nbr += 1
                sleep(1)
            while list(uns_doc.glob("*.json")):
                sleep(2)
            files = files[5:]
    infos = {}
    for f in uns_doc.rglob("*.mp4"):
        c = f.stem.split(".")[-1][1:-1]
        Path(f"Backups/{c}").touch()
    for f in lib_path.rglob("*.mp4"):
        c = f.stem.split(".")[-1][1:-1]
        Path(f"Backups/{c}").touch()
    uns = [f.stem for f in file_doc.glob("Seasons/*.json")]
    uns += [f.name for f in Path("Backups").rglob("*")]
    nb = 1
    scrs = []
    if nb:
        files = sorted(file_doc.glob("Episodes/*.json"), key=lambda f: int(f.stem))
        sites = []
        for f in files:
            with f.open("r") as fh:
                data = json.load(fh)
            sites.append(data["u"])
        nb = 0
        seps = []
        for f in file_doc.glob("Seasons/*.json"):
            with f.open("r") as e:
                data = json.load(e)
            for u in data["eps"]:
                if u not in sites:
                    seps.append(u)

        for u in seps[:5]:
            if u not in scrs:
                webbrowser.get("firefox").open(u)
                scrs.append(u)
            nb += 1
        while list(uns_doc.glob("*.json")):
            sleep(2)
    files += sorted(file_doc.glob("Movies/*.json"), key=lambda f: int(f.stem))
    files = [show(f, uns) for f in files]
    files = [f for f in files if f]
    for f in file_doc.glob("Datas/*.json"):
        tn = Path(f"temps/{f.stem}")
        if tn.exists():
            tn.unlink()
    if not files:
        return 0
    for f in files:
        k = f.stem
        with f.open("r") as e:
            data = json.load(e)
        doc = f.parent.name
        t = data.get("t")
        gr = data.get("gr")
        if doc == "Episodes":
            ep = data["ep"]
            sn = data["sn"]
            if sn not in infos:
                v = file_doc / f"Seasons/{sn}.json"
                with v.open("r") as e:
                    dt = json.load(e)
                t = f"{dt['t']}.S{dt['ss']}.E{ep}"
                gr = dt["gr"]
        dl = data.get("dl")
        videos = gop(dl)
        if not videos:
            break
        key = max(videos, key=lambda v: int(re.sub(r"[^0-9]", r"", v)))
        url = videos[key]
        f = f"[FaselHD].{t}.[{key}].({k}).mp4"
        doc = lib_path / gr
        final_file = doc / f
        download_m3u8_with_aria2c(url, final_file, "https://www.faselhds.care/")

    for f in lib_path.rglob("*.mp4"):
        *parts, ds, fn = f.parts[1:]
        if ds != "Movies":
            serie, ss, *_ = fn.rsplit(".", 5)
            ds = ds.replace("Episodes", "Seasons")
            sr = " ".join(e for e in serie.split(".") if "[" not in e)
            ds = f"{ds}/{sr}/{ss}"
        doc = Path("/home/mohamed/Downloads/Library", *parts, ds)
        doc.mkdir(parents=True, exist_ok=True)
        f.rename(doc / fn)
    c = 1
    while c > 0:
        c = 0
        for current in lib_path.rglob("*"):
            if not current.is_dir():
                continue
            items = list(current.glob("*"))
            if len(items) > 0:
                continue
            current.rmdir()
            c += 1
    print(f"{upclear}Waiting for : {nbr}")
    return nbr
