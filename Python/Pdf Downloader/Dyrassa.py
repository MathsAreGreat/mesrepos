import requests
import os
from tqdm.auto import tqdm
from random import choice
from bs4 import BeautifulSoup
from Mido.variables import run_tasks, sprint

cols = ["#00ff00", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN"]


def monhtml(r):
    sess = requests.Session()
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }
    r = sess.get(r)
    return BeautifulSoup(r.text, "html.parser")


def vid_download(doc, url):
    name = url.split("/")[-1]
    sess = requests.Session()
    p_file = f"{doc}/{name}"
    if os.path.exists(p_file):
        return 0
    p_file = f"{doc}/{name}.part"
    os.makedirs(doc, exist_ok=True)
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    }
    response = sess.get(url, stream=True, timeout=100)
    total_size_in_bytes = int(response.headers.get("content-length", 0))

    if total_size_in_bytes < 1000:
        print("** file :", name)
        print("** url :", url)
        print("=" * (len(url) + 1))
        return 0
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(
        total=total_size_in_bytes,
        leave=False,
        colour=choice(cols),
        unit="iB",
        unit_scale=True,
        desc=f"{name} ",
    )
    with open(p_file, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("Error :", name)
        return 0
    name = p_file.replace(".part", "")
    os.rename(p_file, name)
    print("", end=name)
    return 1


def dig(sec):
    print(sec)
    soup = monhtml(sec)
    links = soup.select("h3 a")
    titre = soup.select_one("h1").text.strip().replace("/", "-")
    if not links:
        return []
    return [
        (f"/home/mohamed/Documents/Dyrassa/{titre}", link["href"]) for link in links
    ]


# soup = monhtml("https://dyrassa.com/primaire/")

# sections = [link["href"] for link in soup.select("#content a") if link.get("href")]

# datas = []

# raws = run_tasks(dig, [(s,) for s in set(sections)], 10)
# datas = [
#     el
#     for raw in raws
#     for el in raw
# ]

# sprint("Let's download !")
# print(f"** {len(datas)} files to download !")
# nb = 1
# while nb:
#     dt = run_tasks(vid_download, datas, 20)
#     nb = sum(d for d in dt)
#     print(f"** {nb} files are downloaded !")


sec = "https://dyrassa.com/evaluations-diagnostiques/evaluations-diagnostiques-maths-college/"

datas = dig(sec)

sprint("Let's download !")
print(f"** {len(datas)} files to download !")

nb = 1
while nb:
    dt = run_tasks(vid_download, datas, 20)
    nb = sum(d for d in dt)
    print(f"** {nb} files are downloaded !")
