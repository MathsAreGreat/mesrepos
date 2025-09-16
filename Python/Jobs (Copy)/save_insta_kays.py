import base64
import json
import os
import re
from glob import glob
from pathlib import Path

import requests
from bs4 import BeautifulSoup

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
        decoded = base64.b64decode(encoded_segment + '===').decode('utf-8')
        extracted_number = int(re.sub(r'\D', '', decoded)) - int(offset)
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
for f in glob("/home/mohamed/Documents/.Socials/Instagram/**", recursive=True):
    if os.path.isfile(f):
        k = f.split("/")[-1].split(".")[0]
        f_uniques.append(k)


for f in glob("/home/mohamed/Downloads/d_scrape_userinst*json"):
    with open(f, "r", encoding="utf-8") as e:
        datas = json.load(e)
    ii += 1
    instuns += [d for d in datas if "instagram.com" in d]
    os.remove(f)

instuns = [re.findall(r"[^/]+", d)[-1] for d in instuns]
instos = [e for e in set(instuns) if e not in f_uniques and len(e) > 10]
if len(instos) < len(instuns):
    with open(fvm, "w") as e:
        json.dump(instos, e, indent=2)


for f in glob("/home/mohamed/Downloads/scraped_insta*json"):
    try:
        with open(f, "r", encoding="utf-8") as e:
            data = json.load(e)
        fl = f.split("/")[-1]
        os.rename(f, f"/home/mohamed/Documents/Files/.Instagram/{fl}")
        data = [re.findall(r"[^/]+", e)[-1] for e in set(data)]
        dataz = [e for e in data if e not in datas]
        if dataz:
            datas += dataz
            with open(fnm, "w") as e:
                json.dump(datas, e)
        print(len(data), "items !", "=" * 20, end="\r")
    except Exception as err:
        print(err)

datas = [e for e in set(datas) if e not in uniques]
with open(fnm, "w") as e:
    json.dump(datas, e, indent=2)

fnm = "/home/mohamed/Documents/datas/FaselHD/Datas"

infos = {}
for f in glob("/home/mohamed/Downloads/scrapedF*json"):
    ID = f.split("_")[1]
    if ID not in infos:
        infos[ID] = {}
    with open(f, "r", encoding="utf-8") as e:
        data = json.load(e)
    infos[ID].update(data)
    v = infos[ID]
    if "titre" in v and "1080p" in v:
        with open(f"{fnm}/{ID}.json", "w") as e:
            json.dump(v, e)

for f in glob("/home/mohamed/Downloads/scrapedF*json"):
    ID = f.split("_")[1]
    fn = f"{fnm}/{ID}.json"
    if os.path.exists(fn):
        os.remove(f)

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

    hide_my_HTML_myH = ''.join(hide_my_HTML)

    for part in hide_my_HTML_myH.strip().split('.'):
        p = data_XsU(part, offset)
        if p:
            adilbo_HTML_encoder_tYb += p
    soup = BeautifulSoup(adilbo_HTML_encoder_tYb, 'html.parser')

    f = dt_doc / f"{k}.json"
    with open(f, "w") as e:
        json.dump(
            {
                el.text.strip(): el["data-url"]
                for el in soup.find_all("button", class_="hd_btn")
                if el.text.strip().endswith("p")
            },
            e
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
        json.dump({k if k.endswith("p") else "144p": v for k,
                  v in videos.items()}, e)
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
    ts = re.sub(r"[^a-z0-9]", r" ", data["title"],
                flags=re.IGNORECASE).split(" ")
    title = ".".join(e for e in ts if e)
    if gr == "Movies":
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
        seasons = [re.findall(r"[0-9]+", s)[-1] for s in data["seasons"]]
        ss = ""
        sn = ""
        if data["ss"]:
            ss = data["ss"].replace("موسم ", "").strip().zfill(2)
        if data["sn"]:
            sn = re.findall(r"[0-9]+", data["sn"])[-1]
        ep = data["ep"].replace("الحلقة ", "").strip().zfill(2)
        u = data["u"]

        info = {
            "t": title,
            "ss": ss,
            "sns": seasons,
            "poster": poster,
            "eps": data["episodes"],
            "gr": gr
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
