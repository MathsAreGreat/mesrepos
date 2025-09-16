import requests
import json
import os
import re
import base64
from uuid import uuid4
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def run_tasks(your_function, datas, nb=20):
    with ThreadPoolExecutor(nb) as executor:
        results = executor.map(lambda args: your_function(*args), datas)
    return results


def monhtml(k):
    sess = requests.session()
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    }
    r = sess.get(k, allow_redirects=True)
    encoding = r.encoding if 'charset' in r.headers.get(
        'content-type', '').lower() else None
    parser = 'html.parser'
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def jbd(s):
    dt = s.get("src")
    if not dt or "base64" not in dt:
        return None
    code = dt.split("base64,", 1)[-1]
    return base64.b64decode(code).decode('utf-8')


def keyfy(p):
    u = f"https://footyfull.com/?p={p}"
    soup = monhtml(u)

    links = [
        [el for el in e.get('href').split('/') if re.search(r"^[0-9]+$", el)]
        for e in soup.findAll("a") if e.get('href')
    ]
    tt = ["".join(e) for e in links if e][0]

    codes = [jbd(s) for s in soup.findAll("script")]
    names = [e.text.lower() for e in soup.findAll(class_="video-name")]
    codes = [s for s in codes if s and "videoselector" in s.lower()]
    code = codes[0].split("[")[-1]
    liens = json.loads(f'[{code}')
    kolo = [
        (n.title(), l.rsplit("/")[-1].rsplit("?")[0])
        for n, l in zip(names, liens)
        if "ok.ru" in l
        and "pre" not in n
        and "post" not in n
        and "highlight" not in n
    ]
    return tt, [
        {"key": key, "name": name}
        for name, key in kolo
    ]


def savetemp(u):
    try:
        soup = monhtml(u)
        datas = soup.findAll(class_="entry-image")
        datas = [e.find("a") for e in datas]
        ls = [
            (
                e.get("data-id"),
                e.get("title").title()
            )
            for e in datas
            if e
        ]
        print(">", len(ls), "items !", end="\r")
        key = uuid4()
        os.makedirs("temps", exist_ok=True)
        with open(f"temps/temp-{key}.json", "w") as e:
            json.dump(ls, e)
    except Exception as err:
        print(err)


def fdwn(i, dd):
    k, t = dd
    d, savedData = keyfy(k)
    if savedData:
        data = {
            "date": d,
            "title": t,
            "savedData": savedData
        }
        print(f"> {i:03}. Match #{k}", end="\r")
    return k, data


def infound(data, *qs):
    for q in qs:
        if q not in data:
            return 0
    return 1


def debut(file_to_save, qteam=""):
    saved_path = f"files/t{file_to_save}.json"
    if os.path.exists(saved_path):
        return 0
    print()
    for f in os.listdir("files"):
        if f[0] == "t" and f.endswith(".json"):
            os.remove(f"files/{f}")
    for i in range(1):
        u = f"https://footyfull.com/page/{i+1}/"
        savetemp(u)
    ls = []
    for f in os.listdir("temps"):
        if f.startswith("temp-"):
            fn = f"temps/{f}"
            with open(fn, "r") as e:
                data = json.load(e)
            ls += data
            os.remove(fn)

    nbrs = {e: c for e, c in ls}
    ls = [
        (e, v)
        for e, v in nbrs.items()
        if infound(v.lower(), "vs", qteam)
    ]

    datas = list(enumerate(ls, start=1))
    results = run_tasks(fdwn, datas)
    datas = []
    for k, data in results:
        item = {"KEY": k} | data
        datas.append(item)
    datas = sorted(datas, key=lambda e: e["date"], reverse=True)
    with open(saved_path, "w") as e:
        json.dump(datas, e)
    return 1


if __name__ == "__main__":
    ss = "https://cc.yallashoot.shop/albaplayer/sports-2/?serv=1"

    sess = requests.session()
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        "Referer": "https://shot.yalla4shoot.com/matches/%d8%aa%d9%81%d8%a7%d8%b5%d9%8a%d9%84-%d9%88%d9%85%d9%88%d8%b9%d8%af-%d9%85%d8%a8%d8%a7%d8%b1%d8%a7%d8%a9-%d8%a7%d9%84%d9%87%d9%84%d8%a7%d9%84-%d9%88-%d8%a7%d9%84%d8%a3%d9%87%d9%84%d9%8a-%d8%a7%d9%84/"
    }
    rs = sess.get(ss)
    print(rs.text)
