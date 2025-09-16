import os
import re
import json
import m3u8
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm.auto import tqdm
from random import choice

cols = [
    "#00ff00", 'red',
    'green', 'yellow',
    'blue', 'magenta',
    'cyan', 'white'
]
sess = requests.session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": "https://ok.ru/",
}


def dwn(dd):
    u, ds, tn = dd
    url = f"{u}{tn}"
    ds = "-".join(e for e in ds.split('/'))
    doc = f"Koora/{ds}"
    os.makedirs(doc, exist_ok=True)
    fn = f"{doc}/{tn}"
    if os.path.exists(fn):
        return None
    fn = f"{doc}/{tn}.part"
    response = sess.get(url, stream=True)
    bar_format = "{l_bar}{bar}{r_bar}"
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(
        total=total_size_in_bytes,
        unit="iB",
        unit_scale=True,
        leave=False,
        desc=f"{tn} ",
        bar_format=bar_format,
        colour=choice(cols),
    )
    with open(fn, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        return 0
    os.rename(fn, f"{doc}/{tn}")
    return 1


def getUrl(k):
    u = f"https://ok.ru/video/{k}"
    fjson = f"t{k}.json"
    cmd = f'yt-dlp "{u}" --flat-playlist --skip-download --dump-json > {fjson}'
    os.system(cmd)
    print(">>", fjson)
    try:
        with open(fjson, "r") as e:
            data = json.load(e)
    except:
        data = {}
    os.remove(fjson)
    print("X", fjson)
    if not data:
        return None
    formats = [
        e["manifest_url"]
        for e in data["formats"]
        if e.get("protocol") and e["protocol"] == "m3u8_native"
    ]
    return formats[0]


def first_last(arr):
    ch, sn, ex = re.findall(r"^(.+[^0-9])([0-9]+)\.(.+)$", arr[0])[0]
    num_digits = len(sn)
    start_num = int(sn)
    end_num = int(arr[-1].rsplit(".", 1)[0].replace(ch, ""))
    return ch, start_num, end_num, num_digits


def getSgs(k, t):
    try:
        url = getUrl(k)
    except:
        url = None
    if not url:
        return {}
    r = sess.get(url)
    playlists = [
        [e["stream_info"]["quality"], e["uri"], e["stream_info"]["bandwidth"]]
        for e in m3u8.loads(r.text).data["playlists"]
    ]
    info = {}
    info["cle"] = k
    info["nm"] = t
    info["formats"] = []
    for k, u, bandwidth in playlists:
        if not u.startswith("http"):
            dom = "/".join(url.split("/")[:3])
            u = f"{dom}{u}"
        sgs = [
            e["uri"]
            for e in m3u8.loads(sess.get(u).text).data["segments"]
        ]
        ch, s, e, dj = first_last(sgs)
        if "st" not in info:
            info["st"] = s
            info["en"] = e
            info["dj"] = dj
        dk = {"ch": ch, "sc": u, "sz": bandwidth, "hd": k}
        info["formats"].append(dk)

    info["formats"] = sorted(
        info["formats"], key=lambda e: e["sz"], reverse=True)

    return info


def print_chapters(data):
    if not data:
        return []
    k, t, formats, start_num, end_num, num_digits = data.values()
    lesdatas = []
    for hd in range(len(formats)):
        ch, u, *_ = formats[hd].values()
        lesdatas += [
            [u, f"{t} [{ch}] ({k})", f"{ch}{chapter_num:0{num_digits}d}.ts"]
            for chapter_num in range(start_num, end_num + 1)
        ]
        if lesdatas:
            break
    return lesdatas


k = "249298291262"
t = "FCB VS PSG"
fjson = f"datas/{k}.json"

os.makedirs("datas", exist_ok=True)
sgs = getSgs(k, t)
with open(fjson, "w") as e:
    json.dump(sgs, e)

datas = print_chapters(sgs)
with ThreadPoolExecutor(20) as executor:
    executor.map(dwn, datas)
