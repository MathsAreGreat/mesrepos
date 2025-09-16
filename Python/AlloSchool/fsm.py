from pathlib import Path
import requests
import json
import re
from Mido.variables import run_tasks, sprint

sess = requests.Session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}
cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

parent_pdf = Path("/home/mohamed/Documents/AlloSchool")

uns = [f.stem.split("-")[-1] for f in parent_pdf.rglob("*pdf")]
uns += [f.name for f in Path("vides").rglob("*")]


def dwn(k, lien, aux):
    try:
        rs = sess.get(lien, stream=True, timeout=5)
        rsf = rs.headers.get("Content-Disposition", lien)
        fr = re.findall(r'([^"/]+).pdf', rsf)[-1]
        doc = parent_pdf / aux
        doc.mkdir(parents=True, exist_ok=True)
        fn = doc / f"{fr}-{k}.pdf"
        if fn.exists():
            return 0
        tmp_fn = doc / f"{fr}-{k}.temp.pdf"
        with open(tmp_fn, "wb") as fl:
            for chunk in rs.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fl.write(chunk)
            else:
                tmp_fn.rename(fn)
        print(f"{upclear}> {fr[:50]}..", "was downloaded successfully :)")
    except:
        print(upclear, "xx", k, "xx", "failed to download.")


def elements(k):
    output = Path(f"datas/{k}.json")
    if output.exists():
        with open(output, "r") as fl:
            vals = json.load(fl)
    else:
        u = f"https://www.alloschool.com/course/{k}"
        r = sess.get(u)
        vals = re.findall(r'http[^"]+/element/([0-9]+)', r.text)
        with open(output, "w") as fl:
            json.dump(sorted(set(vals)), fl)
    return vals


us = [
    "https://www.alloschool.com/category/2nd-degree",
    "https://www.alloschool.com/category/common-core",
    "https://www.alloschool.com/category/middle-school",
    "https://www.alloschool.com/category/1st-degree"
]

nb = 1
datas = []
uns = []


def dig(k):
    print(k)
    vals = elements(k)
    if not vals:
        return []
    print(len(vals), "items !")
    print()
    return [(e, k) for e in vals]


def get_files(k):
    u = f"https://www.alloschool.com/element/{k}"
    r = sess.get(u)
    vals = re.findall(r'http[^"\']+pdf', r.text)
    if not vals:
        Path(f"vides/{k}").touch()
        return k, []
    return k, vals


uns = [f.stem.split("-")[-1] for f in parent_pdf.rglob("*pdf")]
uns += [f.name for f in Path("vides").rglob("*")]
datas = []
while nb:
    nb = 0
    for u in sorted(us):
        if len(datas) > 100:
            break
        r = sess.get(u)
        ks = re.findall(r'http[^"\']+/course/([^"\']+)', r.text)
        ks = [
            (e,)
            for e in set(ks)
        ]
        print("=" * 60)
        raws = run_tasks(dig, ks)
        vals = {
            el: aux
            for raw in raws
            for el, aux in raw
            if el not in uns
        }
        items = [(e,) for e in vals]

        raws = run_tasks(get_files, items[:1000])
        datas = [
            (k, lien, vals[k])
            for k, liens in raws
            for lien in liens
        ]
    nb = len(datas)
    sprint(f"{nb} items to process !")
    print()
    run_tasks(dwn, datas, 20)
    datas = []
    uns = [f.stem.split("-")[-1] for f in parent_pdf.rglob("*pdf")]
    uns += [f.name for f in Path("vides").rglob("*")]
