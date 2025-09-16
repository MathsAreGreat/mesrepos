import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import requests
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

d_today = datetime.now().strftime("%Y%m%d")

pp = "/home/mohamed/Downloads"

os.chdir(pp)

cc = 10

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


def tojpg(img_input):
    name, ex = img_input.rsplit(".", 1)
    if ex == "jpg":
        return 0
    fname = f"{name}.jpg"
    if os.path.exists(fname):
        os.remove(img_input)
        print("::", name.split("/")[-1])
    image = Image.open(img_input).convert("RGB")
    image.save(f"{name}.jpg")
    print(">>", name.split("/")[-1])
    return 1


def finalize(pp):
    nb = 1
    while nb:
        mesfiles = []
        for cr, _, files in os.walk(pp):
            mesfiles += [f"{cr}/{f}" for f in files if f.endswith("webp")]
        with ThreadPoolExecutor(20) as executor:
            executor.map(tojpg, mesfiles)
        nb = len(mesfiles)
    return 1


def save(datas):
    infos = {k: datas[k] for k in keys if k in datas}
    tb = infos["subtitles"]
    if tb:
        k = "live_chat"
        if k in tb:
            del tb[k]
        for key, val in tb.items():
            tb[key] = val[-1]["url"]
        infos["subtitles"] = tb
    return infos


def chs(c):
    c = c.strip()
    dv = f"/home/mohamed/Documents/.Socials/Twitter/Datas/{c}.json"
    if os.path.exists(dv):
        return 0
    url = f"https://twitter.com/i/status/{c}"
    dp = f"/home/mohamed/Documents/.Socials/Twitter/Datas/{c}.txt"
    cmd = f'yt-dlp "{url}" --flat-playlist --skip-download --dump-json > {dp}'
    os.system(cmd)
    with open(dp, "r") as e:
        datas = e.readlines()
    datas = [save(json.loads(e)) for e in datas if e.strip()]
    os.remove(dp)
    with open(dv, "w") as e:
        json.dump(datas, e)
    return 1


def doun(doc, link):
    u = link.get("base_url")
    if not u:
        return 0
    fl = u.split("/")[-1].split("?")[0]
    fn = f"{doc}/delitem_{ID}_{fl}"
    if not os.path.exists(fn):
        try:
            r = requests.get(u, stream=True)
            with open(fn, "wb") as e:
                for chunk in r.iter_content(chunk_size=2048):
                    e.write(chunk)
            return fn
        except:
            return 0
    return fn


pp = "/home/mohamed/Documents/.Socials"
finalize(pp)
itemat = []
for f in os.listdir():
    name, *ex = f.rsplit(".", 1)
    if ex:
        if name.startswith("d_scrape_twitter"):
            art, ID, *_ = name.replace("d_scrape_twitter_", "").split("_")
            with open(f, "r") as e:
                datas = json.load(e)
            os.makedirs(f"{pp}/Twitter/Vids", exist_ok=True)
            fp = f"{pp}/Twitter/Vids/{ID}"
            with open(fp, "w") as e:
                e.write("")
            fp = f"{pp}/Twitter/Images/Files/{d_today}"
            for u in datas:
                v = u.split("/")[-1].split(".")[0].split("?")[0]
                fn = f"{fp}/{art}_{ID}_{v}.jpg"
                if not os.path.exists(fn):
                    os.makedirs(fp, exist_ok=True)
                    r = requests.get(u)
                    with open(fn, "wb") as e:
                        e.write(r.content)
            os.remove(f)
        elif name.startswith("d_scrape_insta"):
            fp = f"{pp}/Instagram"
            with open(f, "r") as e:
                data = json.load(e)
            if not data:
                *_, ID = name.split("_", 3)
                ID = ID[:11]
                Path(f"{fp}/vid_{ID}.jpg").touch()
                os.remove(f)
                continue

            ds = data["user"]
            ID = data["code"]
            tt = data["timestamp"]
            links = data["links"]
            if not isinstance(links, list):
                links = [links]
            try:
                for u in links:
                    fl = u.split("/")[-1].split("?")[0]
                    doc = f"{fp}/{ds}"
                    fn = f"{doc}/{tt}_{ID}_{fl}"
                    if not os.path.exists(fn):
                        os.makedirs(doc, exist_ok=True)
                        r = requests.get(u, timeout=5)
                        with open(fn, "wb") as e:
                            e.write(r.content)
                if os.path.exists(f):
                    os.remove(f)
            except Exception as err:
                print(err)
        elif name.startswith("scraped_face"):
            fp = f"{pp}/Facebooks"
            _, s, ID, *_ = name.split("_")
            if ex[0] == "json":
                try:
                    with open(f, "r") as e:
                        data = json.load(e)
                except:
                    continue
                # os.rename(f, f"Files/{f}")
                if "image" in data:
                    ds = data["owner"]["id"]
                    dt_str = datetime.fromtimestamp(data["created_time"]).strftime(
                        "%Y%m%d%H%M%S"
                    )
                    u = data["image"]["uri"]
                    try:
                        fl = u.split("/")[-1].split("?")[0]
                        doc = f"{fp}/{ds}"
                        fn = f"{doc}/{dt_str}_{ID}_{fl}"
                        if not os.path.exists(fn):
                            os.makedirs(doc, exist_ok=True)
                            r = requests.get(u, stream=True)
                            with open(fn, "wb") as e:
                                e.write(r.content)
                    except:
                        pass
                os.remove(f)
            elif ex[0] == "txt":
                with open(f, "r") as e:
                    data = e.read()
                os.rename(f, f"Files/{f}")
                infos = json.loads(data)
                ds = ".".join(
                    e.strip().replace("'", ".")
                    for e in infos["val"].split(" ")
                    if e.strip()
                )
                doc = f"{fp}/{ds}"
                fdoc = f"{doc}/{ID}.mp4"
                if os.path.exists(fdoc):
                    continue
                if isinstance(infos["img"], list):
                    datas = set(infos["img"])
                    info = []
                    for data in datas:
                        if ID not in data:
                            continue
                        while True:
                            c = 0
                            if not data.startswith("["):
                                data = data[1:]
                                c += 1
                            if not data.endswith("]"):
                                data = data[:-1]
                                c += 1
                            if c == 0:
                                break
                        info = [
                            e for e in json.loads(data) if int(e["video_id"]) == int(ID)
                        ]
                        if info:
                            break
                    if not info:
                        continue
                    links = sorted(
                        info[0]["representations"],
                        key=lambda e: e["width"],
                        reverse=True,
                    )
                else:
                    links = [{"base_url": infos["img"]}]
                audio = links[-1]
                video = [{}]
                if len(links) > 1:
                    video = links[:-1]

                os.makedirs(doc, exist_ok=True)
                r = doun(doc, audio)
                files = [r]
                for link in video:
                    r = doun(doc, link)
                    if r:
                        files.append(r)
                        break
                if len(files) > 1:
                    s, e = files
                    cmd = f"""ffmpeg -i "{s}
                        " -i {e} -c:v copy -c:a aac -strftime 1 "{fdoc}" """
                    os.system(cmd)
                else:
                    fn = files[0]
                    os.rename(fn, fdoc)

vtt = "/home/mohamed/Documents/Projects/Python/playwrights/Files"
for f in os.listdir(vtt):
    fnc = f"{vtt}/{f}"
    ID = f.split(".")[0]
    with open(fnc, "r") as fl:
        data = json.load(fl)
    if not data:
        doc = f"{pp}/Facebooks/Vides"
        os.makedirs(doc, exist_ok=True)
        fn = f"{doc}/createdtime_{ID}_tn.jpg"
        with open(fn, "wb") as f:
            f.write(b"")
        os.remove(fnc)
        continue
    created_time = data["created_time"]
    try:
        ar = data["owner"]["user_id"]
        u = data["image"]["uri"]
        tn = u.split("/")[-1].split("?")[0]
    except:
        os.remove(fnc)
        continue
    doc = f"{pp}/Facebooks/{ar}"
    fn = f"{doc}/{created_time}_{ID}_{tn}"
    if os.path.exists(fn):
        print(fn, "existed")
        continue
    os.makedirs(doc, exist_ok=True)
    try:
        r = requests.get(u)
        with open(fn, "wb") as f:
            f.write(r.content)
        os.remove(fnc)
    except Exception as err:
        print(err)
        if os.path.exists(fn):
            os.remove(fn)

fn = Path(f"/home/mohamed/Documents/datas/Docker/{d_today}.json")
if not fn.exists():
    fn.parent.mkdir(exist_ok=True, parents=True)
    u = "http://localhost/cours"
    try:
        r = requests.get(u, stream=True, timeout=5)
        with open(fn, "w") as e:
            json.dump(r.json(), e)
    except:
        pass

fn = Path("/home/mohamed/Downloads/code.txt")
if fn.exists():
    with open(fn, "r") as e:
        data = e.read()
    dt = datetime.now().strftime("%Y-%m-%d-%H")
    with open("/home/mohamed/Documents/datas/Databases/ugeens.txt", "a") as e:
        e.write(f"\n{dt}\n{data}")
    fn.unlink()
