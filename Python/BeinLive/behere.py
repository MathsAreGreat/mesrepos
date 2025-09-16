from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import requests
import m3u8
import re
from concurrent.futures import ThreadPoolExecutor
import os
import json
from Crypto.Cipher import AES

sess = requests.session()
matches = {}


def monhtml(r):
    rs = sess.get(r)
    txt = rs.text
    return BeautifulSoup(txt, "html.parser")


def basic(k):
    u = f"https://aradsport.live/max.php?player=desktop&live={k}"
    match = re.search(r"return\((\[.+?\])", sess.get(u).text)
    if not match:
        return None
    url = "".join(json.loads(match[1]))
    sess.headers["Referer"] = u
    return url.replace("////", "//")


def basics(nb):
    u = f"https://asdfasfd.hlsjs.ru/lb/premium{nb}/playlist.m3u8"
    urls = sess.get(u, allow_redirects=True).url.split('/')
    urls[-1] = "tracks-v1a1/mono.m3u8"
    return "/".join(urls)


def prima(nb):
    sess = requests.Session()
    referrer = "https://olacast.live/"
    sess.headers = {
        "referer": referrer,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    u = f"https://webui.webtv1.lol/lb/prima{nb}/index.m3u8"
    urls = sess.get(u, allow_redirects=True).url.split('/')
    urls[-1] = "tracks-v1a1/mono.m3u8"
    return "/".join(urls)


def choose(nb):
    if not re.search(r"[a-z]", nb):
        r = f"https://weblivehdplay.ru/livetv.php?id=premium{nb}"
        sess.headers["Referer"] = r
        nb = int(nb)
        if nb > 0:
            return r, basics(nb)
        nb *= -1
        return r, prima(nb)
    r = "https://antenasport.ru"
    sess.headers["Referer"] = r
    u = basic(nb)
    return r, u


def dwn(v, ref, url, e, dd):
    cipher = None
    if dd:
        key, iv = dd
        cipher = AES.new(key, AES.MODE_CBC, iv)
    sess.headers = {
        "Referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    if e:
        item = "-".join(e.split("/"))
        doc = f"/home/mohamed/Videos/Ts/{v}"
        lefile = f"{doc}/{item}"
        if not os.path.exists(lefile):
            os.makedirs(doc, exist_ok=True)
            us = f"{url}/{e}"
            rz = sess.get(us, timeout=100)
            cx = rz.status_code
            if cx == 200:
                c = rz.content
                if cipher:
                    c = cipher.decrypt(c)
                print(">", item)
                with open(lefile, "wb") as f:
                    f.write(c)


def dwns(ref, url, e, dd):
    cipher = None
    if dd:
        key, iv = dd
        cipher = AES.new(key, AES.MODE_CBC, iv)
    sess.headers = {
        "Referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    if e:
        us = f"{url}/{e}"
        rz = sess.get(us, timeout=100)
        cx = rz.status_code
        if cx == 200:
            c = rz.content
            if cipher:
                c = cipher.decrypt(c)
            return c
        return None


def save(v, k):
    try:
        referer, base_url = choose(k[2:])
        base, _ = base_url.rsplit("/", 1)
        rs = sess.get(base_url, stream=1, timeout=100)
        mm = rs.text
        segments = m3u8.loads(mm).segments
        try:
            segment = segments[0]
            kk = segment.key.uri
            sess.headers = {
                "Referer": referer,
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            }
            resp = sess.get(kk, timeout=100)
            vv = segment.key.iv
            iv = int(vv, 16).to_bytes(16, "big")
            key = resp.content
            dd = (key, iv)
        except Exception as e:
            print("Segment :", e)
            dd = None
        return [
            (f"{v} [{k}]", referer, base, seg.uri, dd)
            for seg in segments
        ]
    except Exception:
        return []


def infos(k):
    u = f"http://www.livescore.cz/match/{k}"
    soup = monhtml(u)
    teams = soup.h3.text.replace("/", "")
    cs = soup.findAll("div", class_="detail")
    lives = [e for e in cs if e.findChildren("span", class_="live")]
    nos = [e.text for e in cs if not e.findChildren()]
    live = nos[0]
    if lives:
        live = lives[-1].text
    star = nos[-1]
    start_object = datetime.strptime(star, "%d.%m.%Y %H:%M")
    end_object = start_object + timedelta(hours=3)
    s_date = start_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    e_date = end_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    return teams, s_date, e_date, live


def upod(k):
    v, s, e, l = infos(k)
    nd = datetime.now()
    db = nd + timedelta(minutes=3)
    end = nd + timedelta(hours=3)
    nd = nd.strftime("%Y-%m-%d_%H:%M:%S")
    if nd < s:
        return k, 1
    if nd > e:
        return k, 0
    if k not in matches:
        matches[k] = {
            "t": v,
            "s": s,
            "h": "3000",
            "e": "3000",
            "l": l.split("-")[0].strip(),
        }
    op = 1
    matches[k]["v"] = l
    db = db.strftime("%Y-%m-%d_%H:%M") + ":00"
    if nd > matches[k]["e"]:
        return k, 0
    if "+" not in matches[k]["e"]:
        matches[k]["e"] = end.strftime("%Y-%m-%d_%H:%M") + ":00"
    if "half time" in l.lower():
        op = 0
        if nd > matches[k]["h"]:
            return k, 1
        if matches[k]["h"] == "3000":
            matches[k]["h"] = db
    if "finished" in l.lower():
        op = 0
        if matches[k]["e"] > db:
            matches[k]["e"] = db+"+"
    if op:
        matches[k]["l"] = l.split("-")[0].strip()
    return k, 2


cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear


def fetch_beout(pros):
    ks = [e for e in set(pros.values())]
    lesnbs = 1
    while lesnbs:
        sleep(.2)
        nd = datetime.now()
        nd = nd.strftime("%Y-%m-%d_%H:%M:%S")
        print(upclear*20, end="")
        with ThreadPoolExecutor(10) as executor:
            lesdatas = executor.map(upod, ks)
        datas = {k: nb for k, nb in lesdatas}
        ks = [e for e in ks if datas[e]]
        lesnbs = len(ks)
        keys = [
            (matches[e]["t"]+"/"+matches[e]["l"], v)
            for v, e in pros.items()
            if datas[e] == 2
        ]
        print(len(keys), "m3u8 items !")
        for e in ks:
            if datas[e] < 2:
                continue
            print(
                e, "|", matches[e]["t"], "-",
                matches[e]["l"], f"({matches[e]["v"]})"
            )
            print("End at :", matches[e]["e"])
        with ThreadPoolExecutor(1) as executor:
            lesdatas = executor.map(lambda args: save(*args), keys)
        mesfiles = [e for data in lesdatas for e in data]
        print(len(mesfiles), "files items !")
        with ThreadPoolExecutor(5) as executor:
            executor.map(lambda args: dwn(*args), mesfiles)
