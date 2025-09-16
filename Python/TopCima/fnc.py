import hashlib
import json
import re
import os
from pathlib import Path
from urllib.parse import urljoin

import redis
import requests
from Mido.variables import (
    aria_dwn,
    egybest,
    get_m3u8,
    monhtml,
    download_m3u8_with_aria2c,
    upclear,
    run_tasks,
)

DOWN = "/home/mohamed/Downloads"

parent = Path(f"{DOWN}/Library")

parent.mkdir(parents=True, exist_ok=True)

rds = redis.Redis(host="localhost", port=6379, decode_responses=True)

backup_key = "topcima:backups"
datas_key = "topcima:datas"

sess = requests.session()
sess.headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}

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


def getlink(lien):
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
    infos = []
    for k in info:
        try:
            infos.append((k["label"].split(" ")[0].lower().zfill(6), k["file"]))
        except requests.exceptions.RequestException as e:  # noqa: PERF203
            print(f"Failed to fetch {k['file']}: {e}")
    if not infos:
        print("No working value")
        return None
    dd = max(infos)
    return link, *dd


def urlize(links):
    if not links:
        return None
    for link in links:
        if dd := getlink(link):
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


def get_file(u: str, skip: bool = False) -> int:
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

    fname = cryypt(key)
    ds = rds.get(fname)
    if not ds:
        refs = u.split("/")[:3]
        ref = "/".join(refs)
        headers = sess.headers
        headers["Referer"] = ref
        soup = monhtml(u, headers=headers)
        key = soup.find(id="shortlink")["value"].split("=")[-1]
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
        ds = [key, title, links]
        rds.set(fname, json.dumps(ds))
        print(f"- adding data to {pu}")
    else:
        print(f"- retreiving data of {pu}")
        ds = json.loads(ds)
    key, title, links = ds
    print(egybest(key, title, "1080", "TopCima")[-1])
    if skip:
        rds.sadd(backup_key, key)
    if rds.sismember(backup_key, key):
        rds.sadd(datas_key, u)
        return 0
    dd = urlize(links)
    if not dd:
        rds.sadd(backup_key, key)
        rds.sadd(datas_key, u)
        return 0
    ref, h, link = dd
    fhd = re.sub(r"^0+", r"", h)
    fhd = re.sub(r"^[^0-9]+$", r"1080p", fhd)
    fhd = re.sub(r"[^0-9]", r"", fhd)
    dirc, name = egybest(key, title, fhd, "TopCima")
    dt = ref, dirc, link, f"{name}.mp4"
    if aria_dwn(*dt):
        os.system("clear")
        return 1
    return 0


def db_update(nb=0):
    for f in Path("Library").rglob("*.mp4"):
        parts = f.parts
        fn = Path(DOWN, *parts)
        fn.parent.mkdir(parents=True, exist_ok=True)
        print("Moving !", f.stem)
        f.rename(fn)

    for f in parent.rglob("*).mp4"):
        k = f.stem.split(".")[-1][1:-1]
        rds.sadd(backup_key, k)

    eps = []
    liens = [e for e in rds.smembers("topcima:links") if e]
    if nb:
        datas = run_tasks(refresh_page, [(i + 1,) for i in range(nb)])
        eps = [ep for links in datas for ep in links if ep not in liens]

    if not eps:
        return 0

    links = eps + [e for e in rds.smembers("topcima:links") if e]
    rds.delete("topcima:links")
    rds.sadd("topcima:links", *set(links))
    return 1


def refresh_page(nb=1):
    u = f"https://web6.topcinema.cam/recent/page/{nb}/"
    print("> Freaching", u)
    soup = monhtml(u)
    return [link.get("href") for link in soup.select(".Small--Box > a")]


def refresh_database():
    links = [e for e in rds.smembers("topcima:links") if e]
    us = rds.smembers("topcima:tvs")
    for u in sorted(us, reverse=True):
        if "http" not in u:
            continue
        soup = monhtml(f"{u}list/")
        series = [
            urljoin(u, link["href"]) for link in soup.select(".Season a", href=True)
        ]
        rds.sadd("topcima:series", *series)
    rds.delete("topcima:tvs")
    us = rds.smembers("topcima:series")
    if len(us) > len(set(us)):
        rds.delete("topcima:series")
        rds.sadd("topcima:series", *set(us))
    for u in sorted(set(us), reverse=True):
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
    links = [k for k in dict.fromkeys(links)]
    rds.delete("topcima:links")
    rds.sadd("topcima:links", *links)
    return links[::-1]


def format(url):
    return "-".join(
        e if re.findall(r"[^0-9]", e) else e.zfill(3)
        for e in url.split("/")[-2].split("-")
    )


def get_links(*fs, bol=False):
    links = [
        u for u in rds.smembers("topcima:links") if not rds.sismember(datas_key, u)
    ]
    liens = []
    for f in set(fs):
        if f == "":
            continue
        liens += [url for url in links if f in url]
    links = [(u, bol) for u in sorted(set(liens), key=format)]
    return run_tasks(get_file, links)


if __name__ == "__main__":
    u = "https://vidtube.pro/embed-c9rd1eglym48.html"
    p = get_m3u8(u)
    us = [
        urljoin(u, e) for e in re.findall(r"[^\"']+", p) if ".m3u8" in e or ".mp4" in e
    ]
    aria_dwn(u, "/home/mohamed/Videos", us[0], "vid1.mp4")
    print(p)
