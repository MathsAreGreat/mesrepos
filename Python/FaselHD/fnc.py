import base64
import hashlib
import json
import re
from urllib.parse import urljoin
import redis
import requests

from playwright.sync_api import sync_playwright


from pathlib import Path
from bs4 import BeautifulSoup
from Mido.variables import (
    download_m3u8_with_aria2c,
    egybest,
    monhtml,
    run_tasks,
    upclear,
)

home_path = Path("/home/mohamed/Documents/datas/FaselHD")
home_path.mkdir(parents=True, exist_ok=True)

main_url = "https://www.faselhds.life/"

rds = redis.Redis(host="localhost", port=6379, decode_responses=True)

uniques = [
    re.findall(r"[0-9]+", f.stem)[-1]
    for f in Path("/home/mohamed/Downloads/Library").rglob("*.mp4")
]

# uniques = []


def data_xsu(encoded_segment, offset):
    i = 3
    while i < 20:
        try:
            decoded = base64.b64decode(encoded_segment + "=" * i).decode("utf-8")
            extracted_number = int(re.sub(r"\D", "", decoded)) - int(offset)
            return chr(extracted_number)
        except Exception as e:
            # print(f"Error decoding segment {encoded_segment}: {e}")
            i += 1
        return None


def cryypt(url, c=100):
    if not isinstance(c, int) or c <= 0:
        return cryypt(url)
    salt = "k9f15u1t"
    while c:
        url += salt
        url = hashlib.md5(url.encode()).hexdigest()
        c -= 1
    return f"faselhd_{url}"


def save(u, nb=0):
    c = cryypt(u)
    print(f"{upclear}{u}")
    ds = rds.get(c)
    info = get_iframe(u)
    if not ds:
        ds = {}
        ds.update(info)
    else:
        ds = json.loads(ds)
        ds["src"] = info["src"]
    rds.set(c, json.dumps(ds))
    return ds


def dlink(url):
    r = requests.get(url).text
    links = list(dict.fromkeys(re.findall(r'http[^\'"]+\.m3u8', r)))
    return links


def dlink1(k, url):
    fn = Path("Files") / f"{k}.json"
    dn = Path("Files") / f"{k}s.json"
    if dn.exists():
        with fn.open("r") as fl:
            links = json.load(fl)
    else:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)  # replace with your target page

            t = page.content()
            if "Token Expired" in t:
                print("Token Expired, retrying...")
                browser.close()
                return None

            page.wait_for_selector(".hd_btn")
            buttons = page.query_selector_all(".hd_btn")
            links = [btn.get_attribute("data-url") for btn in buttons]

        with fn.open("w") as fl:
            json.dump(links, fl)

    return links


def dlinks(u):
    scp = None
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": main_url,
    }
    while not scp:
        try:
            soup = monhtml(u)
            print(u)
            scp = [
                sc.text
                for sc in soup.select("script")
                if sc and "hide_my_HTML" in sc.text
            ]
        except Exception as e:
            print(f"Error fetching links: {e}")
            continue
    txt = scp[-1].split("var hide_my_HTML")
    txt = txt[1].split("=", 1)[1].split("\n")
    *hide_my_html, offset = [e[1:-2] for e in txt if e]
    offset = re.findall(r"\)-([0-9]+)", offset)[0]
    adilbo_html_encoder_tyb = ""
    hide_my_ht = "".join(hide_my_html)
    for part in hide_my_ht.strip().split("."):
        p = data_xsu(part, offset)
        if p:
            adilbo_html_encoder_tyb += p
    soup = BeautifulSoup(adilbo_html_encoder_tyb, "html.parser")
    btn = soup.select("button.hd_btn")
    links = [a for a in btn if a.text.strip().endswith("p")]
    return sorted(links, key=lambda link: f"{link.text:>06}", reverse=True)


def get_iframe(u):
    soup = monhtml(u)
    k = soup.select_one("link[rel='shortlink']").get("href").split("=")[-1]
    t = soup.select_one("div.h3").text
    src = soup.iframe.get("src")
    return {"code": k, "title": t, "src": src}


def dwn(u, nb=1):
    c = cryypt(u)
    ds = rds.get(c)
    # if ds:
    #     info = json.loads(ds)
    #     k = info["code"]
    #     print("::", k)
    #     if k in uniques:
    #         return 0
    info = save(u, nb)
    k = info["code"]
    t = info["title"]
    link = info["src"]
    links = dlink(link)
    if not links:
        rds.delete(c)
        print(c, "Retrying...")
        return dwn(u, nb)
    for url in links:
        dist, fname = egybest(k, t, "%(height)s", "FaselHD")
        final_file = Path(dist) / f"{fname}.%(ext)s"
        if final_file.exists():
            return 1
        nb = download_m3u8_with_aria2c(url, final_file, main_url)
        if nb:
            return 1
    return nb


def save_items(u):
    soup = monhtml(u)
    links = soup.select(".postDiv a")
    wb = soup.find_all(class_="page-item")
    if wb:
        wb = wb[-1].find("a").get("href").split("/")[-1].split("?")[0]
    else:
        wb = 1
    return wb, links


def searches(*qs, s=None):
    liens = []
    i = 0
    ds = [""]
    if qs:
        ds = [f"?s={q}" for q in qs]
    r = "page"
    if s:
        r = f"{s}/page"
    for dd in ds:
        i = 0
        while True:
            u = f"{main_url}{r}/{i+1}{dd}"
            wb, links = save_items(u)
            if i < 1:
                print("This is", wb, "page(s) !")
                print("=" * len(u))
                print()
            liens += links
            i += 1
            if not links:
                break
    return liens


def saison_epz(*us):
    links = []
    for u in us:
        if not u:
            continue
        soup = monhtml(u)
        eps = soup.select(".seasonDiv")
        if not eps:
            continue
        links += [re.findall(r"[0-9]+", ep.get("onclick"))[-1] for ep in eps]

    us = [f"{main_url}?p={k}" for k in links if set(links)]
    links = []
    for u in us:
        if not u:
            continue
        soup = monhtml(u)
        eps = soup.select_one("#epAll")
        if not eps:
            continue
        eps = eps.select("a")
        if not eps:
            continue
        links += eps
    return links


def saison_eps(*us):
    links = []
    for u in us:
        if not u:
            continue
        soup = monhtml(u)
        title = soup.select_one(".h1.title").text.strip()
        seasons = soup.select(".seasonDiv")
        for s in seasons:
            link_id = re.findall(r"[0-9]+", s.get("onclick"))[-1]
            name = f"{title} {s.select_one(".title").text.strip()}"
            link = f"{main_url}?p={link_id}"
            soup = monhtml(link)
            eps = soup.select_one("#epAll")
            if not eps:
                continue
            eps = eps.select("a")
            if not eps:
                continue
            for ep in eps:
                links.append(ep)
                ep_url = ep.get("href")
                ep_id = cryypt(ep_url)
                print(">>", ep_id)
                if rds.get(ep_id):
                    continue
                info = get_iframe(ep_url)
                info["title"] = f"{name} {ep.text.strip()}"
                rds.set(ep_id, json.dumps(info))
    return links


def tolink(us=[], urls=[]):
    links = []
    liens = saison_eps(*us)
    links += [link.get("href") for link in liens]
    links += urls
    return [urljoin(main_url, link) for link in set(links)]


def saved(qs=[], us=[], urls=[]):
    links = tolink(qs, us, urls)
    print(len(links), "links here !")
    return run_tasks(save, links)


if __name__ == "__main__":
    links = []
    import time

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://ok.ru/profile/910127230771/video")
        page.wait_for_selector(".video-card_n.ellip")
        buttons = page.query_selector_all(".video-card_n.ellip")
        links += [btn.get_attribute("href").split("video/")[-1] for btn in buttons]
        time.sleep(10)

    print(links)
