from pathlib import Path
import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor
sess = requests.Session()
sess.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}
pdf_path = Path("/home/mohamed/Documents/AlloSchool")
uniques = [f.name for f in pdf_path.rglob("*.pdf")]


cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up+clear


def cl_links(url):
    vals = sess.get(url).text
    vals = re.findall(r'http[^"]+/course/[^"]+', vals)
    with ThreadPoolExecutor(10) as executor:
        datas = executor.map(
            pdf_links,
            vals
        )
    return [e for data in datas for e in data]


def pdf_links(url):
    vals = sess.get(url).text
    items = vals.split('<ol', 1)[-1].split('</ol', 1)[0].split("<li")[-3:]
    items = [
        re.sub(r"^[^>]*>", r"", item)
        for item in items
    ]
    items = [
        re.sub(r"<[^>]+>", r"", item).strip()
        for item in items
    ]
    title = "/".join(items)
    els = re.findall(r'(http[^"]+/element/[0-9]+)"', vals)
    f = re.findall(r'(http[^"]+pdf)"', vals)
    s = re.findall(r'(http[^"]+zip)"', vals)
    t = re.findall(r'(http[^"]+rar)"', vals)
    vals = f+s+t
    vals = [(title, v) for v in set(vals)]
    for v in set(els):
        us = dwn_file(v)
        vals += [(title, u) for u in us]
    print(f"{upclear}=>", url)
    return vals


def dwn_file(download_url):
    try:
        vals = sess.get(download_url).text
        return re.findall(r'(http[^"]+pdf)"', vals)
    except:
        return []


def download_file(doc, download_url):
    r = sess.get(download_url, stream=True, timeout=5)
    try:
        f, ex = r.headers["Content-Disposition"].split('"')[1].rsplit(".", 1)
        c = re.findall(r"[0-9]+", download_url)[-1]
        name = f"{f}.{c}.{ex}"
    except:
        name = download_url.split('/')[-1]
    fpath = pdf_path / doc
    filename: Path = fpath / name
    if not filename.exists():
        fpath.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(filename, 'wb') as file:
            file.write(r.content)
        print(f"{upclear}:: {name} .")


parent = Path("/home/mohamed/Documents/AlloSchool")
uns = [
    f.stem.split(".")[-1].replace('(', '').replace(')', '')
    for f in parent.rglob("*.pdf")
]
uns += [f.name for f in parent.rglob("*.zip")]
uns += [f.name for f in parent.rglob("*.rar")]

url = "https://www.alloschool.com/category/middle-school"
# url = "https://www.alloschool.com/category/primary"
# url = "https://www.alloschool.com/category/common-core"

c = url.split("/")[-1]
fn = f"{c}.json"
try:
    with open(fn, "r") as f:
        datas = json.load(f)
except:
    print()
    datas = cl_links(url)
    with open(fn, "w") as f:
        json.dump(datas, f)

datas = [
    (d, e)
    for d, e in datas
    if e.split('/')[-1] not in uns and e.split('/')[-2] not in uns
]
print(">>", len(datas), "items !")
print()
with ThreadPoolExecutor(5) as executor:
    executor.map(
        lambda args: download_file(*args),
        datas
    )
