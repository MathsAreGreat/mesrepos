import os
import html
import json
import re
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from Besites.variables import retry_on_exception


cols = ["#00ff00", "red", "green", "yellow",
        "blue", "magenta", "cyan", "white"]

sess = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": "https://ok.ru/",
}

sess.headers = headers


def run_tasks(fn, ds, nb=30):
    def your_function(args):
        return fn(*args)

    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


@retry_on_exception(1)
def check_for_datas(k):
    doc = "datas/OKRU"
    fn = f"{doc}/{k}"
    if re.search(r"[a-z]", k.lower()):
        Path(doc).mkdir(parents=True, exist_ok=True)
        Path(fn).touch()
    if Path(fn).exists():
        return None
    ok_url = f"https://ok.ru/videoembed/{k}"
    r = sess.get(ok_url)
    txt = html.unescape(r.text)
    soup = BeautifulSoup(txt, "html.parser")
    msg = soup.find(class_="vp_video_stub_txt")
    if msg:
        Path(doc).mkdir(parents=True, exist_ok=True)
        Path(fn).touch()
        return None
    return ok_url


def getUrl(k):
    ok_url = check_for_datas(k)
    if not ok_url:
        return None
    fjson = f"t{k}.json"
    cmd = f'yt-dlp "{ok_url}" --flat-playlist --skip-download --dump-json > {fjson}'
    os.system(cmd)
    print(">>", fjson, end="\r")
    try:
        with open(fjson, "r") as e:
            data = json.load(e)
    except:
        data = {}
    os.remove(fjson)
    print("X", fjson)
    if not data:
        return []
    for e in data["formats"]:
        if e.get("protocol") and e["protocol"] == "m3u8_native":
            return e["manifest_url"]
