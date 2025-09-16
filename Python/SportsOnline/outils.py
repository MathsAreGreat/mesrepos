import re
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
sess = requests.session()


def concatize(*fs, o="output", ex="ts"):
    files = [f"{f}.{ex}" for f in fs]
    filenames = "|".join(files[:])
    cmd = f'ffmpeg -i "concat:{filenames}" -c copy "{o}.{ex}"'
    os.system(cmd)
    msg = f"* {o}.{ex} Created !"
    print(f"{msg:<40}", end="\r")


def sort_fnc(s):
    return sum(int(e) for e in re.findall(r"[0-9]+", s))


def combine_vids(p, d):
    if not os.path.exists(p):
        return 0
    os.chdir(p)
    for v_out in os.listdir():
        if not v_out.endswith('.ts'):
            doc = f"/home/mohamed/Documents/Projects/Python/PrimaSport/{d}"
            os.makedirs(doc, exist_ok=True)
            out = f"{doc}/{v_out}"
            fs = [
                f"{v_out}/{f[:-3]}" for f in os.listdir(v_out) if f.endswith('.ts')]
            fs = sorted(fs, key=sort_fnc)
            if len(fs) < 100:
                concatize(*fs, o=out)
            else:
                i = 0
                while fs:
                    i += 1
                    concatize(*fs[:100], o=f"{out}_{i}")
                    fs = fs[100:]
                fs = [f"{out}_{n+1}" for n in range(i)]
                concatize(*fs, o=out)
                for f in fs:
                    os.remove(f"{f}.ts")
                    msg = f"** Removing {f}.ts"
                    print(f"{msg:<40}", end="\r")
    #                 rmtree(v_out)

    msg = "> All is Done !"
    print(f"{msg:<40}")
    return 1


def monhtml(u, r):
    sess.headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Referer": r
    }
    rs = sess.get(u)
    txt = rs.text
    return BeautifulSoup(txt, "html.parser")


def jdid(u):
    ref = "/".join(u.split("/")[:3])
    soup = monhtml(u, ref)
    iframe = soup.iframe
    while iframe:
        ref = "/".join(u.split("/")[:3])
        u = iframe["src"]
        soup = monhtml(u, ref)
        iframe = soup.iframe
    sess.headers = {
        'User-Agent': agent,
        'Referer': ref
    }

    ref = "/".join(u.split("/")[:3])
    r = sess.get(u)
    us = re.findall(r'[^\'"]+m3u8[^\'"]*', r.text)
    us = us[0].split("|")
    nb = us[us.index("https")+1]
    if re.search(r"[^0-9]", nb):
        return None
    m3u = us[us.index("hls")+1]
    ind = us.index("m3u8")
    s, e = us[ind+1:ind+3]
    ld = us.index("btn")
    ht = us[ld-1]
    return ref, f"https://{ht}.cdnministry.net:{nb}/hls/{m3u}.m3u8?s={s}&e={e}"


def infos(k):
    u = f"http://www.livescore.cz/match/{k}"
    soup = monhtml(u, u)
    fn = f"files/{k}.json"
    try:
        with open(fn, "r") as e:
            infos = json.load(e)
    except:
        infos = {}
    teams = soup.h3.text
    cs = soup.findAll("div", class_="detail")
    lives = [e for e in cs if e.findChildren("span", class_="live")]
    nos = [e.text for e in cs if not e.findChildren()]
    live = nos[0]
    if lives:
        live = lives[-1].text.strip()
    star = nos[-1]
    s_object = datetime.strptime(star, "%d.%m.%Y %H:%M") - timedelta(hours=1)
    n_object = datetime.now()
    h_object = n_object + timedelta(minutes=3)
    s_date = s_object.strftime("%Y-%m-%d-%H-%M") + "-00"
    h_date = ""
    if not infos:
        infos["s"] = s_date
        infos["t"] = teams
        infos["h"] = h_date
        infos["e"] = h_date
        infos["l"] = live
    else:
        last = infos["l"].split("=>")[0].strip()
        if "-" not in live and last != live:
            infos["l"] = f"{last} => {live}"
        if "finish" in live.lower():
            if infos["e"] == "":
                e_date = h_object.strftime("%Y-%m-%d-%H-%M") + "-00"
                infos["e"] = e_date
        elif "half time" in live.lower():
            if infos["h"] == "":
                h_date = h_object.strftime("%Y-%m-%d-%H-%M") + "-00"
                infos["h"] = h_date
        else:
            infos["l"] = live

    with open(fn, "w") as e:
        json.dump(infos, e, indent=2)
    return infos["t"], infos["s"], infos["h"], infos["e"], infos["l"]
