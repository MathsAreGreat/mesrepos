import os
from pathlib import Path
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
import requests
import re
from concurrent.futures import ThreadPoolExecutor

sess = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    # "Referer": "https://ok.ru/",
}


def run_tasks(fn, ds, nb=5):
    def your_function(args):
        return fn(*args)

    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


def monhtml(r, data=None):
    if data:
        r = sess.post(r, data=data)
    else:
        r = sess.get(r)
    encoding = (
        r.encoding if "charset" in r.headers.get(
            "content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def lrcify(u, ar, tt):
    print(">", ar, "-", tt, " " * 20, end="\r")
    doc = Path(f"/home/mohamed/Documents/datas/LRCBand/{ar}")
    doc.mkdir(parents=True, exist_ok=True)
    fn = doc / f"{tt}.lrc"
    if os.path.exists(fn):
        return 0
    soup = monhtml(u)
    c = soup.find(id="lrc_text").decode_contents()
    lines = re.split("<br[^>]+>", c)
    lyrics = "\n".join(lines)
    with open(fn, "w", encoding="utf-8") as fl:
        fl.write(lyrics)
    return 1


u = "https://rclyricsband.com"


def lrc_ar(n):
    ar = unquote(n).strip().title()
    u = f"https://rclyricsband.com/artist?ar={ar}"
    soup = monhtml(u)
    links = [
        (urljoin(u, li.find("a")["href"]), ar, li.find("a").text.strip())
        for li in soup.find_all("li", class_="singers_list")
    ]
    run_tasks(lrcify, links)


soup = monhtml(u, data={"search": "yemchi"})
links = [
    (li.find("a")["href"], li.find("a").text)
    for li in soup.find_all("li", class_="list_results")
]

arts = [
    link.split("=")[-1]
    for link, _ in links
    if "#" not in link and link.startswith("artist")
]

arts = sorted(set(arts))
print(len(arts), "Artists !")
for i, n in enumerate(arts, start=1):
    print(i, ":", n, "=================================")
    lrc_ar(n)
