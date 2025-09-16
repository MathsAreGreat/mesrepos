
import json
from urllib.parse import urljoin

import requests
from Besites.variables import monhtml


sess = requests.session()
sess.headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}


try:
    with open("Backups/okanimes.json", "r") as e:
        okanimes = json.load(e)
except:
    okanimes = {}


def servers(url):
    soup = monhtml(sess, url)

    links = [
        e["data-href"].rsplit("?", 1)
        for e in soup.find_all(class_="servers-list")
    ]

    return [
        server(urljoin(url, u))
        for u, r in links
        if "=mp4" in r or "=ok" in r
    ]


def server(url):
    r = sess.get(url).json()
    return r["data"]["attributes"]["url"]


def ok_episodes(okanime, anime):
    soup = monhtml(sess, okanime)
    links = soup.find(id="episodes-search-results").findAll("a")
    return [
        [
            f"{i:02}",
            servers(urljoin(okanime, link["href"]))
        ]
        for i, link in enumerate(links, start=1)
        if not okanimes.get(f"{anime}-{i:02}")
    ]


def oking(okanime, name):
    print("Okanimes :")
    ok_datas = ok_episodes(okanime, name)
    for ep, links in ok_datas:
        code = f"{name}-{ep}"
        okanimes[code] = {"links": {}}
        print("okanime :", code)
        okanimes[code]["links"]["mps"] = [e.split("/")[-1].split(
            "-")[-1].split(".")[0] for e in links if "mp4" in e]
        okanimes[code]["links"]["oks"] = [e.split("/")[-1]
                                          for e in links if "ok" in e]

    with open("Backups/okanimes.json", "w") as e:
        json.dump(okanimes, e)
    return okanimes
