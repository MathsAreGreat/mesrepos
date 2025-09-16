import os
from urllib.parse import urljoin

import requests
from Mido.variables import aria_dwn, monhtml, run_tasks

main_url = "https://server6.mp3quran.net/"


def dwn(u):
    *_, d, f = u.split("/")
    fn = f"/home/mohamed/Music/Quran/{d}/{f}"
    if os.path.exists(fn):
        return 0
    os.makedirs(f"/home/mohamed/Music/Quran/{d}", exist_ok=True)
    r = requests.get(u, stream=True)
    with open(fn, "wb") as fl:
        fl.write(r.content)
    return 1


def choose_moqri(link):
    lien = link.get("href")
    if not lien:
        return None
    if lien.endswith("php"):
        return None
    url = urljoin(main_url, f"/{lien}")
    print(url)

    soup = monhtml(url, headers=headers)

    links = [(url, e) for e in soup.find_all("a")[1:]]

    datas = run_tasks(collect, links, 20)

    return [e for e in datas if e]


def collect(url, link):
    link = link.get("href")
    if not link:
        return None
    if not link.startswith(("0", "1")):
        return None
    lien = urljoin(url, link)
    *_, d, f = lien.split("/")
    fn = f"/home/mohamed/Music/Quran/{d}/{f}"
    if os.path.exists(fn):
        return None
    dd = (url, f"/home/mohamed/Music/Quran/{d}", lien, f)
    return dd


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Referer": main_url,
}

links = []
sp = monhtml(main_url, headers=headers)
for mlink in sp.find_all("a")[1:]:
    liens = choose_moqri(mlink)
    if not liens:
        continue
    links += liens


run_tasks(aria_dwn, links, 20)
