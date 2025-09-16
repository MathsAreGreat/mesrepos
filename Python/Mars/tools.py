from tqdm.auto import tqdm
import random
from pathlib import Path
from bs4 import BeautifulSoup
import requests

cols = ["#00ff00", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN"]


def monhtml(r, ref=None, data=None):
    sess = requests.session()
    if not ref:
        refs = r.split('/')[:3]
        ref = "/".join(refs)
    sess.headers = {
        "referrer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    if data:
        r = sess.post(r, data=data)
    else:
        r = sess.get(r)
    encoding = r.encoding if 'charset' in r.headers.get(
        'content-type', '').lower() else None
    parser = 'html.parser'  # or lxml or html5lib
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def vid_download(url):
    doc = Path("/home/mohamed/Music/Radios/Mars")
    f = f"{url.split("/")[-1]}"
    f_file = doc / f
    if f_file.exists():
        return 0
    f = f"{url.split("/")[-1]}.part"
    f_file = doc / f
    refs = url.split('/')[:3]
    ref = "/".join(refs)
    doc.mkdir(parents=True, exist_ok=True)
    try:
        sz = f_file.stat().st_size
    except:
        sz = 0
    sess = requests.Session()
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Range": f"bytes={sz}-",
        "Referer": ref
    }
    response = sess.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    incomplete = 1
    if total_size_in_bytes < 1000:
        incomplete = 0
    block_size = 1024
    clr = random.choice(cols)
    progress_bar = tqdm(
        total=total_size_in_bytes,
        leave=False,
        colour=clr,
        unit="iB",
        unit_scale=True,
        desc=f"{f}: "
    )
    try:
        if incomplete:
            with open(f_file, "ab") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
        f_file.rename(f_file.with_suffix(""))
        c = f_file.stem.split("_")[-1].split(".")[0].strip()
        doc = Path("Backups")
        doc.mkdir(parents=True, exist_ok=True)
        fn = doc / c
        fn.touch()
        print(end="")
    except Exception as e:
        print("ERROR, something went wrong")
        print(e)


def mp3files(u, uns):
    soup = monhtml(u)
    links = soup.findAll("a", href=True)
    liens = [e["href"] for e in links]
    liens = [
        e
        for e in liens
        if e.endswith("mp3") and e not in uns
    ]
    print(len(liens), "items !")
    for lien in liens[:3]:
        vid_download(lien)
    return len(liens)


nb = 1
while nb:
    parent = Path("/home/mohamed/Music/Radios/Mars")
    for f in parent.rglob('*.mp3'):
        c = f.stem.split("_")[-1]
        fn = Path(f"Backups/{c}")
        if not fn.is_file():
            fn.touch()
    so = "https://replay.radiomars.ma/podcasts/Mars-Attack/Mars_Attack"
    uns = [
        f"{so}_{f.stem}.mp3"
        for f in Path("Backups").rglob('*')
    ]
    u = "https://www.radiomars.ma/ar/emissions/مارس-أطاك/"
    nb = mp3files(u, uns)
