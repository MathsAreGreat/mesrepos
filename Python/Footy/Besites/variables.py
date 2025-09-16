from concurrent.futures import ThreadPoolExecutor
import base64
import json
import requests
from urllib.parse import unquote
import os
from pathlib import Path
import re
from shutil import rmtree
import subprocess
from bs4 import BeautifulSoup
from functools import wraps
from time import sleep

DOWN_PATH = "Videos"


def retry_on_exception(wait_seconds=1):
    """
    A decorator to retry a function if an exception is raised.

    Args:
        wait_seconds (int): Number of seconds to wait before retrying.
    Returns:
        function: A wrapped function with retry logic.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    attempts += 1
                    print(f"> Attempt {attempts} failed !")
                    sleep(wait_seconds)

        return wrapper

    return decorator


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


def combine_vids(pt=DOWN_PATH):
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
                fs, key=lambda e: re.sub(r"[^0-9]", r"", e.rsplit(".", 1)[0]).zfill(20)
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


def run_tasks(your_function, datas, nb=20):
    with ThreadPoolExecutor(nb) as executor:
        results = executor.map(lambda args: your_function(*args), datas)
    return results


def multiple(nb=1):
    u = f"https://soccerfullmatch.com/page/{nb}"
    soup = monhtml(u)
    links = [(link["href"],) for link in soup.select("a[rel=bookmark]")]
    return run_tasks(single, links)


def monhtml(k):
    sess = requests.session()
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }
    r = sess.get(k, allow_redirects=True)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def single(u):
    *_, y, m, d = u.rsplit("-", 3)
    dt = f"{y}-{m}-{d}"
    soup = monhtml(u)
    tables = soup.findAll("table", class_="linktable")
    links = [
        tr.findAll("td") for tb in tables for tr in tb.findAll("tr") if tr.find("td")
    ]

    links = [(e[2].text.strip(), e[3].text, e[-2].a) for e in links if len(e) > 3]

    links = [
        [("en", en), ("dt", dt)]
        + [
            el.split("=", 1)
            for el in unquote(link["href"]).split("?", 1)[-1].split("&")
        ]
        for en, t, link in links
        # if link and ("ok.ru" in t.lower() or "dailymotion" in t.lower() or "smoothpre" in t.lower())
    ]

    links = [{k: v for k, v in el if k not in ["dl"]} for el in links]
    doc = Path("Keys")
    doc.mkdir(parents=True, exist_ok=True)
    for el in links:
        m = el["em"]
        del el["em"]
        st = base64.b64decode(f"{m}===").decode("utf-8")
        el["st"] = st
        m = st.split("/")[-1].split("=")[-1]
        fn = doc / f"{m}.json"
        if fn.exists():
            continue
        with open(fn, "w") as dl:
            json.dump(el, dl)


def fetch():
    keys = {}
    for f in Path("Keys").glob("*.json"):
        with open(f, "r") as fl:
            el = json.load(fl)
        keys[f.stem] = el
    return keys
