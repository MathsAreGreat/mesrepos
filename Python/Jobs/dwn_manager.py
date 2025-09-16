from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime, timezone
import os
from pathlib import Path

import requests
from rich import print as rprint
from PIL import Image, ImageFile

d_today = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")

pp = "/home/mohamed/Downloads"

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


fn = Path("/home/mohamed/Downloads/code.txt")
if fn.exists():
    with fn.open("r") as e:
        data = e.read()
    with Path("/home/mohamed/Documents/datas/Databases/ugeens.txt").open("r") as e:
        datas = [el.strip() for el in e if el.strip()]
    datas = "\n".join(datas[-2:])
    with Path("/home/mohamed/Documents/datas/Databases/ugeens.txt").open("w") as e:
        e.write(f"{datas}\n{d_today}\n{data}")
    fn.unlink()

containers = ["cours", "courses", "chapters"]
for container in containers:
    fn = Path(f"/home/mohamed/Documents/datas/Docker/{container}_{d_today}.json")
    if not fn.exists():
        fn.parent.mkdir(exist_ok=True, parents=True)
        u = f"http://localhost/{container}"
        try:
            r = requests.get(u, stream=True, timeout=5)
            with fn.open("w") as e:
                json.dump(r.json(), e)
        except requests.exceptions.RequestException as req_err:
            rprint(f"Request error: {req_err}")
        except json.JSONDecodeError as json_err:
            rprint(f"JSON decoding error: {json_err}")
        except OSError as file_err:
            rprint(f"File operation error: {file_err}")

for f in Path(f"/home/mohamed/Documents/datas/Docker/").glob("*.json"):
    if f.stat().st_size < 10:
        f.unlink()


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


pp = "/home/mohamed/Downloads"

os.chdir(pp)
pp = "/home/mohamed/Documents/.Socials"
finalize(pp)
itemat = []
for f in os.listdir():
    name, *ex = f.rsplit(".", 1)
    if name.startswith("scraped_face"):
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
            if os.path.exists(fn):
                os.remove(f)
