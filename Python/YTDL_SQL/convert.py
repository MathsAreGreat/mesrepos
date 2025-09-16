import hashlib
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from moviepy import AudioFileClip
from mutagen.id3 import APIC, COMM, ID3, TALB, TCON, TDRC, TIT2, TPE1, TPE2, TRCK, USLT

mesfiles = []

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

hayd = {"َ", "ّ", "!", "|", "؟"}

f = "infos.json"
with open(f, "r") as fl:
    datas = json.load(fl)


def remove_emoji(text):
    regex = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    t = regex.sub(r"", text)
    t = re.sub(r"[：:\.]+", r" - ", t)
    t = re.sub(r'"', r" ", t)
    t = re.sub(r"\s+", r" ", t)
    return t


def alreadyExist():
    uns = [f for f in os.listdir("/home/mohamed/Documents/datas/Backups")]
    for p in ["/home/mohamed/Music/Soundtracks", "Audios", "News"]:
        if os.path.exists(p):
            uns += [
                f.stem.split("(")[-1].split(")")[0]
                for f in Path(p).rglob("*")
                if f.suffix in (".mp3", ".m4a", ".webm")
            ]
    datas = []
    for f in os.listdir("Files"):
        code = f.rsplit(".", 1)[0]
        if code in uns:
            continue
        fn = f"Files/{f}"
        with open(fn, "r", encoding="utf-8") as e:
            data = json.load(e)
        # if data["uploader_id"][1:] not in ds:
        #     continue
        if data.get("duration") and data["duration"] > 60:
            datas.append(code)
    return datas


def tfiles():
    files = sorted(Path("/home/mohamed/Documents/Youtube/Subs/Lrc").rglob("*.lrc"))
    paroles = {}
    for f in files:
        key = f.stem
        if key in paroles:
            continue
        with open(f, "r", encoding="utf-8") as z:
            data = z.read()
        paroles[key] = data

    for f in Path("Files").glob("*json"):
        if f.stem.startswith("PL"):
            continue
        with open(f, "r") as fl:
            data = json.load(fl)
        try:
            ch = data["channel_id"]
            if ch in datas["defs"]:
                continue
            datas["defs"][ch] = {}
            datas["defs"][ch]["ID"] = data["uploader_id"]
            datas["defs"][ch]["ar"] = data["uploader"].strip()
            if ch in datas["Youtube"]:
                continue
            datas["Youtube"].append(ch)
        except:
            pass

    with open("infos.json", "w") as el:
        json.dump(datas, el, indent=4)

    genrate = {}
    for k, v in datas.items():
        if k == "defs":
            continue
        for e in v:
            genrate[e] = k.title()

    dataz = []
    for f in Path("Files").glob("*.json"):
        code = f.stem
        if code.startswith("PL"):
            continue
        with open(f, "r", encoding="utf-8") as e:
            data = json.load(e)
        try:
            dt = data.get("upload_date")
            if not dt:
                dt = ""
            ch = data["channel_id"]
            if ch:
                t = data["title"].strip()
                key = ""
                if "playlist_title" in data:
                    key = data["playlist_title"].strip()
                dd = (ch, key, dt, t, code)
                dataz.append(dd)
        except:
            pass

    dataz = sorted(dataz, key=lambda e: ".".join(s for s in e if s))
    infoz = {}
    cnt = []
    i = 1
    for *key, dt, t, code in dataz:
        cle = "".join(key)
        if cle not in cnt:
            i = 1
            cnt.append(cle)
        ch, al = key
        if "defs" not in datas:
            continue
        ar = datas["defs"][ch]["ar"]
        g = genrate[ch]
        comment = f"{code}{g}{ar}{al}{t}"
        t = remove_emoji(t)
        fl = {}
        fl["artist"] = ar.title()
        fl["album_artist"] = ar.title()
        fl["album"] = al.title()
        fl["genre"] = g.title()
        fl["track_number"] = f"{i}"
        fl["year"] = dt[:4]
        fl["date"] = dt
        fl["comment"] = cryypt(comment)
        fl["name"] = t.title()
        fl["title"] = f"{i:03}. {t.title()}"
        fl["lyrics"] = paroles.get(code)
        infoz[code] = fl
        i += 1
    return infoz


def cryypt(k, c=10):
    if not isinstance(c, int) or c <= 0:
        return cryypt(k)
    salt = "https://www.google.com"
    url = "https://live.cima4u.live/Episode" + k
    while c:
        url += salt
        url = hashlib.md5(url.encode()).hexdigest()
        c -= 1
    return url


def hawl(f):
    name = f.rsplit(".", 1)[0]
    nf = f"{name}.mp3"
    if os.path.exists(nf):
        os.remove(f)
        print(f, "is removed !")
        return 0
    clip = AudioFileClip(f)
    clip.write_audiofile(f"{name}_tmp.mp3")
    print(upclear * 10, f"{name}.mp3", "is extracted !")
    os.rename(f"{name}_tmp.mp3", nf)
    clip.close()
    return 1


def remove_empties(*paths):
    msg = " Time To Free Space "
    print(f"{msg:*^50}")
    print()
    for p in paths:
        c = 1
        z = 0
        if not os.path.exists(p):
            c = 0
        while c > 0:
            c = 0
            for current, dirs, files in os.walk(p):
                current = re.sub(r"\\", r"/", current)
                if len(dirs) + len(files) == 0:
                    c += 1
                    print(current, "is an empty folder !")
                    os.rmdir(current)


def convert(pth):
    mesfiles = []
    for c, _, files in os.walk(pth):
        mesfiles += [f"{c}/{f}" for f in files if f.endswith(("webm", "m4a"))]
    with ThreadPoolExecutor(10) as executor:
        executor.map(hawl, mesfiles)
    return len(mesfiles)


def teggings(pth):
    global mesfiles
    mesfiles = tfiles()
    lesfiles = [f for f in Path(pth).rglob("*") if f.is_file()]
    with ThreadPoolExecutor(50) as executor:
        executor.map(taggin, lesfiles)


def taggin(fname: Path):
    global mesfiles
    code = fname.stem
    datas = mesfiles.get(code)
    if not datas:
        print(">>>", code)
        return 0
    t = datas["name"].replace("/", "-")
    del datas["name"]
    dt = datas["date"]
    del datas["date"]

    if fname.suffix == ".mp3":
        datas["album_cover"] = code
        modify_metadata(fname, **datas)

    pts = "/home/mohamed/Music/Soundtracks"
    dto = Path(f"{pts}/{datas['genre']}/{datas['artist']}/{datas['album']}")
    dto.mkdir(parents=True, exist_ok=True)
    to = dto / f"{code}.mp3"
    if to == fname:
        return 1
    fname.rename(to)
    return 1


def tolrc(f):
    with open(f, "r", encoding="utf8") as e:
        infos = e.read().split("\n\n")
    start, *datas = infos
    datas = [l.split("\n") for l in datas if l.strip()]
    datas = [[gad(i, e) for i, e in enumerate(l)] for l in datas]
    datas = [(t, " ".join(s)) for t, *s in datas]
    datas = [f"[{t}] {s}" for t, s in datas]
    return re.findall(r"Language:([^\n]+)", start), datas


def gad(i, l):
    if i:
        return re.sub(r"\s+", r" ", l)
    l = l.split(" ")[0]
    r = l.split(":")
    if len(r) > 2:
        h, m, s = r
        if h == "00":
            l = f"{m}:{s}"
    return l


def lrci(f):
    item, info = tolrc(f)
    subs = "\n".join(info)
    fn = f.split("/")[-1]
    name, *eng = fn.replace(".vtt", "").rsplit(".", 1)
    if item:
        eng = item[0].strip()
    elif not eng:
        eng = "ar"
    else:
        eng = eng[0]
    lg = eng.title()
    spath = f"/home/mohamed/Documents/Youtube/Subs/Lrc/{lg}"
    nw = f"{spath}/{name}.lrc"
    if os.path.exists(nw):
        return 0
    os.makedirs(spath, exist_ok=True)
    with open(nw, "w", encoding="utf-8") as e:
        e.write(subs)
    print(">", name)
    return 1


def gad_lrc(pth):
    mesfiles = []
    to = "/home/mohamed/Documents/Youtube/Subs/Vtt"
    for c, _, files in os.walk(pth):
        for f in files:
            if f.endswith(".vtt"):
                os.rename(f"{c}/{f}", f"{to}/{f}")

    for c, _, files in os.walk(to):
        mesfiles += [f"{c}/{f}" for f in files if f.endswith(".vtt")]

    if mesfiles:
        print(f"{len(mesfiles)} Subtitles")
        with ThreadPoolExecutor(10) as executor:
            executor.map(lrci, mesfiles)


def gad_all(pth="Audios"):
    if os.path.exists(pth):
        nb = 1
        gad_lrc(pth)
        while nb:
            nb = convert(pth)
        teggings(pth)
        remove_empties(pth)

    ii = 0
    for f in Path("Files").glob("*.json"):
        with open(f, "r", encoding="utf-8") as e:
            data = json.load(e)
        if not data or not data["uploader"]:
            f.unlink()
            ii += 1
    print(">", ii, "items removed !")

    for f in Path("/home/mohamed/Music/Soundtracks").rglob(".mp3"):
        c = f.stem
        fn = f"/home/mohamed/Documents/datas/Backups/{c}"
        with open(fn, "w") as e:
            e.write("")

    remove_empties("/home/mohamed/Music/Soundtracks", "Audios", "News")
    print("> Updating Youtube IDs !")
    return 1


def dwn_jpeg(k):
    fn = f"/home/mohamed/Pictures/.Covers/YT_Covers/{k}.jpg"
    if os.path.exists(fn):
        return fn
    res = ["maxres", "sd", "hq", "mq", ""]
    for rs in res:
        url = f"https://i.ytimg.com/vi/{k}/{rs}default.jpg"
        with requests.get(url) as cover:
            bcontent = cover.content
            if len(bcontent) > 1100:
                with open(fn, "wb") as e:
                    e.write(cover.content)
                return fn
    return fn


def modify_metadata(
    file_path,
    title=None,
    artist=None,
    album=None,
    album_artist=None,
    genre=None,
    year=None,
    comment=None,
    track_number=None,
    force=0,
    album_cover=None,
    lyrics=None,
):
    # Open the audio file
    try:
        audio = ID3(file_path)
        existing_comment = audio["COMM::XXX"].text[0]
        if existing_comment == comment and force:
            return 0
    except Exception as err:
        print("**", err)
    audio = ID3()
    # Check if the comment is different or not present
    if comment:
        # Comment is different or not present, update it
        cm = COMM(encoding=3, text=comment)
        audio["COMM"] = cm

    if track_number:
        audio["TRCK"] = TRCK(encoding=3, text=track_number)

    # Modify the title tag
    if title:
        audio["TIT2"] = TIT2(encoding=3, text=title)

    # Modify the artists tag (TPE1)
    if artist:
        audio["TPE1"] = TPE1(encoding=3, text=artist)

    # Modify the album tag
    if album:
        audio["TALB"] = TALB(encoding=3, text=album)

    # Modify the album artist tag (TPE2 or ALBUMARTIST)
    if album_artist:
        audio["TPE2"] = TPE2(encoding=3, text=album_artist)

    # Modify the genre tag
    if genre:
        audio["TCON"] = TCON(encoding=3, text=genre)

    # Modify the year tag
    if year:
        audio["TDRC"] = TDRC(encoding=3, text=year)

    # Add the album cover URL as a link
    if album_cover:
        fn = dwn_jpeg(album_cover)
        with open(fn, "rb") as cover:
            audio["APIC"] = APIC(
                encoding=3,
                mime="image/jpeg",  # Replace with the appropriate MIME type if necessary
                type=3,  # 3 is for album cover
                desc="Cover",
                data=cover.read(),
            )

    if lyrics:
        audio.add(USLT(encoding=3, text=lyrics.strip()))
    # Save the changes
    print(upclear * 10, "::", comment)
    audio.save(file_path)


if __name__ == "__main__":
    gad_all()
