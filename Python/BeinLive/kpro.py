import m3u8
import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote
from Crypto.Cipher import AES


agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
referrer = 'https://play-1.reyada-365.com/'
doom = "https://www.kooora4live.ai"

sess = requests.session()
sess.headers = {
    "Referer": referrer,
    "User-Agent": agent
}


def bsin(text):
    return BeautifulSoup(text, 'html.parser')


def monhtml(r):
    sess = requests.session()
    sess.headers["Referer"] = r
    rs = sess.get(r, allow_redirects=True)
    txt = rs.text
    return bsin(txt)


def koora():
    soup = monhtml(doom)
    infos = []
    divs = soup.findAll(
        attrs={'class': 'match-container'}
    )
    i = 1
    for div in divs:
        link = div.find("a")['href']
        nb = len(link.split("/"))
        if nb < 5:
            continue
        ts = " VS ".join(
            t.text.strip()
            for t in div.findAll(attrs={'class': 'team-name'})
        )
        infos.append((ts, link))
    return infos


def basic(url):
    ns = url.split('/')
    if re.search(r"[^0-9]", ns[4]):
        u = url+"?serv=0"
    else:
        ns[3] = "embed"
        u = "/".join(ns[:5])
    sess = requests.session()
    sess.headers['referer'] = u
    r = sess.get(u)
    html = r.text
    base_url = re.findall(r"url = ([^;]+)", html)[0]
    kk = re.findall(r"key[0-9]+", html)[0]
    return base_url.replace("'", ""), kk


def choose(referrer, ch, key):
    sess = requests.session()
    sess.headers["Referer"] = referrer
    streamUrl = f"{referrer}/token.php"
    streamUrl = sess.post(streamUrl, data={"ch": ch, "key": key})
    print(streamUrl)
    streamUrl = streamUrl.json()["url"]
    streamUrl = unquote(re.sub(r"(.{1,2})", r"%\1", streamUrl))
    return streamUrl


def dwn(v, ref, url, e, dd):
    cipher = None
    if dd:
        key, iv = dd
        cipher = AES.new(key, AES.MODE_CBC, iv)
    sess.headers = {
        "Referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    if e:
        item = "-".join(e.split("/"))
        doc = f"/home/mohamed/Videos/Ts/{v}"
        lefile = f"{doc}/{item}"
        if not os.path.exists(lefile):
            os.makedirs(doc, exist_ok=True)
            us = f"{url}/{e}"
            rz = sess.get(us, timeout=100)
            cx = rz.status_code
            if cx == 200:
                c = rz.content
                if cipher:
                    c = cipher.decrypt(c)
                print(">", item)
                with open(lefile, "wb") as f:
                    f.write(c)


def save(c, k):
    if re.search(r"[a-z]", c):
        ch = c
    else:
        ch = f"bein{c:>02}"
    key = f"key{k:>03}"
    referrer = "https://u1.koooralive.io"
    v = f"CH-{key}"
    base_url = choose(referrer, ch, key)
    base, _ = base_url.rsplit("/", 1)
    sess = requests.session()
    print(base_url)
    sess.headers = {
        "Referer": referrer,
    }
    print(referrer)
    rs = sess.get(base_url, stream=True)
    mm = rs.text
    segments = m3u8.loads(mm).segments
    try:
        segment = segments[0]
        k = segment.key.uri
        sess.headers = {
            "Referer": referrer,
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        }
        resp = sess.get(f"{base}/{k}")
        vv = segment.key.iv
        iv = int(vv, 16).to_bytes(16, "big")
        key = resp.content
        dd = (key, iv)
    except Exception as e:
        print("Segment :", e)
        dd = None
    return [
        (v, referrer, base, seg.uri, dd)
        for seg in segments
    ]


# ks = [("1", "1")]
# with ThreadPoolExecutor(10) as executor:
#     datas = executor.map(lambda e: save(*e), ks)
# lesdatas = [e for data in datas for e in data]
# with ThreadPoolExecutor(10) as executor:
#     executor.map(lambda args: dwn(*args), lesdatas)

datas = koora()
print(datas)
