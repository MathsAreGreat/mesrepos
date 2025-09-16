import os
import subprocess
import html
import json
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from random import choice
import requests
import m3u8
from concurrent.futures import ThreadPoolExecutor
from shutil import rmtree
from pathlib import Path
from datetime import datetime
from Besites.variables import retry_on_exception


cols = ["#00ff00", "red", "green", "yellow",
        "blue", "magenta", "cyan", "white"]

sess = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": "https://ok.ru/",
}

sess.headers = headers


def run_tasks(fn, ds, nb=20):
    def your_function(args):
        return fn(*args)

    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


@retry_on_exception(1)
def check_for_datas(k):
    doc = "datas/OKRU"
    fn = f"{doc}/{k}"
    if re.search(r"[a-z]", k.lower()):
        Path(doc).mkdir(parents=True, exist_ok=True)
        Path(fn).touch()
    if Path(fn).exists():
        return None
    ok_url = f"https://ok.ru/videoembed/{k}"
    r = sess.get(ok_url)
    txt = html.unescape(r.text)
    soup = BeautifulSoup(txt, "html.parser")
    msg = soup.find(class_="vp_video_stub_txt")
    if msg:
        Path(doc).mkdir(parents=True, exist_ok=True)
        Path(fn).touch()
        return None
    return ok_url


def getUrl(k, t):
    ok_url = check_for_datas(k)
    if not ok_url:
        return None
    fjson = f"t{k}.json"
    cmd = f'yt-dlp "{ok_url}" --flat-playlist --skip-download --dump-json > {fjson}'
    os.system(cmd)
    print(">>", fjson, end="\r")
    try:
        with open(fjson, "r") as e:
            data = json.load(e)
    except:
        data = {}
    os.remove(fjson)
    print("X", fjson)
    if not data:
        return []
    for e in data["formats"]:
        if e.get("protocol") and e["protocol"] == "m3u8_native":
            uri = e["manifest_url"]
            pl = get_playlist(uri)
            dts = get_segments(pl)
            return [(u, t, f"{i:06}.ts") for i, u in enumerate(dts)]


def get_playlist(uri):
    r = sess.get(uri)
    mdt = m3u8.loads(r.text)
    pl = None
    bd = 0
    for playlist in mdt.playlists:
        bandwidth = playlist.stream_info.bandwidth
        if bandwidth > bd:
            bd = bandwidth
            pl = urljoin(uri, playlist.uri)
    return pl


def get_segments(uri):
    mdt = m3u8.load(uri, headers=headers)
    return [urljoin(uri, seg.uri) for seg in mdt.segments]


def sauver(k, t):
    d = datetime.now()
    n = d.strftime("%Y%m%d%H%M")
    doc = f"datas/OKRU/{n}"
    fjson = f"{doc}/{k}.json"
    if os.path.exists(fjson):
        with open(fjson, "r") as e:
            sgs = json.load(e)
    else:
        os.makedirs(doc, exist_ok=True)
        sgs = getUrl(k, t)
        if not sgs:
            return []
        with open(fjson, "w") as e:
            json.dump(sgs, e)
    return sgs


def dwn(url, ds, tn):
    sess = requests.session()
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": "https://ok.ru/",
    }
    ds = "-".join(e.title() for e in ds.split("/"))
    doc = ds.rsplit(".", 1)[0]
    ds = ds.replace(" ", ".")
    doc = f"Library/MixAnimes/Seasons/{doc}/{ds}"
    if Path(f"{doc}.mp4").exists():
        return None
    Path(doc).mkdir(parents=True, exist_ok=True)
    sn = Path(f"{doc}/{tn}")
    if sn.exists():
        return None
    fn = Path(f"{doc}/{tn}.part")
    response = sess.get(url, stream=True, allow_redirects=False, timeout=100)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(
        total=total_size_in_bytes,
        unit="iB",
        unit_scale=True,
        leave=False,
        desc=f"{tn} ",
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
    fn.rename(sn)
    return 1


def goo(stream):
    docr = Path("Library/MixAnimes/Seasons")
    for f in docr.glob("*/*.ts"):
        if int(f.stat().st_size) < 1000:
            f.unlink()
    sgz = run_tasks(sauver, stream, 5)
    if not sgz:
        return 0
    datas = [sgs for sgs in sgz if sgs]
    datas = [d for dt in datas for d in dt]
    print("OKRU :", len(datas), "items !")
    run_tasks(dwn, datas, 10)
    return combine_vids("Library/MixAnimes")


def concatize(*files, o="output", ex="ts"):
    """
    Concatenate multiple files using FFmpeg.

    Parameters:
        files (*args): List of file paths to concatenate.
        output_name (str): Name of the output file.
        extension (str): Extension for the output file.
    """
    if not files:
        print("No files provided for concatenation.")
        return

    input_files = "|".join(str(file) for file in files)
    output_path = Path(f"{o}.{ex}")
    cmd = f'ffmpeg -i "concat:{input_files}" -c copy "{output_path}"'

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"* {output_path} Created!", end="\r")
    except subprocess.CalledProcessError:
        print("Error: Failed to concatenate files.")


def combine_vids(pt):
    try:
        p = Path(pt)
    except:
        return 0
    nb = 0
    for v_out in p.rglob("*"):
        if v_out.is_file():
            continue
        fs = [f"{f}" for f in v_out.glob("*.part")]
        if fs:
            nb += 1
            continue
        fn = v_out.with_suffix(f"{v_out.suffix}.mp4")
        if not fn.exists():
            fs = [f"{f}" for f in v_out.glob("*.ts")]
            fs = sorted(
                fs, key=lambda e: re.sub(
                    r"[^0-9]", r"", e.rsplit(".", 1)[0]).zfill(20)
            )
            ph = 0
            j = 1
            NBR = 900
            while len(fs) > NBR:
                i = 0
                ph += 1
                while fs:
                    i += 1
                    concatize(*fs[:NBR], o=f"{v_out}_{j}_{i}")
                    fs = fs[NBR:]
                fs = [f"{v_out}_{j}_{n+1}.ts" for n in range(i)]
                j += 1
            concatize(*fs, o=v_out, ex="mp4")
            if ph:
                for f in fs:
                    os.remove(f)
                    msg = f"** Removing {f}"
                    print(f"{msg:<40}")
        if fn.exists():
            rmtree(f"{v_out}")
    msg = "> All is Done !"
    print(f"{msg:<40}")
    return nb


def get_datas(k):
    ok_url = check_for_datas(k)
    if not ok_url:
        return []
    fjson = f"t{k}.json"
    cmd = f'yt-dlp "{ok_url}" --flat-playlist --skip-download --dump-json > {fjson}'
    subprocess.run(cmd, shell=True, check=True)
    print(">>", fjson, end="\r")
    try:
        with open(fjson, "r") as e:
            data = json.load(e)
        Path(fjson).unlink()
        print("X", fjson, " " * 5)
    except:
        data = {}
    if not data:
        return []
    for e in data["formats"]:
        if e.get("protocol") and e["protocol"] == "m3u8_native":
            uri = e["manifest_url"]
            pl = get_playlist(uri)
            return get_segments(pl)


@retry_on_exception(1)
def contenu(u):
    sess.headers = headers
    r = sess.get(u, stream=True, timeout=10)
    c = int(r.headers.get("content-length", 0))
    print(f"> {c} bytes", " " * 10, end="\r")
    return c


def oksize(k):
    dts = get_datas(k)
    if not dts:
        return 0
    nb = 10000
    datas = run_tasks(contenu, [(e,) for e in dts[:nb]], 20)
    somme = sum(datas)
    nb = somme // 1000
    return nb / 1000
