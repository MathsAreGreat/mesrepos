import json
from concurrent.futures import ThreadPoolExecutor
import os

from Besites.animerco import ercoing
from Besites.animeup import uping
from Besites.mp4upload import MP4
from Besites.okanime import oking
from Besites.okru import check_for_datas as ok_check, oksize
from Besites.daily import check_for_datas as dm_check, dmsize
from Besites.witanime import witing
from Besites.videa import contenu, check_for_datas

os.makedirs("Backups", exist_ok=True)

try:
    with open("segs.json", "r") as e:
        segs = json.load(e)
    segs = {
        k: {
            c: v
            for c, v in segs[k].items()
            if v["size"] >= 0
        }
        for k in segs
    }
except:
    segs = {}


def run_tasks(fn, ds, nb=20):
    def your_function(args): return fn(*args)
    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


def finalize(k, code, t):
    if "-" in k:
        return None
    if k in segs[code]:
        return None

    if t == "ok":
        vv = ok_check(k)
        s = -1
        if "http" in str(vv):
            s = oksize(k)
        return code, k, {"site": "okru", "size": s}

    if t == "dm":
        vv = dm_check(k)
        s = -1
        if "http" in str(vv):
            s = dmsize(k)
        return code, k, {"site": "dailymotion", "size": s}

    if t == "vd":
        vv = check_for_datas(k)
        s = -1
        if "http" in str(vv):
            s = contenu(k)
        return code, k, {"site": "videa", "size": s}

    if t == "mp":
        lien = MP4(k).save()
        return code, k, {"site": "mp4upload", "size": lien.size}


def collected(*arrs):
    mesdatas = []
    uns = []
    for arr in arrs:
        for code, info in arr.items():
            if code not in segs:
                segs[code] = {}
            for key, vals in info["links"].items():
                for v in vals:
                    if v not in uns and ".html" not in v:
                        uns.append(v)
                        mesdatas.append((v, code, key[:-1]))
    return mesdatas


def retreive(anime4up, animerco=None, okanime=None, witanime=None):
    animercos = {}
    okanimes = {}
    witanimes = {}
    name, animeup = uping(anime4up)
    if okanime:
        okanimes = oking(okanime, name)
    if animerco:
        animercos = ercoing(animerco, name)
    if witanime:
        witanimes = witing(witanime, name)

    mesdatas = collected(animeup, okanimes, animercos, witanimes)
    while mesdatas:
        datas = run_tasks(finalize, mesdatas[:5])
        mesdatas = mesdatas[5:]
        for dd in datas:
            if not dd:
                continue
            code, k, info = dd
            if code not in segs:
                segs[code] = {}
            segs[code][k] = info
            with open("segs.json", "w") as e:
                json.dump(segs, e)


with open("infos.json", "r") as e:
    animes = json.load(e)

for anime in animes:
    retreive(**anime)
