import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import eyed3
import redis
import requests
from rich import print

rds = redis.Redis(host="localhost", port=6379, decode_responses=True)

mesfiles = {}

gs_path = Path("genres.json")
with gs_path.open("r", encoding="utf-8") as e:
    genres = json.load(e)

us_path = Path("users.json")
with us_path.open("r", encoding="utf-8") as e:
    users = json.load(e)

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

hayd = {"َ", "ّ", "!", "|", "؟"}

infos = {
    "Audiobooks": [
        "Eslam Adel",
        "Tasgeel Podcast",
        "Audiobook بالعربي",
        "Readtube - جيل يقرأ",
    ],
    "Podcasts": [
        "Omar Aburobb",
        "Haidurant",
        "Yamane History",
        "Mr Ballen",
        "Mahmood Mahdy",
        "The Pot Cast",
        "قرية العجائب - بدر العلوي",
        "Ma7nsbus",
        "المواطن سعيد",
        "عمرو عابدين",
        "Loai Fawzi",
        "Mohamed Saadani",
        "mohamed abd elati",
        "AlJazeera Arabic",
        "Mics Podcasts",
        "Yaya Azzam",
        "طحالب",
        "Alcha5Ana",
        "Abdullatif",
        "Abu Sadeq",
        "Sameh Sanad",
        "Mahmoud Abo Ismail",
        "Mohamed Goely",
        "Fahmy Productions",
        "الدحيح",
    ],
    "Writings": [
        "AJplus Saha",
    ],
    "Religious": [
        "عبدالرحمن مسعد",
        "عبدالله مصطفى",
        "Sameh Hussien",
        "Islam Sobhi | القارئ اسلام صبحي",
    ],
    "Pure": [
        "Palmtherapysounds.Com",
        "Chaama Z",
        "Zamane",
        "Spacetoon",
        "Carmen Tockmaji",
        "Taha Nouri",
        "Alaa Wardi",
        "Ash",
    ],
}

genrate = {}

for k, v in infos.items():
    for e in v:
        genrate[e.lower()] = k.title()


def remove_emoji(text):
    regex = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    t = regex.sub(r"", text)
    t = re.sub(r"[:\.]+", r" - ", t)
    t = re.sub(r'"', r" ", t)
    t = re.sub(r"\s+", r" ", t)
    return t


def alreadyexist():
    uns = []

    for f in Path("Files").glob("*txt"):
        f.unlink()

    for p in [
        "/home/mohamed/Music/Soundtracks",
        "/home/mohamed/Music/Soundtrackz",
        "Audios",
    ]:
        if Path(p).exists():
            uns += [
                f.stem.split("(")[-1].split(")")[0]
                for f in Path(p).rglob("*")
                if f.suffix in (".mp3", ".m4a", ".webm")
            ]
    datas = []
    for pt in ["/home/mohamed/Documents/Youtube/IDs", "Files"]:
        for f in Path(pt).glob("*json"):
            code = f.stem
            if rds.sismember("backup:ytb", code):
                continue
            if code in uns:
                continue
            min_time = 60
            with f.open("r", encoding="utf-8") as e:
                data = json.load(e)
            if data.get("duration") and data["duration"] > min_time:
                datas.append(code)
    datas = list(set(datas))
    print(">", len(datas), "items !")
    return datas


def tfiles() -> dict:
    files = sorted(Path("/home/mohamed/Documents/Youtube/Subs/Lrc").rglob("*.lrc"))
    paroles = {}
    with Path("addons.json").open("r") as f:
        infoz = json.load(f)

    for file in files:
        key = file.stem
        if key in paroles:
            continue
        with file.open("r", encoding="utf-8") as f:
            paroles[key] = f.read()

    datas = []
    files = list(Path("Files").glob("*.json"))
    files += [
        f
        for f in Path("/home/mohamed/Documents/Youtube/IDs").glob("*.json")
        if f not in files
    ]

    for file in files:
        try:
            code = file.stem
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not data:
                    continue
                dt = data["upload_date"]
                chid = data.get("channel_id")
                ch = users.get(chid) if chid and users.get(chid) else data["uploader"]
                data["uploader"] = ch
                g = genres.get(chid) if chid and genres.get(chid) else data.get("genre")
                data["genre"] = g
                if ch:
                    t = data["title"].strip()
                    key = data.get("playlist_title", "").strip()
                    dd = (ch, key, dt, t, code, g)
                    datas.append(dd)
                    file.unlink()
                    Path(f"/home/mohamed/Documents/Youtube/IDs/{code}").unlink(True)
                    with Path(f"/home/mohamed/Documents/Youtube/IDs/{code}.json").open(
                        "w", encoding="utf-8"
                    ) as f:
                        json.dump(data, f)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    with Path("gc_links.json").open("w", encoding="utf-8") as f:
        json.dump(datas, f)

    cnt = []
    i = 1
    for *key, dt, tl, code, g in datas:
        cle = "".join(key)
        if cle not in cnt:
            i = 1
            cnt.append(cle)
        ar, al = key
        if not g:
            g = genrate.get(ar.lower(), "Youtube")
        comment = f"{code}{g}{ar}{al}{tl}"
        t = remove_emoji(tl)
        fl = {
            "artist": ar.title(),
            "album_artist": ar.title(),
            "album": al.title(),
            "genre": g.title(),
            "track_number": f"{i}",
            "year": dt[:4],
            "date": dt,
            "comment": cryypt(comment),
            "name": t.title(),
            "title": f"{dt}. {t.title()}",
            "lyrics": paroles.get(code),
        }
        infoz[code] = fl
        i += 1
    return infoz


def tfile(i, code):
    files = sorted(Path("/home/mohamed/Documents/Youtube/Subs/Lrc").rglob("*.lrc"))
    paroles = None
    for f in files:
        key = f.stem
        if key != code:
            continue
        with f.open("r", encoding="utf-8") as z:
            paroles = z.read()
        break
    f = Path(f"/home/mohamed/Documents/Youtube/IDs/{code}.json")

    if not f.exists():
        return {}

    with f.open("r", encoding="utf-8") as e:
        data = json.load(e)
    if not data:
        return {}

    dt = data["upload_date"]
    chid = data.get("channel_id")
    ch = users.get(chid) if chid and users.get(chid) else data["uploader"]
    data["uploader"] = ch
    g = genres.get(chid) if chid and genres.get(chid) else data.get("genre")
    data["genre"] = g
    if ch:
        t = data["title"].strip()
        key = ""
        if "playlist_title" in data:
            key = data["playlist_title"].strip()

        with f.open("w", encoding="utf-8") as e:
            json.dump(data, e)

    if not g:
        g = genrate.get(ch.lower(), "Youtube")

    comment = f"{code}{g}{ch}{key}{t}"
    t = remove_emoji(t)
    fl = {}
    fl["artist"] = ch.title()
    fl["album_artist"] = ch.title()
    fl["album"] = key.title()
    fl["genre"] = g.title()
    fl["track_number"] = int(f"{i}")
    fl["year"] = int(dt[:4])
    fl["date"] = dt
    fl["comment"] = cryypt(comment)
    fl["name"] = t.title()
    fl["title"] = f"{dt}. {t.title()}"
    fl["lyrics"] = paroles
    return fl


def cryypt(k, c=10):
    if not isinstance(c, int) or c <= 0:
        return cryypt(k)
    salt = "https://www.google.com"
    url = "https://live.cima4u.live/Episode" + k
    while c:
        url += salt
        url = hashlib.md5(url.encode(), usedforsecurity=False).hexdigest()
        c -= 1
    return url


def remove_empties(*paths):
    msg = " Time To Free Space "
    print(f"{msg:*^50}")
    print()
    for pt in paths:
        p = Path(pt)
        c = 1
        if not p.exists():
            c = 0
        while c > 0:
            c = 0
            for current in p.rglob("*"):
                if not current.is_dir():
                    continue
                items = list(current.glob("*"))
                if len(items) > 0:
                    continue
                current.rmdir()
                c += 1


def teggings(pth):
    lesfiles = [f for f in Path(pth).rglob("*") if f.is_file()]
    with ThreadPoolExecutor(50) as executor:
        executor.map(lambda e: taggin(*e), enumerate(lesfiles, start=1))


def taggin(nb: int, fname: Path):
    code = fname.stem
    datas = tfile(nb, code)
    if not datas:
        print(">>>", code)
        return 0
    del datas["name"]
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
    with Path(f).open("r", encoding="utf8") as e:
        infos = e.read().split("\n\n")
    start, *datas = infos
    datas = [line.split("\n") for line in datas if line.strip()]
    datas = [[gad(i, e) for i, e in enumerate(line)] for line in datas]
    datas = [(t, " ".join(s)) for t, *s in datas]
    datas = [f"[{t}] {s}" for t, s in datas]
    return re.findall(r"Language:([^\n]+)", start), datas


def gad(i, line):
    if i:
        return re.sub(r"\s+", r" ", line)
    nbr = 2
    line = line.split(" ")[0]
    r = line.split(":")
    if len(r) > nbr:
        h, m, s = r
        if h == "00":
            line = f"{m}:{s}"
    return line


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
    spath = Path(f"/home/mohamed/Documents/Youtube/Subs/Lrc/{lg}")
    nw = spath / f"{name}.lrc"
    if nw.exists():
        return 0
    spath.mkdir(parents=True, exist_ok=True)
    with nw.open("w", encoding="utf-8") as e:
        e.write(subs)
    print(">", name)
    return 1


def gad_lrc(pth):
    to = Path("/home/mohamed/Documents/Youtube/Subs/Vtt")
    for f in Path(pth).rglob("*.vtt"):
        fv = to / f.name
        if fv.is_file():
            fv.unlink()
        f.rename(fv)

    mesfiles = [str(f) for f in to.rglob("*.vtt")]

    if mesfiles:
        print(f"{len(mesfiles)} Subtitles")
        with ThreadPoolExecutor(10) as executor:
            executor.map(lrci, mesfiles)


def gad_all(pth="Audios"):
    if Path(pth).exists():
        gad_lrc(pth)
        teggings(pth)
        remove_empties(pth)

    ii = 0
    for f in Path("Files").glob("*.json"):
        with f.open("r", encoding="utf-8") as e:
            data = json.load(e)
        if not data or not data["uploader"]:
            f.unlink()
            ii += 1
    print(">", ii, "items removed !")

    for f in Path("/home/mohamed/Music/Soundtracks").rglob("*.mp3"):
        c = f.stem
        rds.sadd("backup:ytb", c)

    remove_empties("/home/mohamed/Music/Soundtracks", "Audios")
    print("> Updating Youtube IDs !")
    print(":: Finished !")
    return 1


def dwn_jpeg(k):
    covers_path = Path("/home/mohamed/Pictures/.Covers/YT_Covers")
    fn = covers_path / f"{k}.jpg"
    if fn.exists():
        return fn
    covers_path.mkdir(parents=True, exist_ok=True)
    res = ["maxres", "sd", "hq", "mq", ""]
    minimum_size = 1100
    for rs in res:
        url = f"https://i.ytimg.com/vi/{k}/{rs}default.jpg"
        with requests.get(url, timeout=10) as cover:
            bcontent = cover.content
            if len(bcontent) > minimum_size:
                with fn.open("wb") as e:
                    e.write(cover.content)
                return fn
    return fn


def modify_metadata(
    file_path: Path,
    title: str = None,
    artist: str = None,
    album: str = None,
    album_artist: str = None,
    genre: str = None,
    year: int = None,
    comment: str = None,
    track_number: int = None,
    album_cover: str = None,
    lyrics: str = None,
) -> None:
    try:
        audio_file = eyed3.load(file_path)
        if audio_file.tag is None:
            audio_file.initTag()

        if title:
            audio_file.tag.title = title
        if artist:
            audio_file.tag.artist = artist
        if album:
            audio_file.tag.album = album
        if album_artist:
            audio_file.tag.album_artist = album_artist
        if genre:
            audio_file.tag.genre = genre
        if year:
            audio_file.tag.recording_date = eyed3.core.Date(year)
        if comment:
            audio_file.tag.comments.set(comment)
        if track_number:
            audio_file.tag.track_num = track_number
        if lyrics:
            audio_file.tag.lyrics.set(lyrics.strip())

        if album_cover:
            cover_file = dwn_jpeg(album_cover)
            if cover_file.exists():
                with cover_file.open("rb") as img_fp:
                    image_data = img_fp.read()
                audio_file.tag.images.set(3, image_data, "image/jpeg", "Cover")

        audio_file.tag.save()
        print(f"Metadata updated for {file_path.name}")
    except Exception as e:
        print(f"Error updating metadata for {file_path.name}: {e}")


if __name__ == "__main__":
    gad_all()
