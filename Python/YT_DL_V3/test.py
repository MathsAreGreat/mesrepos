from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re


def tolrc(f):
    with Path(f).open("r", encoding="utf8") as e:
        infos = e.read().split("\n\n")
    start, *datas = infos
    datas = [line.split("\n") for line in datas if line.strip()]
    datas = [[gad(i, e) for i, e in enumerate(line)] for line in datas]
    datas = [(t, " ".join(s)) for t, *s in datas]
    datas = [f"[{t}] {s}" for t, s in datas]
    return re.findall(r"Language:([^\n]+)", start), datas


def gad(i, line):
    if i:
        return re.sub(r"\s+", r" ", line)
    nbr = 2
    line = line.split(" ")[0]
    r = line.split(":")
    if len(r) > nbr:
        h, m, s = r
        if h == "00":
            line = f"{m}:{s}"
    return line


def lrci(f):
    item, info = tolrc(f)
    subs = "\n".join(info)
    fn = f.split("/")[-1]
    name, *eng = fn.replace(".vtt", "").rsplit(".", 1)
    if item:
        eng = item[0].strip()
    elif not eng:
        eng = "ar"
    else:
        eng = eng[0]
    lg = eng.title()
    spath = Path(f"/home/mohamed/Documents/Youtube/Subs/Lrc/{lg}")
    nw = spath / f"{name}.lrc"
    if nw.exists():
        return 0
    spath.mkdir(parents=True, exist_ok=True)
    with nw.open("w", encoding="utf-8") as e:
        e.write(subs)
    print(">", name)
    return 1


def gad_lrc(pth):
    to = Path("/home/mohamed/Documents/Youtube/Subs/Vtt")
    for f in Path(pth).rglob("*.vtt"):
        name = re.sub(r"[\(\)]", r"", f.name.split(" ")[-1])
        print("->", name)
        fv = to / name
        if fv.is_file():
            fv.unlink()
        f.rename(fv)

    mesfiles = [str(f) for f in to.rglob("*.vtt")]

    if mesfiles:
        print(f"{len(mesfiles)} Subtitles")
        with ThreadPoolExecutor(10) as executor:
            executor.map(lrci, mesfiles)


pth = "/home/mohamed/Videos/Youtube"
gad_lrc(pth)
