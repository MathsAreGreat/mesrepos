from Mido.variables import monhtml, aria_dwn, run_tasks, egybest
import re
from pathlib import Path


USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

referrer = "https://m15.asd.rest/"

wref = "https://m.gamehub.cam/"

headers = {
    "user-agent": USER_AGENT
}

uns = [
    f.stem.split(".")[-1][1:-1]
    for f in Path("/home/mohamed/Downloads/Library/ArabSeed").rglob("*.mp4")
]


def eps(u):
    headers["Referer"] = referrer
    soup = monhtml(u, headers=headers)
    return [
        (e.get("href"),)
        for e in soup.select_one(".ContainerEpisodesList").select("a")
    ]


def dwatch(u):
    headers["Referer"] = referrer
    soup = monhtml(u, headers=headers)
    t = soup.select_one(".InfoPartOne h2").text
    return t, soup.find(id="shortLinkInput").get("value").split("=")[-1], soup.select_one(".watchBTn").get("href")


def dlink(u):
    soup = monhtml(u, headers=headers)
    containerServers = soup.select_one("div.containerServers")
    links = [
        link.get("data-link")
        for link in containerServers.select("li[data-link]")
        if "gamehub" in link.get("data-link")
    ]
    hds = [
        re.findall(r"[0-9]+", h.text)[-1]
        for h in containerServers.select("h3")
    ]
    headers["Referer"] = wref
    datas = []
    for h, link in zip(hds, links):
        soup = monhtml(f"{link}?filename=vid", headers=headers)
        dl = soup.source.get("src")
        datas.append((int(h), dl))
    return max(datas, key=lambda e: e[0])


def infos(u):
    t, c, url = dwatch(u)
    if c in uns:
        return None
    h, dl = dlink(url)
    dist, fl = egybest(c, t, h, "ArabSeed")
    return (
        wref,
        dist,
        dl,
        f"{fl}.mp4"
    )


u = "https://m15.asd.rest/selary/%d8%a7%d9%86%d9%85%d9%8a-your-forma-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%a7%d9%88%d9%84/"

urls = eps(u)
datas = run_tasks(infos, urls)
datas = [e for e in datas if e]
run_tasks(aria_dwn, datas)
