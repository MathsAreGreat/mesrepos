import re
from concurrent.futures import ThreadPoolExecutor
import json
import os

d_path = "Videos/%(id)s.%(ext)s"
s_path = "Videos/Files/%(title)s/%(upload_date)s_%(section_title)s (%(id)s).%(ext)s"

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

DOM = "https://www.youtube.com"

try:
    with open("Datas/playlists.json", "r") as e:
        lds = json.load(e)
except:
    lds = {}

cs = {}

users = {
    "AJplussaha": "AJplus Saha",
    "TheYahyaAzzam": "Yaya Azzam",
    "MicsPodcast": "Mics Podcasts",
    "anaalaraby": "Mohamed Saadani",
    "9li9": "عبدالرحمن مسعد",
    "abdulrahmanmosad9736": "عبدالرحمن مسعد",
    "NewMedia_Life": "الدحيح",
    "m3kamele7trami": "Mohamed Abd Elati",
    "tasgeelpodcast": "Tasgeel Podcast",
    "EslamAdel": "Eslam Adel",
    "FahmyProductions": "Fahmy Productions",
    "user-yj5vt8ki7u": "طحالب",
    "Tahalip": "طحالب",
    "janazeermedia2": "طحالب",
    "Filmolokhia": "Mohamed Goely",
}

reverses = {
    "الدحيح": "New Media Academy Life",
}

keys = [
    "title",
    "channel_id",
    "duration",
    "subtitles",
    "chapters",
    "uploader",
    "uploader_id",
    "upload_date",
]


def thumbnaudio(nbr):
    q = "bestaudio[ext=m4a]/bestaudio"
    dp = "Audios/%(id)s.%(ext)s"
    url = nbr
    if not nbr.startswith("PL"):
        url = f"{DOM}/watch?v={nbr}"
    sub = "--write-sub --sub-langs all,-live_chat --ignore-errors"
    cmd = f'yt-dlp -f "{q}" "{url}" -o "{dp}" {sub}'
    os.system(cmd)
    print(upclear*10, end="")


def subtitre(nbr):
    dp = "Audios/%(id)s.%(ext)s"
    url = f"{DOM}/watch?v={nbr}"
    sub = "--write-sub --sub-langs all,-live_chat --ignore-errors"
    cmd = f'yt-dlp --skip-download "{url}" -o "{dp}" {sub}'
    os.system(cmd)
    print(upclear*10, end="")


def gad(l):
    data = json.loads(l)
    if data["title"] == "[Private video]":
        return None
    keys = {"id", "playlist_id", "playlist_title"}
    info = {k: v for k, v in data.items() if k in keys}
    for c, v in cs.items():
        if c.lower() in data["title"].lower().replace("_", " "):
            info["playlist_title"] = v
            break
    id = info["playlist_id"]
    if "pls" not in lds:
        lds["pls"] = {}
    if "ids" not in lds:
        lds["ids"] = {}
    if id.startswith("PL"):
        lds["pls"][id] = info["playlist_title"]
        lds["ids"][info["id"]] = id
    return info


def save(l):
    data = gad(l)
    if not data:
        return 0
    c = data["id"]
    json_file = f"Files/{c}.json"
    if os.path.exists(json_file):
        return 0
    dd = (f"=={c}", 1, "")
    datas = channelize(dd)
    if not datas:
        return 0
    infos = {k: datas[k] for k in keys if k in datas}
    infos.update(data)
    tb = infos["subtitles"]
    if tb:
        k = "live_chat"
        if k in tb:
            del tb[k]
        for key, val in tb.items():
            tb[key] = val[-1]["url"]
        infos["subtitles"] = tb
    k = "id"
    if k in infos:
        del infos[k]

    with open(json_file, "w") as e:
        json.dump(infos, e, indent=2)
    return 1


def channelize(dd):
    c, mx, *fs = dd
    if mx < 0:
        return 0
    json_file = f"Files/{c}.json"
    if os.path.exists(json_file):
        return {}
    r = "rjwwx"
    if not fs:
        f = ""
    elif len(fs) < 2:
        f = fs[0]
        if f.startswith("+="):
            f = ""
            r = fs[0][2:]
    else:
        f = "|".join(f"({e})" for e in fs if not e.startswith("+="))
        r = "|".join(f"({e[2:]})" for e in fs if e.startswith("+="))
    cnt = 1
    txt_file = f"Files/{c}.txt"
    if not os.path.exists(txt_file):
        dd = f"{DOM}/@{c}/videos"
        if c.startswith("UC"):
            dd = f"{DOM}/channel/{c}/videos"
        elif c.startswith("PL"):
            dd = f"{DOM}/playlist?list={c}"
        elif c.startswith("=="):
            c = c[2:]
            dd = f"{DOM}/watch?v={c}"
            cnt = 0
        print("Loading", c, "!")
        cmd = f'yt-dlp "{dd}" --flat-playlist --dump-json'
        if mx:
            cmd += f' --playlist-end "{mx}" '
        cmd += f' --match-title "{f}"'
        cmd += f' --reject-title "{r}"'
        cmd += f" > {txt_file}"
        os.system(cmd)
        print("Loaded", c, "!")
    if cnt:
        with open(txt_file, "r") as e:
            lines = [e.strip() for e in e.readlines() if e.strip()]
        os.remove(txt_file)
        lines = list(set(lines))
        with ThreadPoolExecutor() as executor:
            executor.map(save, lines)
        print(">", c)
        return {}
    with open(txt_file, "r") as e:
        lines = e.read()
    if not lines:
        return {}
    os.remove(txt_file)
    datas = json.loads(lines)
    print(upclear*10, end="")
    return datas


def stablize(ds):
    for f in os.listdir("Files"):
        fn = f"Files/{f}"
        if not f.endswith(".json"):
            os.remove(fn)
            continue
        with open(fn, "r", encoding="utf-8") as e:
            data = json.load(e)
        uid = data.get("uploader_id")
        if uid:
            uid = uid[1:]
            ar = uid
            if ar in users:
                print(ar, "=>", users[ar])
                ar = users[ar]
                data["uploader"] = ar
            data["title"] = " ".join(e for e in data["title"].split(" ") if e)
            stop = 0
            pls = ds.get(uid)
            pt = None
            if ar in reverses:
                pt = reverses[ar]
            elif pls:
                pt = pls[-1].split("|")[-1]
                for p in pls[:-1]:
                    pz = p.split("|")
                    for z in pz:
                        v = z.replace("*", ".+")
                        if re.search(fr"{v}", data["title"]):
                            pt = pz[-1].strip().replace("*", " ")
                            stop = 1
                            break
                    if stop:
                        break
            if pt:
                print("* PL :", pt)
                data["playlist_title"] = pt
            with open(fn, "w") as e:
                json.dump(data, e)
            print(upclear*10, end="")
    with open("Datas/playlists.json", "w") as e:
        json.dump(lds, e, indent=2)


if __name__ == "__main__":
    import requests
    from bs4 import BeautifulSoup

    def monhtml(r, ref=None, data=None):
        sess = requests.session()
        sess.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        }
        if not ref:
            refs = r.split('/')[:3]
            ref = "/".join(refs)
        sess.headers["Referer"] = ref
        if data:
            r = sess.post(r, data=data)
        else:
            r = sess.get(r)
        encoding = r.encoding if 'charset' in r.headers.get(
            'content-type', '').lower() else None
        parser = 'html.parser'  # or lxml or html5lib
        return BeautifulSoup(r.content, parser, from_encoding=encoding)

    def get_datas(u):
        soup = monhtml(u)
        t = soup.title.text
        iframes = soup.findAll("iframe", src=True)
        # return iframes
        return [
            (
                link["src"].split("video=")[-1].split("/")[-1].split("?")[0],
                f'{t} {i}'
            )
            for i, link in enumerate(iframes, start=1)
            if "ok.ru" in link["src"] or "dailymotion" in link["src"]
        ]

    u = "https://www.footarchives.com/2024/09/20242025_35.html"
    print(get_datas(u))
