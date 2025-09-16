import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from Mido.variables import aria_dwn, egybest, get_m3u8, monhtml, upclear, run_tasks

DOWN = "/home/mohamed/Downloads"

parent = Path(f"{DOWN}/Library")

parent.mkdir(parents=True, exist_ok=True)


uns = [f.stem.split(".")[-1][1:-1] for f in parent.rglob("*.mp4")]

sess = requests.session()
sess.headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}

with Path("infos.json").open("r") as fl:
    top_infos = json.load(fl)

cols = ["#00ff00", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN"]

seasons = {
    "الاول": "01",
    "الثاني": "02",
    "الثالث": "03",
    "الرابع": "04",
    "الخامس": "05",
    "السادس": "06",
    "السابع": "07",
    "الثامن": "08",
    "التاسع": "09",
    "العاشر": "10",
}


def getlink(lien, nb=-1):
    us = lien.split("/")
    dom = us[2]
    key = us[-1].split(".")[0]
    link = f"https://{dom}/embed-{key}.html"
    print(link)
    r = get_m3u8(link)
    if not r:
        print("No value")
        return None
    if "label" not in r:
        dd = re.findall(r'file:"([^"]+)".+height:([^,]+)', r)
        info = [{"file": url, "label": f"{hd}p"} for url, hd in dd]
    else:
        dd = re.findall(r"\[[^\]]+\]", r)[0].split("{file", 1)[-1].replace("'", '"')
        dd = "[{file" + dd
        dd = re.sub(r"([\{,])([0-9a-z]+):", r'\1"\2":', dd)
        info = json.loads(dd)
    sess.headers["Referer"] = link
    infos = {}
    for k in info:
        infos[k["label"].split(" ")[0].lower().zfill(6)] = k["file"]
    key = sorted(infos)[nb]
    dd = key, infos[key]
    return link, *dd


def urlize(links, nb=-1):
    if not links:
        return None
    for link in links:
        if dd := getlink(link, nb):
            return dd
    return None


def cryypt(url, c=100):
    if not isinstance(c, int) or c <= 0:
        return cryypt(url)
    salt = "k9f15u1t"
    while c:
        url += salt
        url = hashlib.md5(url.encode()).hexdigest()
        c -= 1
    return f"topcima_{url}"


def get_file(u):
    if "-" not in u:
        return 0
    pu = "-".join(e for e in u.split("/")[-2].split("-") if "%" not in e)
    print("Fetching :", pu)
    ks = [e for e in u.split("/") if "-" in e][-1].split("-")
    key = "-".join(
        re.sub(r"[^0-9a-z]", r"", e, flags=re.IGNORECASE)
        for e in ks
        if re.search(r"[0-9a-z]", e, flags=re.IGNORECASE)
    )
    print(upclear * 2, end="")

    print("::", pu)

    ds = None
    if not ds:
        refs = u.split("/")[:3]
        ref = "/".join(refs)
        headers = sess.headers
        headers["Referer"] = ref
        soup = monhtml(u, headers=headers)
        key = soup.find(id="shortlink")["value"].split("=")[-1]
        if key in uns:
            return 0
        title = soup.find_all("h1")[-1].text.strip()
        url = soup.find("a", class_="download").get("href")

        ref = "/".join(url.split("/")[:3])
        headers = sess.headers
        headers["Referer"] = ref
        soup = monhtml(url, headers=headers)
        links = [
            link.get("href")
            for link in soup.select("a.downloadsLink.green")
            if link.get("href")
        ]
        print(f"- adding data to {pu}")
    dd = urlize(links)
    if not dd:
        return 0
    ref, h, link = dd
    fhd = re.sub(r"^0+", r"", h)
    fhd = re.sub(r"^[^0-9]+$", r"1080p", fhd)
    fhd = re.sub(r"[^0-9]", r"", fhd)
    dirc, name = egybest(key, title, fhd, "TopCima")
    dt = ref, dirc, link, f"{name}.mp4"
    if aria_dwn(*dt):
        print(upclear * 2, end="")
        return 1
    return 0


def refresh_database():
    links = top_infos["episodes"]
    seasons = top_infos["seasons"]
    us = top_infos["series"]
    for u in sorted(us, reverse=True):
        if "http" not in u:
            continue
        soup = monhtml(f"{u}list/")
        seasons += [
            urljoin(u, link["href"]) for link in soup.select(".Season a", href=True)
        ]
    top_infos["series"] = list(dict.fromkeys(us))
    for u in dict.fromkeys(seasons):
        if "http" not in u:
            continue
        soup = monhtml(u)
        row = soup.find(class_="row")
        links += [urljoin(u, link["href"]) for link in row.find_all("a", href=True)]
        p = soup.find(class_="watch")
        su = "-".join(e for e in u.split("/")[-2].split("-") if "%" not in e)
        print(su, " " * 50, end="\r")
        if not p:
            continue
        url = urljoin(u, p.get("href"))
        soup = monhtml(url)
        links += [
            urljoin(u, link["href"])
            for link in soup.find_all("a", class_="recent--block", href=True)
        ]
    top_infos["episodes"] = list(dict.fromkeys(links))[::-1]
    links = top_infos["movies"]
    top_infos["movies"] = list(dict.fromkeys(links))
    with Path("infos.json").open("w") as fl:
        json.dump(top_infos, fl, indent=2)
    return top_infos["movies"] + top_infos["episodes"]


links = [(e,) for e in refresh_database()]
run_tasks(get_file, links, 15)
