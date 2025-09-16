import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

d_path = "Videos/%(id)s.%(ext)s"
s_path = "Videos/Files/%(title)s/%(upload_date)s_%(section_title)s (%(id)s).%(ext)s"

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

DOM = "https://www.youtube.com"

us_path = Path("users.json")
pl_path = Path("pls.json")
usd_path = Path("users_id.json")

with pl_path.open("r", encoding="utf-8") as e:
    pls = json.load(e)

with us_path.open("r", encoding="utf-8") as e:
    users = json.load(e)

with usd_path.open("r", encoding="utf-8") as e:
    users_id = json.load(e)

ups = {k: v for v, k in users.items()}
upds = {k: v for v, k in users_id.items()}

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
    q = "bestaudio"
    dp = "Audios/%(uploader_id)s_%(upload_date)s_%(title)s (%(id)s).%(ext)s"
    dp = "Audios/%(id)s.%(ext)s"
    url = nbr
    if not nbr.startswith("PL"):
        url = f"{DOM}/watch?v={nbr}"
    sub = [
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--write-sub",
        "--sub-langs",
        "all,-live_chat",
        "--cookies-from-browser",
        "firefox",
    ]
    cmd = [
        "yt-dlp",
        "-f",
        q,
        url,
        "--ignore-errors",
        "--match-filter",
        "!is_live",
        "-o",
        dp,
        "--concurrent-fragments",
        "16",
        *sub,
    ]
    subprocess.run(cmd, check=True)
    print(upclear * 10, end="")


def gad(st):
    data = json.loads(st)
    if data["title"] == "[Private video]":
        return None
    keys = {"id", "playlist_id", "playlist_title"}
    info = {k: v for k, v in data.items() if k in keys}
    return info


def save(st):
    data = gad(st)
    if not data:
        return 0
    c = data["id"]
    json_file = Path(f"/home/mohamed/Documents/Youtube/IDs/{c}.json")
    if json_file.exists():
        return 0
    json_file = Path(f"Files/{c}.json")
    if json_file.exists():
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
    infos.pop(k, None)

    with json_file.open("w") as e:
        json.dump(infos, e, indent=2)
    return 1


def channelize(dd):
    c, mx, *fs = dd
    if mx < 0:
        return 0
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
    txt_file = Path(f"Files/{c}.txt")
    if not txt_file.exists():
        dd = f"{DOM}/@{c}/videos"
        if c.startswith("UC"):
            dd = f"{DOM}/channel/{c}/videos"
        elif c.startswith("PL"):
            dd = f"{DOM}/playlist?list={c}"
        elif c.startswith("=="):
            c = c[2:]
            dd = f"{DOM}/watch?v={c}"
            txt_file = Path(f"Files/{c}.txt")
            cnt = 0
        print("Loading", c, "!")
        cmd = (
            f'yt-dlp "{dd}" --cookies-from-browser firefox --flat-playlist --dump-json'
        )
        if mx:
            cmd += f' --playlist-end "{mx}" '
        cmd += f' --match-title "{f}"'
        cmd += f' --reject-title "{r}"'
        cmd += f" > {txt_file}"
        os.system(cmd)
        print("Loaded", c, "!")
    if cnt:
        with txt_file.open("r") as el:
            lines = [e.strip() for e in el.readlines() if e.strip()]
        txt_file.unlink()
        with ThreadPoolExecutor(30) as executor:
            executor.map(save, lines)
        print(">", c)
        return {}
    with txt_file.open("r") as e:
        lines = e.read()
    if not lines:
        return {}
    txt_file.unlink()
    datas = json.loads(lines)
    print(upclear * 10, end="")
    return datas


def stablize(ds):
    for f in Path("Files").glob("*"):
        if f.suffix != ".json":
            f.unlink()
            continue
        with f.open("r", encoding="utf-8") as e:
            data = json.load(e)

        uid = data.get("channel_id")
        if uid:
            data["title"] = " ".join(e for e in data["title"].split(" ") if e)
            usd = users_id.get(uid)
            if usd:
                data["uploader_id"] = f"@{usd}"
            elif data.get("uploader_id"):
                users_id[uid] = data.get("uploader_id")[1:]

            user = users.get(uid)
            if user:
                data["uploader"] = user
            elif data.get("uploader"):
                users[uid] = data["uploader"]

            pl = pls.get(uid)
            if not pl:
                if ch := users_id.get(uid):
                    for ck, v in ds.items():
                        c, k = ck.split("==")
                        if c != ch:
                            continue
                        if k in data["title"]:
                            data["playlist_title"] = v
                            print(f.stem, ":", v)
                            break
            else:
                data["playlist_title"] = pl

            with f.open("w", encoding="utf-8") as e:
                json.dump(data, e)
            print(upclear * 10, end="")

    with us_path.open("w", encoding="utf-8") as e:
        json.dump(users, e, indent=4)
    with usd_path.open("w", encoding="utf-8") as e:
        json.dump(users_id, e, indent=4)
