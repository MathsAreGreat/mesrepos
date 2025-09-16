from datetime import datetime
import os
import json
import m3u8
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import outils

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

refs = {
    "sn": "https://arryadia.snrt.ma/",
    "sh": "https://sba.net.ae/",
    "AD": "https://player.mangomolo.com",
    "KS": "https://www.alkass.net/",
}
sess = requests.session()


def dwn(dd):
    if dd:
        try:
            url, doc, e = dd
            cx = 1
            lefile = e.replace("/", "-")
            fn = f"{doc}/{lefile}"
            if not os.path.exists(fn):
                us = url.rsplit("/", 1)[0] + "/" + e
                rz = sess.get(us, stream=True, timeout=100)
                cx = rz.status_code
                if cx == 200:
                    print(">", lefile, end="\r")
                    with open(fn, "wb") as f:
                        c = rz.content
                        f.write(c)
        except Exception as err:
            print(err)


def choose(key):
    fn = f"{key}.json"
    with open(fn, "r", encoding="utf-8") as f:
        info = json.load(f)
    uris = info["segs"]
    fr = info["seg"]
    url = f"{fr}/{uris[0]}"
    ref = refs.get(key[:2])
    return ref, url


def filedwn(k, sub):
    doc = f"/home/mohamed/Videos/Koora/Matches/{sub}"
    os.makedirs(doc, exist_ok=True)
    dd = outils.jdid(k)
    if not dd:
        return []
    r, u = dd
    sess.headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Referer": r,
    }
    rs = sess.get(u, stream=True)
    mm = rs.text
    try:
        return [(u, doc, seg["uri"]) for seg in m3u8.loads(mm).data["segments"]]
    except:
        print("No", k, "url !")
        return [""]


def generate(k, key):
    nw = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    dd = outils.infos(k)
    if not dd:
        return []
    t, start, half, end, lv = dd
    tt = f"** {t:22}"
    if nw < start:
        msg = f"{tt} : {start} ! "
        print(f"{msg:60}")
        return []
    if end and nw > end:
        msg = f"{tt} : Stream Ended ! "
        print(f"{msg:60}")
        with open(f"Finished/{k}", "w") as fl:
            fl.write("")
        return []
    if half and nw > half:
        msg = f"{tt} : Half time ! "
        print(f"{msg:60}")
        return []
    v = lv.split("-")[0].strip()
    l = f"{t}/{v}"
    msg = "> Starting ! "
    print(f"{msg:60}")
    return filedwn(key, l)


NB = 55

while NB > 2:
    beg = time.time()

    with open("datas.json", "r") as fl:
        urls = json.load(fl)
    if urls:
        datas = [
            (k, v)
            for k, v in urls.items()
            if ")" not in k and not os.path.exists(f"Finished/{k}")
        ]
        with open("datas.json", "w") as fl:
            json.dump({k: v for k, v in datas}, fl)

        mesliens = []
        for c, k in datas:
            try:
                mesliens += generate(c, k)
            except:
                print(f"> Error : {NB}")

        print(">>>", len(mesliens), "items !")
        if mesliens:
            with ThreadPoolExecutor(10) as executor:
                executor.map(dwn, mesliens)
    NB -= int(time.time() - beg) + 1
    time.sleep(1)

os.remove("/home/mohamed/Documents/Stuff/monlogfile.log")
