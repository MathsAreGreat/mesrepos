import hashlib
import json
import re
from pathlib import Path

import cloudscraper
import requests
from mesvariables import DOM
from Mido.variables import download_m3u8_with_aria2c, egybest
from numpy import base_repr

# "spis16t3 bot 1.0"

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

scraper = cloudscraper.create_scraper()

sess = requests.Session()
sess.headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": DOM,
}


def dwn(u, nb=0):
    p = Path("/home/mohamed/Downloads/Library")
    if not u.startswith("http"):
        c = u
        dd = get_links("", c, 1)
    else:
        c = cryypt(u)
        for _ in p.rglob(f"*{c}).mp4"):
            return 0
        dd = egy_links(u) if nb else fetch(u, 1)
    if not dd:
        return 0
    c, name, link = dd
    doc, titre = egybest(c, name, "1080hd", "Shahid4u")
    titre = titre.replace("1080hd", "%(height)s")
    fname = Path(f"{doc}/{titre}.%(ext)s")
    download_m3u8_with_aria2c(link, fname)
    return doc


def cryypt(url, c=100):
    if not isinstance(c, int) or c <= 0:
        return cryypt(url)
    salt = "k9f15u1t"
    *_, url = [e for e in url.split("/") if e]
    while c:
        url += salt
        url = hashlib.md5(url.encode()).hexdigest()
        c -= 1
    return url


def eps(u):
    r = scraper.get(u)
    us = re.findall(r"href=\"(http[^\"']+/watch/[^\"']+)", r.text)
    return us[::-1]


def fetch(u, nb):
    return get_links(u, cryypt(u), nb)


def egy_links(url):
    r = sess.get(url)
    us = re.findall(r"<titl[^>]+>([^\-<]+)", r.text)
    name = us[0]
    us = re.findall(r"http[^\"';]+m3u8\?*[^\\\"';]*", r.text)
    if not us:
        return None
    link = us[0]
    return name, link


def decode_string(p, a, c, k, *el):
    d = el[-1]

    def e_func(c):
        return (e_func(c // a) if c >= a else "") + (
            chr(c + 29) if (c := c % a) > 35 else base_repr(c, 36).lower()
        )

    while c > 0:
        c -= 1
        d[e_func(c)] = k[c] or e_func(c)

    p = re.sub(r"\b\w+\b", lambda m: d.get(m.group(0), ""), p)

    return p


def urlize(url):
    sess.headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }
    try:
        r = sess.get(url, timeout=5)
        if "|m3u8" not in r.text and "|mp4" not in r.text:
            return None
        nb = re.findall(r"\|([0-9]+0)p\|", r.text)
        if not nb:
            return None
        nb = int(nb[0])
        tt = r.text.replace("\\'", "<&>")
        datas = tt.split("'")
        ind = datas.index(".split(")
        exp, tnb, wst = datas[ind - 3 : ind]
        tnb = [int(e) for e in tnb.split(",") if e.strip()]
        r = decode_string(
            exp.replace("<&>", "'"), *tnb, wst.replace("<&>", "'").split("|"), 0, {}
        )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        print("Timeout")
        return None
    return nb, r


def dep_links(u, text):
    c = cryypt(u)
    fn = Path(f"/home/mohamed/Documents/datas/Shahid/{c}.json")
    if not fn.exists():
        us = re.findall(r"<titl[^>]+>([^\-<]+)", text)
        name = us[0]
        us = re.findall(r"JSON.parse\('([^;]+)", text)
        lien = us[0]
        links = [
            link.replace("\\", "") for link in re.findall(r"\"(http[^\"]+)\"", lien)
        ]
        with fn.open("w") as f:
            json.dump([name, *links], f)


def get_links(u, c, nb):
    if nb < 1:
        return None
    fn = Path(f"/home/mohamed/Documents/datas/Shahid/{c}.json")
    fn.parent.mkdir(parents=True, exist_ok=True)
    print("#", u)
    if not fn.exists():
        scraper = cloudscraper.create_scraper()
        r = scraper.get(u)
        text = r.text
        us = re.findall(r"<titl[^>]+>([^<]+) -", text)
        name = us[0]
        us = re.findall(r"JSON.parse\('([^;]+)", text)
        lien = us[0]
        links = [
            link.replace("\\", "") for link in re.findall(r"\"(http[^\"]+)\"", lien)
        ]
        vn = Path(f"/home/mohamed/Documents/datas/Backups/{c}")
        if not links:
            vn.touch()
            return None

        lesdatas = []
        for url in links:
            print(">>", url)
            dd = get_link(url)
            if dd:
                nb, link = dd
                lesdatas.append((nb, url, link))
        _, url, link = max(lesdatas, key=lambda x: x[0])
        with fn.open("w") as f:
            json.dump([name, url], f)
    else:
        with fn.open("r") as f:
            datas = json.load(f)
        name, url = datas
        nb, link = get_link(url)
    print("Chosen :", url, "|", nb)
    return c, name, link


def get_link(url):
    dd = urlize(url)
    if not dd:
        return None
    nb, r = dd
    us = re.findall(r"http[^\"]+m3u8[^\"]*", r)
    if us:
        link = us[0]
        return nb, link
    return None


if __name__ == "__main__":
    u = "https://vidbam.org/embed-hksxo6237s9d.html"
    r = urlize(u)
    print(r)
