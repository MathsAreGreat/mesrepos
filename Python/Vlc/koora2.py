from datetime import datetime
import requests
import os
import re
from bs4 import BeautifulSoup
agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
referrer = 'https://8k.alkoora.live'


def bsin(text):
    return BeautifulSoup(text, 'html.parser')


def monhtml(r, ref):
    sess = requests.session()
    sess.headers.update({
        'User-Agent': agent,
        'Referer': ref
    })
    t = ""
    nb = 5
    while t == "" and nb:
        rs = sess.get(r, allow_redirects=False)
        t = rs.text
        print(nb)
        nb -= 1
    return bsin(t)


def koora():
    u = "https://koora4lives.koora4live.co/"
    soup = monhtml(u)
    infos = []
    divs = soup.findAll(attrs={'class': 'alkooralive'})
    i = 1
    for div in divs:
        link = div.find("a")['href']
        ts = " VS ".join(
            t.text.strip()
            for t in div.findAll(attrs={'class': 'team-name'})
        )
        infos.append(link)
        print(">", i, ":", ts)
        i += 1
    nb = int(input("Enter your chosen match : "))-1
    return infos[nb]


def basic(url):
    soup = monhtml(url)
    link = soup.find(target="search_iframe")
    u = link["href"]
    ds = datetime.now().strftime("%Y%m%d")
    print('>', u)
    soup = monhtml(u)
    links = [
        (link.text, link["href"])
        for link in soup.findAll("a")
        if link.get("href")
        and "serv=" in link["href"]
    ]
    infos = []
    for i, (t, u) in enumerate(links, start=1):
        vl = 1
        vl = choose(ds, t, u)
        infos.append(vl)
        if vl:
            print(f"> {i:02d}.", t, ":", u)
    nb = int(input("Enter your chosen match : "))-1
    return infos[nb]


def choose(ds, t, url):
    if "جوال" in t:
        return None
    doc = f"koora4lives/{ds}"
    fn = f"{doc}/{t}.txt"
    if not os.path.exists(fn):
        os.makedirs(doc, exist_ok=True)
        sess = requests.session()
        rs = sess.get(url)
        txt = rs.text
        us = re.findall(r"http[^'\"]+m3u8[^'\"]*", txt)
        if not us:
            return None
        link = us[0]
        with open(fn, "w") as e:
            e.write(link)
    else:
        with open(fn, "r") as e:
            link = e.read()
    return link


def liveit():
    url = koora()
    url = basic(url)
    url = choose(url)
    print(f"> {url}")
    print(f"> {referrer}")
    cmd = f"""vlc -v --loop "{url}" --http-referrer="{referrer}
        " --http-user-agent="{agent}" --adaptive-use-access"""
    os.system(cmd)


if __name__ == "__main__":
    # url = "https://t4.kora44.site/broadcast/O0DNxDYc5s0V8BTYi6vRrg/1729453213/1729452952/1/bein01.m3u8"
    # referrer = "https://games-promax.com/"
    # cmd = f"""vlc -v --loop "{url}" --http-referrer="{referrer}
    #     " --http-user-agent="{agent}" --adaptive-use-access"""
    # os.system(cmd)
    url = "https://games-promax.com/read100/24.php?hash=eyJBUiAxIjoiYmVpbjAxIiwiQVIgMiI6ImJlaW4wOSIsIkVOIjoibXVsdGktMSJ9"
    ref = "https://yalla-shoot-2k.com/"
    soup = monhtml(url, ref)
    iframe = soup.iframe
    link = iframe.get("src")
    soup = monhtml(link, link)
    print(soup)
