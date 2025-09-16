import requests
import os
import sys
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
referrer = "https://play-1.reyada-365.com/"
doom = "https://www.kooora4live.ai"


def bsin(text):
    return BeautifulSoup(text, "html.parser")


def monhtml(r):
    sess = requests.session()
    sess.headers = {"referer": r, "User-Agent": agent}
    rs = sess.get(r, allow_redirects=True)
    txt = rs.text
    return bsin(txt)


def koora():
    soup = monhtml(doom)
    infos = []
    divs = soup.findAll(attrs={"class": "match-container"})
    i = 1
    for div in divs:
        link = div.find("a")["href"]
        nb = len(link.split("/"))
        if nb < 5:
            continue
        ts = " VS ".join(
            t.text.strip() for t in div.findAll(attrs={"class": "team-name"})
        )
        infos.append(link)
        print(">", i, ":", ts)
        i += 1
    nb = int(input("Enter your chosen match : ")) - 1
    return infos[nb]


def basic(url):
    ns = url.split("/")
    if re.search(r"[^0-9]", ns[4]):
        u = url + "?serv=0"
    else:
        ns[3] = "embed"
        u = "/".join(ns[:5])
    print(u)
    sess = requests.session()
    sess.headers["Referer"] = u
    r = sess.get(u)
    html = r.text
    base_url = re.findall(r"url = ([^;]+)", html)[0]
    kk = re.findall(r"key[0-9]+", html)[0]
    ref = re.findall(r"http.+token.php", html)[0]
    return ref, base_url.replace("'", ""), kk


def choose(streamUrl, ch, key):
    sess = requests.session()
    referrer = streamUrl.rsplit("/", 1)[0]
    sess.headers = {"Referer": referrer}
    streamUrl = sess.post(streamUrl, data={"ch": ch, "key": key})
    streamUrl = streamUrl.json()
    streamUrl = unquote(re.sub(r"(.{1,2})", r"%\1", streamUrl["url"]))
    return referrer, streamUrl


def liveit(referrer, ch, key):
    referrer, url = choose(referrer, ch, key)
    print(f"> {ch=}")
    print(f"> {key=}")
    print(f"> {url=}")
    print(f"> {referrer=}")
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    http = f'--http-referrer="{referrer}"'
    setting = f'--http-user-agent="{agent}" --adaptive-use-access'
    cmd = f"""vlc --loop --play-and-exit "{url}" {http} {setting}"""
    os.system(cmd)


def livenow():
    url = koora()
    while True:
        print("livenow")
        ref, ch, key = basic(url)
        liveit(ref, ch, key)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _, c, k = sys.argv
        ch = f"bein{c:>02}"
        if re.search(r"[a-z]", c):
            ch = c
        key = f"key{k:>03}"
        doom = "https://t1.360kora.io"
        doom = "https://4k.kooora4lives.net"
        liveit(f"{doom}/token.php", ch, key)
    else:
        livenow()
