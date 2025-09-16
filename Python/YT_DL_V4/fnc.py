import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

DOM = "https://www.youtube.com"


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
    dp = "/home/mohamed/Music/YT_Songs/tmp/%(id)s.%(ext)s"
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


def channelize(c, **additionals):
    json_file = Path(f"/home/mohamed/Documents/Youtube/IDs/1{c}.json")
    if not json_file.exists():
        json_file = Path(f"/home/mohamed/Documents/Youtube/IDs/{c}.json")
        txt_file = Path(f"Files/{c}.txt")
        if not txt_file.exists():
            if not txt_file.exists():
                dd = f"{DOM}/watch?v={c}"
                txt_file = Path(f"Files/{c}.txt")
                print("Loading", c, "!")
                cmd = f'yt-dlp "{dd}" --cookies-from-browser firefox --flat-playlist --dump-json > {txt_file}'
                os.system(cmd)
                print("Loaded", c, "!")
            with txt_file.open("r") as e:
                data = e.read()
            if not data:
                return {}
        txt_file.unlink()
        datas = json.loads(data)
        if datas["title"] == "[Private video]":
            return None
        info = {k: v for k, v in datas.items() if k in keys}
        art, *tt = re.findall(r"[^\-]+", info["title"])
        if not tt:
            tt = [""]
        tt = tt[0]
        info["artist"] = art.split("(")[0].strip()
        info["name"] = tt.split("(")[0].strip()
        if additionals:
            info.update(additionals)
        print(upclear * 10, end="")
        with json_file.open("w") as e:
            json.dump(info, e, indent=2)
    else:
        with json_file.open("r") as e:
            info = json.load(e)
    return info


if __name__ == "__main__":
    c = "VHygTMF98Rw"
    channelize(c)
    thumbnaudio(c)
