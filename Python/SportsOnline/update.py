import re
import requests
import json
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor

sess = requests.Session()
os.chdir("/home/mohamed/Documents/datas/PrimaSport")


def basic(u, ref):
    sess.headers = {
        "referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    match = re.search(r"return\((\[.+?\])", sess.get(u).text)
    if not match:
        return None
    url = "".join(json.loads(match[1]))
    return u, url.replace("////", "//")


def monhtml(k, ref):
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }
    r = sess.get(k)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"  # or lxml or html5lib
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def stream(nbr):
    u = f"https://antenasport.store/stream{nbr}.php"
    ref = "/".join(u.split("/")[:3])
    soup = monhtml(u, ref)
    iframe = soup.iframe
    while iframe:
        ref = "/".join(u.split("/")[:3])
        u = iframe["src"]
        soup = monhtml(u, ref)
        iframe = soup.iframe
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }
    r = sess.get(u)
    us = re.findall(r'http[^\'"]+m3u8', r.text)
    if not us:
        return 0
    ref = u.rsplit("=", 1)[0]
    f, l = us[0].split(f"premium{nbr}")
    return ref, f, l


def lienize(nbr):
    u = f"https://antenasport.store/{nbr}.php"
    ref = "/".join(u.split("/")[:3])
    soup = monhtml(u, ref)
    iframe = soup.iframe
    title = soup.title.text.split("-", 1)[-1].strip()
    while iframe:
        ref = "/".join(u.split("/")[:3])
        u = iframe["src"]
        soup = monhtml(u, ref)
        iframe = soup.iframe
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }
    ref = u
    r = sess.get(u)
    us = re.findall(r'http[^\'"]+m3u8', r.text)
    if us:
        url = us[0]
        # sess.headers = {
        #     "referer": ref,
        #     "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        # }
        # link = sess.get(u, allow_redirects=True).url
        # link = link.rsplit('/', 1)[0]
        # url = f"{link}/tracks-v1a1/mono.m3u8"
    else:
        ref, url = basic(u, ref)
    info = {
        "r": ref,
        "u": url,
        "t": title,
    }
    with open(f"{nbr}.json", "w") as e:
        json.dump(info, e)
    print(">>", nbr)
    return 1


u = "https://antenasport.store"
soup = monhtml(u, u)
links = [
    e["href"][1:].split(".")[0]
    for e in soup.findAll("a", href=True)
    if e["href"].endswith(".php") and "stream" not in e["href"]
]
print(">>", len(links), "items !")

with ThreadPoolExecutor(20) as executor:
    executor.map(lienize, links)

datas = [f"stream{i}" for i in range(10, 700) if f"stream{i}" not in links]
datas = [e for e in datas if not os.path.exists(f"{e}.json")]
print(">>", len(datas), "items !")
with ThreadPoolExecutor(50) as executor:
    executor.map(lienize, datas)

infos = {}
aytres = {}
for f in os.listdir():
    k = f.split(".")[0]
    with open(f, "r") as e:
        data = json.load(e)
    u = data["u"]
    if "premium" in u:
        infos[k] = data
    else:
        aytres[k] = data

with open("/home/mohamed/Documents/Projects/Python/PrimaSport/all.json", "w") as e:
    json.dump(infos, e)
with open("/home/mohamed/Documents/Projects/Python/PrimaSport/autres.json", "w") as e:
    json.dump(aytres, e)
