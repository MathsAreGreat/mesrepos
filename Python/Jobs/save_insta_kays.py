import base64
from datetime import datetime, timezone
import json
import os
import re
from pathlib import Path
from PIL import Image
import requests
from bs4 import BeautifulSoup
from Mido.variables import run_tasks

pp = "/home/mohamed/Pictures/.InstaGram"

uniques = []
itemz = []
for *_, files in os.walk(pp):
    unique = [
        "_".join(f.replace("dashinit", "dashinit_n").split("_")[1:-4]) for f in files
    ]
    uniques += [f for f in set(unique)]

fnm = "/home/mohamed/Documents/Projects/PYTHON/Selenium/vids.json"
fvm = "/home/mohamed/Documents/Files/instuns.json"


def data_XsU(encoded_segment, offset):
    try:
        decoded = base64.b64decode(encoded_segment + "===").decode("utf-8")
        extracted_number = int(re.sub(r"\D", "", decoded)) - int(offset)
        return chr(extracted_number)
    except Exception as e:
        print(f"Error decoding segment {encoded_segment}: {e}")
        return None


try:
    with open(fnm, "r", encoding="utf-8") as e:
        datas = json.load(e)
except:
    datas = []


try:
    with open(fvm, "r", encoding="utf-8") as e:
        instuns = json.load(e)
except:
    instuns = []

ii = 0
f_uniques = []


datas = [e for e in set(datas) if e not in uniques]
with open(fnm, "w") as e:
    json.dump(datas, e, indent=2)

for f in Path("/home/mohamed/Downloads").glob("d_scrape_alphacoder*json"):
    try:
        doc = Path("/home/mohamed/Documents/Files/AlphaCoders")
        ID = f.stem.split("_")[-2]
        fn = doc / f"{ID}.json"
        if not fn.exists():
            with open(f, "r", encoding="utf-8") as e:
                data = json.load(e)
            doc.mkdir(parents=True, exist_ok=True)
            f.rename(fn)

            t = data["title"].replace(" ", ".").title()
            u = data["src"]
            r = requests.get(u, stream=True)
            ds = Path("/home/mohamed/Pictures/Wallpapers/AlphaCoders")
            ds.mkdir(parents=True, exist_ok=True)
            fn = ds / f"{t}.{ID}.{u.split('/')[-1]}"
            with open(fn, "wb") as e:
                e.write(r.content)
        else:
            f.unlink()
    except Exception as err:
        print(err)


def fetch_urls(data):
    parser = "html.parser"  # or lxml or html5lib
    soup = BeautifulSoup(data, parser)
    bts = soup.findAll("button", {"data-url": True})
    return {bt.text: bt["data-url"] for bt in bts}


file_doc = Path("/home/mohamed/Downloads")


for fv in file_doc.glob("DFaselHD_*json"):
    try:
        with open(fv, "r", encoding="utf-8") as e:
            datas = json.load(e)
    except:
        print(f"Error processing {fv}")
        fv.unlink()
        continue
    dt_doc = Path("/home/mohamed/Documents/datas/Fasel/Datas")
    dt_doc.mkdir(parents=True, exist_ok=True)
    k, *hide_my_HTML, offset = datas
    adilbo_HTML_encoder_tYb = ""

    hide_my_HTML_myH = "".join(hide_my_HTML)

    for part in hide_my_HTML_myH.strip().split("."):
        p = data_XsU(part, offset)
        if p:
            adilbo_HTML_encoder_tYb += p
    soup = BeautifulSoup(adilbo_HTML_encoder_tYb, "html.parser")

    f = dt_doc / f"{k}.json"
    with open(f, "w") as e:
        json.dump(
            {
                el.text.strip(): el["data-url"]
                for el in soup.find_all("button", class_="hd_btn")
                if el.text.strip().endswith("p")
            },
            e,
        )
    fv.unlink()


for fv in file_doc.glob("d_scrape_FaselHD_*json"):
    with open(fv, "r", encoding="utf-8") as e:
        datas = json.load(e)
    dt_doc = Path("/home/mohamed/Documents/datas/Fasel/Datas")
    dt_doc.mkdir(parents=True, exist_ok=True)
    k = datas["ID"]
    videos = fetch_urls(datas["data"])

    f = dt_doc / f"{k}.json"
    with open(f, "w") as e:
        json.dump({k if k.endswith("p") else "144p": v for k, v in videos.items()}, e)
    fv.unlink()

for fv in file_doc.glob("d_scrape_Fasel_*json"):
    with open(fv, "r", encoding="utf-8") as e:
        datas = json.load(e)
    season_doc = Path("/home/mohamed/Documents/datas/Fasel/Seasons")
    season_doc.mkdir(parents=True, exist_ok=True)
    episode_doc = Path("/home/mohamed/Documents/datas/Fasel/Episodes")
    episode_doc.mkdir(parents=True, exist_ok=True)
    movie_doc = Path("/home/mohamed/Documents/datas/Fasel/Movies")
    movie_doc.mkdir(parents=True, exist_ok=True)

    k = datas["ID"]
    data = datas["infos"]  # all infos here !

    gr = data["genre"].title()  # Movies, Animes, TV Shows, etc.
    if not gr.endswith("s"):
        gr = f"{gr}s"
    poster = data["poster"]
    short = data["short"].split("=")[-1]
    ts = re.sub(r"[^a-z0-9]", r" ", data["title"], flags=re.IGNORECASE).split(" ")
    title = ".".join(e for e in ts if e)
    if not data.get("ep"):
        gr = "Movies"
        info = {
            "t": title,
            "dl": k,
            "gr": gr,
            "poster": poster,
        }
        f = movie_doc / f"{short}.json"
        with open(f, "w") as e:
            json.dump(info, e)
    else:
        seasons = [re.findall(r"[0-9]+", s)[-1] for s in data.get("seasons", [])]
        ss = ""
        sn = ""
        if data.get("ss"):
            ss = data["ss"].replace("موسم ", "").strip().zfill(2)
        if data.get("sn"):
            sn = re.findall(r"[0-9]+", data["sn"])[-1]
        ep = data["ep"].replace("الحلقة ", "").strip().zfill(2)
        u = data["u"]

        info = {
            "t": title,
            "ss": ss,
            "sns": seasons,
            "poster": poster,
            "eps": data["episodes"],
            "gr": gr,
        }
        f = season_doc / f"{sn}.json"
        with open(f, "w") as e:
            json.dump(info, e)

        info = {
            "ep": ep,
            "sn": sn,
            "dl": k,
            "u": u,
        }
        f = episode_doc / f"{short}.json"
        with open(f, "w") as e:
            json.dump(info, e)
    fv.unlink()


fn = "/home/mohamed/Documents/datas/Daily/okru.json"

try:
    with open(fn, "r", encoding="utf-8") as e:
        datas = json.load(e)
except:
    datas = {}


for fv in file_doc.glob("disokru_*json"):
    with open(fv, "r", encoding="utf-8") as e:
        dt = json.load(e)
    fv.unlink()
    for dd in dt:
        k, v = dd.split("==", 1)
        if k in datas:
            continue
        datas[k] = v


with open(fn, "w", encoding="utf-8") as e:
    json.dump(datas, e, indent=4)


def srcify(item):
    elements = item.get("video_versions")
    if not elements:
        elements = item["image_versions2"]["candidates"]
    element = max(elements, key=lambda el: el["height"])
    return element["url"]


prt = Path("/home/mohamed/Documents/.Socials/Instagram")

parent = Path("/home/mohamed/Downloads")

with open("/home/mohamed/Documents/datas/Databases/instas.txt", "r") as fl:
    datas = fl.readlines()
datas = [e.strip() for e in datas if e.strip() and ("/p/" in e or "/reel/" in e)]

uns = [f.stem.split("==")[0] for f in prt.rglob("*") if f.is_file()]

for f in parent.glob("*.json"):
    if not f.stem.startswith("scraped_useristag"):
        continue
    try:
        with f.open("r") as fl:
            data = json.load(fl)
        datas += data
        f.unlink()
    except:
        continue
datas = [e.split("/")[-3:-1] for e in set(datas) if e.split("/")[-2] not in uns]
datas = [f"https://www.instagram.com/{p}/{k}/" for p, k in datas]

with open("/home/mohamed/Documents/datas/Databases/instas.txt", "w") as fl:
    fl.write("\n".join(sorted(datas)))


for f in file_doc.glob("*.json"):
    if not f.stem.startswith("scraped_istag"):
        continue
    try:
        with f.open("r", encoding="utf-8") as fl:
            data = json.load(fl)
    except Exception as err:
        print(err)
        f.unlink()
        continue

    f.unlink()
    code = data["code"]
    timestamp = data.get("taken_at")
    dt = "now"
    user = data["user"]["full_name"]
    srcs = [srcify(data)]
    if timestamp:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
            "%Y%m%d-%H%M%S"
        )
    items = data.get("carousel_media", [])
    if items:
        for item in items:
            src = srcify(item)
            srcs.append(src)

    for src in srcs:
        name = src.split("/")[-1].split("?")[0]
        name = re.sub(r"helc$", r"jpg", name)
        doc = prt / user
        doc.mkdir(parents=True, exist_ok=True)
        fn = doc / f"{code}=={dt}_{name}"
        if fn.exists():
            continue
        print(fn.stem)
        with fn.open("wb") as fl:
            r = requests.get(src, stream=True)
            fl.write(r.content)


def tojpg(img_input: Path):
    fname = img_input.with_suffix(".jpg")
    if fname.exists():
        img_input.unlink()
        print("::", img_input.name)
    image = Image.open(f"{img_input}").convert("RGB")
    image.save(f"{fname}")
    print(">>", img_input.name)
    return 1


def finalize(pp):
    nb = 1
    if nb:
        mesfiles = [(f,) for f in pp.rglob("*.webp")]
        mesfiles += [(f,) for f in pp.rglob("*.heic")]
        run_tasks(tojpg, mesfiles, 20)
        nb = len(mesfiles)
    return 1


pp = Path("/home/mohamed/.Kindas/Instagram")
finalize(pp)

for doc in pp.glob("*"):
    if doc.is_file():
        continue
    for f in doc.rglob("*"):
        if not f.is_file():
            continue
        f.rename(doc / f.name)

nb = 1
while nb:
    nb = 0
    for doc in pp.rglob("*"):
        if doc.is_file():
            continue
        if list(doc.rglob("*")):
            continue
        doc.rmdir()
        nb += 1
