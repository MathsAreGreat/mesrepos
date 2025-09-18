from datetime import datetime
import json
import re
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()
DATA_FILE = "seen_links.json"

# Load seen links
seen_links = []


def monhtml(u):
    sess = requests.session()
    r = sess.get(u)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/get_datas")
def get_videos():
    global seen_links  # <- tell Python this is the module-level variable
    url = "https://api.dailymotion.com/user/ahaspoorts/videos?limit=20&fields=title,id,thumbnail_url"
    r = requests.get(url)
    rjson = r.json()
    datas = [e for e in rjson["list"] if e["id"] not in seen_links]
    seen_links += [e["id"] for e in datas]
    return {"datas": datas}


@app.get("/get_salat")
def get_pray():
    url = "https://app.muslimpro.com/prayer-times/morocco/taroudant?lat=30.4727126&lng=-8.8748765&alt=236.82470703125&country_code=MA"
    soup = monhtml(url)
    rjson = json.loads(soup.find(id="prayer-times-jsonld").text)
    salawat = rjson["itemListElement"]
    ps = [
        e.text
        for e in soup.select("p.font-rethink")
        if re.search(r" 20[0-9]{2}.+14[0-9]{2}", e.text)
    ]
    mil, hij = [e.strip() for e in max(ps).split("|")]
    infos = {"miladi": mil, "hijri": hij}
    for s in salawat:
        infos[s["name"]] = datetime.strptime(
            s["startDate"].split("+")[0], "%Y-%m-%dT%H:%M:%S"
        ).strftime("%H:%M")
    return infos
