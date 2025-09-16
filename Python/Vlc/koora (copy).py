import os
import re
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
referrer = "https://play-1.reyada-365.com/"


def bsin(text):
    return BeautifulSoup(text, "html.parser")


def monhtml(r):
    sess = requests.session()
    rs = sess.get(r)
    txt = rs.text
    return bsin(txt)


def koora():
    u = "https://kooora4lives.io/"
    soup = monhtml(u)
    infos = []
    divs = soup.findAll(attrs={"class": "match-container"})
    i = 1
    for div in divs:
        link = div.find("a")["href"]
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
    sess.headers["referer"] = u
    r = sess.get(u)
    html = r.text
    base_url = re.findall(r"url = ([^;]+)", html)[0]
    kk = re.findall(r"key[0-9]+", html)[0]
    return base_url.replace("'", ""), kk


def choose(referrer, ch, key):
    sess = requests.session()
    sess.headers = {
        "referer": referrer,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    streamUrl = f"{referrer}/token.php"
    streamUrl = sess.post(streamUrl, data={"ch": ch, "key": key})
    print(streamUrl)
    streamUrl = streamUrl.json()["url"]
    streamUrl = unquote(re.sub(r"(.{1,2})", r"%\1", streamUrl))
    return streamUrl


def liveit():
    url = koora()
    ch, key = basic(url)
    url = url.split("/")[:3]
    referrer = "/".join(url)
    url = choose(referrer, ch, key)
    print(f"> {url}")
    print(f"> {referrer}")
    cmd = f"""vlc -v --loop "{url}" --http-referrer="{referrer}
        " --http-user-agent="{agent}" --adaptive-use-access"""
    os.system(cmd)


# ref = "https://8k.alkoora.live/albaplayer/on-time-sport-2/"
# u = ref + "?serv=2"
# print(u)
# sess = requests.session()
# sess.headers["referer"] = u
# r = sess.get(u)
# html = r.text
# url = re.findall(r"http[^\"']*m3u8[^\"']*", html)[0]

# kk = re.findall(r"[^<>]*m3u8[^<>]*", html)
# print(kk)

ref = "https://veplay.top"
url = "https://veplay.top//stream/0215c8b6-aace-4b5f-98c8-5a554c77326c#autostart"
cmd = f"""yt-dlp "{url}"  --add-header "Referer: {ref}" """
os.system(cmd)
