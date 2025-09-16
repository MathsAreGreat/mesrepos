import requests
import os
from pathlib import Path
from tqdm.auto import tqdm
from random import choice
from bs4 import BeautifulSoup

cols = ["#00ff00", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN"]
os.makedirs("/home/mohamed/Documents/Livre2", exist_ok=True)
os.chdir("/home/mohamed/Documents/Livre2")


def monhtml(r):
    sess = requests.Session()
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }
    r = sess.get(r)
    return BeautifulSoup(r.text, 'html.parser')


keys = {
    "": ["Arabic", 2],
    "f": ["Français", 21],
    "e": ["Anglais", 2],
}


def fetch(t=""):
    doc, nb = keys[t]
    links = []
    for i in range(200):
        u = f"http://livre{nb}.com/p{t}{i}.html"
        soup = monhtml(u)
        links += [
            f'http://livre{nb}.com/{a["href"].strip()}'
            for a in soup.findAll("a", href=True)
            if a['href'].endswith('.pdf')
        ]
    return [
        (doc, e)
        for e in set(links)
        if not os.path.exists(doc+"/"+e.split('/')[-1])
    ]


def vid_download(dd):
    doc, url = dd
    name = url.split('/')[-1]
    sess = requests.Session()
    p_file = f"{doc}/{name}"
    if os.path.exists(p_file):
        return 0
    p_file = f"{doc}/{name}.part"
    os.makedirs(doc, exist_ok=True)
    path = Path(p_file)
    try:
        sz = path.stat().st_size
    except:
        sz = 0
    sess.headers = {
        "Range": f"bytes={sz}-",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }
    response = sess.get(url, stream=True, timeout=100)
    total_size_in_bytes = int(response.headers.get("content-length", 0))

    if total_size_in_bytes < 10000:
        print("** file :", name)
        return None
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(
        total=total_size_in_bytes,
        leave=False,
        colour=choice(cols),
        unit="iB",
        unit_scale=True,
        desc=f"{name} ",
    )
    with open(p_file, "ab") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("Error :", name)
        return 0
    name = p_file.replace('.part', '')
    os.rename(p_file, name)
    print("", end=name)
    return 1
