import json
import os
import re
from pathlib import Path

import requests
from Mido.variables import monhtml


def export_key(k):
    soup = monhtml(f"https://antenaplanet.store/{k}.php")
    src = soup.iframe.get("src").split("?")[-1].split("=")[-1]
    return re.sub(r"^cn", r"", src)


def fetch():
    monfl = Path("/home/mohamed/Documents/datas/Databases/antanas.json")
    try:
        with monfl.open("r") as fr:
            mesinfos = fr.load()
    except:
        mesinfos = {}

    u = "https://antenaplanet.store/index2.txt"
    r = requests.get(u)
    line = next(e.strip() for e in r.text.split("=") if e.strip() and "http" in e)
    areas = [e.strip() for e in re.split(r"-+", line) if e.strip()]
    key = ""
    for area in areas:
        lines = [e.strip() for e in area.split("\n") if e.strip()]
        datas = [
            line.split("/")[-1].rsplit(".", 1)[0] for line in lines if "http" in line
        ]
        infos = [line for line in lines if "http" not in line]

        if "une 2025" in infos[0]:
            key = re.sub(r"[^0-9a-z]+", r"-", infos[0].lower())
            infos = infos[1:]

        if key not in mesinfos:
            mesinfos[key] = []

        for info in infos:
            dd = [info, datas]
            if dd in mesinfos[key]:
                continue
            mesinfos[key].append(dd)
    for k, v in mesinfos.items():
        v = sorted(v, key=lambda e: e[0][0])
        mesinfos[k] = v
    with monfl.open("w") as fr:
        json.dump(mesinfos, fr)


k = os.sys.argv[-1]

# print(export_key(k))

sess = requests.Session()

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


# k = "suspilnetv"
r = f"https://antenaplanet.store/{k}.php"

bol = None

while not bol:
    soup = monhtml(r)
    src = soup.iframe.get("src")
    sess.headers = {"referer": r, "User-Agent": agent}
    rs = sess.get(src)
    bol = re.findall(r"var channelKey[^;]+", rs.text)
    r = src

bol = re.findall(r'[^"]+', bol[0].strip())
print(bol[-1])
