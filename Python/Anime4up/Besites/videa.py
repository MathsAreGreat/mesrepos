import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from random import choice

import requests
from tqdm.auto import tqdm
from Besites.variables import retry_on_exception

cols = ["#00ff00", "red", "green", "yellow",
        "blue", "magenta", "cyan", "white"]

sess = requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": "https://videa.hu/",
}

sess.headers = headers


def run_tasks(fn, ds, nb=20):
    def your_function(args):
        return fn(*args)

    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


def goo(eps):
    episodes = [(k, t, n) for t, n, k in eps]
    run_tasks(vid_dwn, episodes, 5)


@retry_on_exception(1)
def vid_dwn(k, t, n):
    url = get_datas(k)
    t = t.title()
    doc = f"Library/MixAnimes/Seasons/{t}"
    tn = f"{t} E{n}"
    tn = tn.replace(" ", ".")
    fn = f"{doc}/{tn}.mp4"
    if os.path.exists(fn):
        return None
    os.makedirs(doc, exist_ok=True)
    p_file = f"{doc}/{tn}.mp4.part"
    try:
        sz = os.stat(p_file).st_size
    except Exception as err:
        print("vid_dwn :", err)
        sz = 0
    sess = requests.session()
    sess.headers = {
        "Referer": "https://videa.hu/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Range": f"bytes={sz}-",
    }

    os.makedirs(doc, exist_ok=True)
    response = sess.get(url, stream=True, timeout=100)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(
        total=total_size_in_bytes,
        unit="iB",
        unit_scale=True,
        leave=False,
        desc=f"{tn} ",
        colour=choice(cols),
    )
    with open(p_file, "ab") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        return 0
    os.rename(p_file, fn)
    return 1


@retry_on_exception(1)
def check_for_datas(k):
    doc = Path("datas/Videa")
    fn = doc / k
    if Path(fn).exists():
        return None
    ok_url = f"https://videa.hu/player?v={k}"
    r = sess.get(ok_url)
    if k not in r.text:
        Path(doc).mkdir(parents=True, exist_ok=True)
        Path(fn).touch()
        return None
    return ok_url


def get_datas(k):
    ok_url = check_for_datas(k)
    if not ok_url:
        return None
    fjson = f"t{k}.json"
    cmd = f'yt-dlp "{ok_url}" --flat-playlist --skip-download --dump-json > {fjson}'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(">>", fjson, end="\r")
        with open(fjson, "r") as e:
            data = json.load(e)
        Path(fjson).unlink()
        print("X", fjson, " " * 5)
    except Exception as err:
        print("get_datas :", err)
        data = {}
    if not data:
        doc = Path("datas/Videa")
        Path(doc).mkdir(parents=True, exist_ok=True)
        fn = doc / k
        fn.touch()
        return None
    return data["url"]


@retry_on_exception(1)
def contenu(k):
    u = get_datas(k)
    if not u:
        return 0
    try:
        sess.headers = headers
        r = sess.get(u, stream=True, timeout=10)
        c = int(r.headers.get("content-length", 0))
        print(f"> {c} bytes", end="\r")
        return (c // 1000) / 1000
    except Exception as err:
        print(err)
        return contenu(k)
