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
sess.headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}

try:
    with open("status.json", "r") as el:
        status = json.load(el)
except:
    status = {}


def choose(nb):
    r = "https://viwlivehdplay.ru/"
    sess.headers["Referer"] = r
    if not re.search(r"[a-z]", nb):
        nb = int(nb)
        return r, basics(nb)
    if re.search(r"^-", nb):
        return r, prima(nb[1:])
    r = "https://antenasport.ru"
    sess.headers["Referer"] = r
    u = basic(nb)
    return r, u


def basic(k):
    u = f"https://aradsport.live/max.php?player=desktop&live={k}"
    match = re.search(r"return\((\[.+?\])", sess.get(u).text)
    if not match:
        return None
    url = "".join(json.loads(match[1]))
    sess.headers["Referer"] = u
    return url.replace("////", "//")


def basics(nb):
    u = f"https://salamus2023.onlinehdhls.ru/lb/premium{nb}/playlist.m3u8"
    urls = sess.get(u, allow_redirects=True).url.split('/')
    urls[-1] = "tracks-v1a1/mono.m3u8"
    return "/".join(urls)


def prima(nb):
    u = f"https://salamus2023.onlinehdhls.ru/lb/prima{nb}/index.m3u8"
    urls = sess.get(u, allow_redirects=True).url.split('/')
    urls[-1] = "tracks-v1a1/mono.m3u8"
    return "/".join(urls)


def dwn(v, ref, url, e, dd):
    item = "-".join(e.split("/"))
    doc = f"/home/mohamed/Videos/Ts/{v}"
    lefile = f"{doc}/{item}"
    if os.path.exists(lefile):
        return 0
    cipher = None
    if dd:
        key, iv = dd
        cipher = AES.new(key, AES.MODE_CBC, iv)
    sess.headers = {
        "Referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    os.makedirs(doc, exist_ok=True)
    us = f"{url}/{e}"
    rz = sess.get(us, timeout=5)
    cx = rz.status_code
    if cx == 200:
        c = rz.content
        if cipher:
            c = cipher.decrypt(c)
        print(">", item)
        with open(lefile, "wb") as f:
            f.write(c)
    return 1


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
        rz = sess.get(us, timeout=5, stream=True)
        cx = rz.status_code
        if cx == 200:
            c = rz.content
            if cipher:
                c = cipher.decrypt(c)
            return c
        return None


def saves(a, ks):
    t, s, l = infos(a)
    end_object = datetime.now()
    db = end_object.strftime("%Y-%m-%d_%H:%M:%S")
    if s > db:
        print(">", s)
        print(">", db)
        print("Mazal", a, "!")
        return [0]
    end_object = datetime.now() + timedelta(minutes=5)
    end_str = end_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    if a not in status:
        status[a] = {
            "s": s,
            "h": None,
            "e": None,
            "l": l
        }
    status["n"] = db
    if "half time" in l.lower():
        if not status[a]["h"]:
            status[a]["h"] = end_str
        if status[a]["h"] < db:
            print(">", a, "Half Time !")
            status[a]["l"] = l
            return [0]
    elif "finished" in l.lower():
        if not status[a]["e"]:
            status[a]["e"] = end_str
        if status[a]["e"] < db:
            print(">", a, "Finished !")
            status[a]["l"] = l
            return []
    else:
        status[a]["l"] = l

    l = status[a]["l"].split("-")[0].strip()

    ds = []
    for k in ks:
        v = f"{t} [{k}][{l}]"
        try:
            referer, base_url = choose(k)
            base, _ = base_url.rsplit("/", 1)
            rs = sess.get(base_url, stream=True, timeout=5)
            mm = rs.text
            segments = m3u8.loads(mm).segments
            try:
                segment = segments[0]
                k = segment.key.uri
                resp = sess.get(k)
                vv = segment.key.iv
                iv = int(vv, 16).to_bytes(16, "big")
                key = resp.content
                dd = (key, iv)
            except Exception as e:
                print("Segment :", e)
                dd = None
            ds += [
                (v, referer, base, seg.uri, dd)
                for seg in segments
            ]
        except Exception as e:
            print("choose :", e)
            ds.append(None)
    return ds


cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear


doc = "/home/mohamed/Videos/Ts"
os.makedirs(doc, exist_ok=True)

lesdatas = []


def monhtml(r):
    rs = sess.get(r)
    txt = rs.text
    return BeautifulSoup(txt, "html.parser")


def infos(k):
    u = f"http://www.livescore.cz/match/{k}"
    soup = monhtml(u)
    teams = soup.h3.text
    cs = soup.findAll("div", class_="detail")
    lives = [e for e in cs if e.findChildren("span", class_="live")]
    nos = [e.text for e in cs if not e.findChildren()]
    live = nos[0]
    if lives:
        live = lives[-1].text
    star = nos[-1]
    start_object = datetime.strptime(
        star, "%d.%m.%Y %H:%M") - timedelta(hours=1)
    # end_object = start_object + timedelta(hours=3)
    s_date = start_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    # e_date = end_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    return teams, s_date, live


def save(k):
    try:
        referer, base_url = choose(k)
        base, _ = base_url.rsplit("/", 1)
        rs = sess.get(base_url, stream=True)
        mm = rs.text
        segments = m3u8.loads(mm).segments
        try:
            segment = segments[0]
            k = segment.key.uri
            resp = sess.get(k)
            vv = segment.key.iv
            iv = int(vv, 16).to_bytes(16, "big")
            key = resp.content
            dd = (key, iv)
        except Exception as e:
            print("Segment :", e)
            dd = None
        return [
            (referer, base, seg.uri, dd)
            for seg in segments
        ]
    except Exception as e:
        print("choose :", e)
        return []


def sauver(v):
    lefile = f"{doc}/Live-{v}.ts"
    garbage = []
    with open(lefile, "wb") as f:
        while True:
            datas = save(v)
            print()
            print(f"{upclear*12}::", len(datas), "items !")
            print()
            for ref, base, uri, dd in datas:
                if uri in garbage:
                    continue
                cs = None
                nb = 3
                while not cs:
                    try:
                        cs = dwns(ref, base, uri, dd)
                    except:
                        pass

                print(f"{upclear}>", uri, ":", len(cs), " "*10)
                garbage.append(uri)
                f.write(cs)
            sleep(.3)


# ks = ["do22"]
# for k in ks:
#     lesdatas = save(k)
#     print(lesdatas)
#     # with ThreadPoolExecutor(10) as executor:
#     #     executor.map(lambda args: dwn(*args), lesdatas)
#     for args in lesdatas:
#         dwn(f"CH{k}", *args)

# with ThreadPoolExecutor() as executor:
#     executor.map(
#         sauver,
#         ks
#     )

temps = datetime.now().strftime("%H:%M:%S")
while temps < "21:50":
    try:
        with open("infos.json", "r") as el:
            ks = json.load(el)
    except:
        ks = {}
    os.system("clear")
    print("Reolads at", temps)
    ks = {
        k: v
        for k, v in ks.items()
        if k not in status
        or status[k]["l"] != "Finished"
    }
    with ThreadPoolExecutor(10) as executor:
        datas = executor.map(lambda args: saves(*args), ks.items())
    lesdatas = [e for data in datas for e in data]
    if not lesdatas:
        break
    lesdatas = [e for e in lesdatas if e]
    print(len(lesdatas))
    with ThreadPoolExecutor(5) as executor:
        executor.map(lambda args: dwn(*args), lesdatas)
    sleep(1)
    temps = datetime.now().strftime("%H:%M:%S")
    with open("status.json", "w") as fl:
        json.dump(status, fl, indent=2)
