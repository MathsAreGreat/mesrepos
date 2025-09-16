from functions import combine_vids
import os
import glob
import re
import json
import m3u8
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm.auto import tqdm
from random import choice
import cv2
import time
from fetch import debut
from datetime import datetime
from shutil import rmtree


def get_video_duration(file_path):
    try:
        # Open the video file
        cap = cv2.VideoCapture(file_path)
        # Get the frames per second (fps) and frame count
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Calculate the duration in seconds
        duration = frame_count / fps
        # Release the video capture object
        cap.release()
        return int(duration)+1
    except Exception as e:
        print(f"Error: {e}")
        return None


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


def v_crop(dd):
    v_in, i, start, end = dd
    v_out = f"{v_in} [Part{i}]"
    ex = "mp4"
    cmd = f'ffmpeg -i "{v_in}.{ex}" -ss {start} -t {end -
                                                    start} -c copy -avoid_negative_ts make_zero "{v_out}.{ex}"'
    os.system(cmd)
    return 1


os.makedirs("Matches", exist_ok=True)
os.makedirs("files", exist_ok=True)


c = 1
while c:
    today = datetime.today().strftime("%Y%m%d%H")
    debut(today)
    rmtree("datas", ignore_errors=True)
    for f in glob.glob("Koora/*/*.part"):
        os.remove(f)

    uniques = [
        f.split("(")[-1].split(")")[0] for f in glob.glob("Koora/*.mp4")
    ]

    uniques += [
        f.split("(")[-1].split(")")[0] for f in glob.glob("Matches/*.mp4")
    ]

    uniques += [
        f.split("/")[-1].split(")")[0] for f in glob.glob("Backups/*")
    ]
    keys = []
    f = "files/datas.json"
    datas = []
    for f in os.listdir("files"):
        with open(f"files/{f}", "r") as e:
            datas += json.load(e)
    datas = {e["KEY"]: e for e in datas}
    datas = [
        v
        for v in datas.values()
        if v["title"].endswith("Real Madrid")
        and v["date"] == "20240430"
    ]
    if not datas:
        print("No data", time.time())
        time.sleep(3000)
        continue
    datas = sorted(datas, key=lambda e: e["date"])
    for data in datas:
        savedData = [
            e
            for e in data["savedData"]
            if "pre" not in e["name"].lower()
            and "post" not in e["name"].lower()
            and "highl" not in e["name"].lower()
        ]
        for el in savedData:
            dt = data["date"]
            t = f"""{data["title"]} [{el["name"]}] [{
                dt[-2:]}-{dt[4:-2]}-{dt[:4]}]"""
            keys.append((el["key"], t))
    infos = [(k, t) for k, t in keys if k not in uniques]
    if not infos:
        print("No data", time.time())
        time.sleep(5)
        continue
    print("Some datas Here !")
    datas = []
    for k, t in infos:
        fjson = f"datas/{k}.json"
        if not os.path.exists(fjson):
            os.makedirs("datas", exist_ok=True)
            sgs = getSgs(k, t)
            with open(fjson, "w") as e:
                json.dump(sgs, e)
        else:
            with open(fjson, "r") as e:
                sgs = json.load(e)
        datas = print_chapters(sgs)
        if datas:
            break

    with ThreadPoolExecutor(20) as executor:
        executor.map(dwn, datas)

    arr = list(glob.glob("Koora/*/*.part"))
    tsr = list(glob.glob("Koora/*/*.ts"))
    if not arr and tsr:
        combine_vids()
        parties = []
        # for f in glob.glob("Koora/*mp4"):
        #     size = os.stat(f).st_size
        #     if size > 1900000000:
        #         duree = get_video_duration(f)
        #         parts = (os.stat(f).st_size // 1500_000_000) + 1
        #         print(f)
        #         print(">", size)
        #         print(">", duree)
        #         print()
        #         rg = duree//parts
        #         for i in range(parts):
        #             st = i*rg
        #             ed = (i+1)*rg
        #             parties.append([f.rsplit(".", 1)[0], i+1, st, ed])
        #         parties[-1][-1] = duree

        # with ThreadPoolExecutor(10) as executor:
        #     executor.map(v_crop, parties)

        for f in glob.glob("Koora/*].mp4"):
            name = f.rsplit(" ", 1)[0]
            fn = f"{name}.mp4"
            try:
                os.remove(fn)
            except:
                pass

        os.makedirs("Matches", exist_ok=True)
        os.makedirs("Backups", exist_ok=True)
        for f in glob.glob("Koora/*mp4"):
            c = f.split("(")[-1].split(")")[0]
            with open(f"Backups/{c}", "w") as e:
                e.write("")
            fn = f.replace("Koora/", "Matches/")
            os.rename(f, fn)
        for f in glob.glob("datas/*json"):
            with open(f, "r") as e:
                data = json.load(e)
            if data:
                continue
            c = f.split("/")[-1].split(".")[0]
            with open(f"Backups/{c}", "w") as e:
                e.write("")
