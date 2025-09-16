import json
from pathlib import Path
import re
from Mido.variables import aria_dwn, egybest, monhtml, run_tasks, upclear
import redis


r = redis.Redis(host="localhost", port=6379, decode_responses=True)

ref = "https://ak.sv"


def season(key, nb=0):
    u = f"{ref}/series/{key}"
    soup = monhtml(u)
    meslinks = soup.select("a")
    arr = [
        link.get("href").split("episode/")[-1].split("/")[0]
        for link in meslinks
        if link.get("href") and "/episode/" in link.get("href")
    ]
    eps = [e for e in set(arr) if not r.sismember(f"akwam:episodes_{key}", e)]
    if eps:
        r.sadd(f"akwam:episodes_{key}", *eps)
    print("::", key)
    if nb:
        meslinks = soup.find(id="series-episodes").select("a")
        ts = [
            link.get("href").split("series/")[-1].split("/")[0]
            for link in meslinks
            if link.get("href") and "/series/" in link.get("href")
        ]
        return ts, arr
    return arr


def single(g, cle):
    ds = r.get(f"akwam_{g}_{cle}")
    if ds:
        return json.loads(ds)
    url = f"{ref}/{g}/{cle}"
    print(f"{upclear}>", url)
    soup = monhtml(url)
    t = soup.h1.text.strip().replace("\n", "")
    if not soup.find(class_="header-tabs"):
        return {}
    tags = [li.text.strip() for li in soup.find(class_="header-tabs").select("li")]
    links = [
        (
            re.findall(r"[0-9-a-z\s\.]+", link.text, flags=re.IGNORECASE)[-1].strip(),
            link.get("href").split("/")[-1],
        )
        for link in soup.select("a.link-download")
    ]
    ds = {
        "name": t,
        "type": g,
        "links": [(key, tag, size) for tag, (size, key) in zip(tags, links)],
    }
    r.set(f"akwam_{g}_{cle}", json.dumps(ds))
    return ds


def get_episodes(*cles):
    if cles:
        for cle in cles:
            if not r.sismember("akwam:series", cle):
                r.sadd("akwam:series", cle)
    first_pass = True
    ts = []
    dones = []
    while first_pass or ts:
        ss = list(r.smembers("akwam:series"))
        print("|| Restart with", len(ss), "items !")
        first_pass = False
        ts = []
        arrs = []
        for key in ss:
            if key in dones:
                continue
            dones.append(key)
            tsr, arr = season(key, 1)
            ts += tsr
            arrs += arr
        ts = [e for e in ts if e not in ss]
        if ts:
            r.sadd("akwam:series", *ts)
        run_tasks(single, [("episode", e) for e in set(arrs)])
    return [single("episode", e) for e in r.smembers(f"akwam:episodes_{cle}")]


def episodes(*cles):
    if not cles:
        return 0
    arrs = []
    tr = []
    for cle in cles:
        if not r.sismember("akwam:series", cle):
            r.sadd("akwam:series", cle)
        ts, arr = season(cle, 1)
        arrs += arr
        tr += ts
    for c in set(tr):
        if c in cles:
            continue
        if not r.sismember("akwam:series", c):
            r.sadd("akwam:series", c)
        arrs += season(c)

    run_tasks(single, [("episode", e) for e in set(arrs)])
    return {
        e: single("episode", e)
        for cle in cles
        for e in r.smembers(f"akwam:episodes_{cle}")
    }


def dwn(k, ep):
    dl = ep["links"][0]
    doc, name = egybest(
        f"{dl[0]}-{k}", ep["name"], re.sub(r"[^0-9]", r"", dl[1]), "Akwam"
    )
    u = f"{ref}/download/{dl[0]}/{k}"
    soup = monhtml(u)
    uri = soup.find("a", download=True, href=True).get("href")
    aria_dwn(ref, doc, uri, f"{name}.mp4", False)


def get_movies(nb=0):
    u = f"https://ak.sv/movies?page={nb+1}"
    print(upclear, ">", u)
    soup = monhtml(u)
    meslinks = soup.select("a")
    return [
        link.get("href").split("movie/")[-1].split("/")[0]
        for link in meslinks
        if link.get("href") and "/movie/" in link.get("href")
    ]


# keys = ("3676", "5072", "4286", "117")
# eps = episodes(*keys)
# run_tasks(dwn, eps.items())

# # datas = run_tasks(get_movies, [(i,) for i in range(2)])
# # links = [link for urls in datas for link in urls]
# # run_tasks(single, [("movie", e) for e in set(links)])

k = "3226"
ep = single("movie", k)
dwn(k, ep)
