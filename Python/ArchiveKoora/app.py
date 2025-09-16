import re
from pathlib import Path

from Mido.variables import download_m3u8_with_aria2c, monhtml

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}

pt = "/home/mohamed/Videos/Matches"

uns = [f.stem.split(".")[-1][1:-1] for f in Path(pt).rglob("*.mp4")]


def formate(src):
    if "ok.ru" in src:
        ID = src.split("/")[-1].split("?")[0]
        u = f"https://ok.ru/videoembed/{ID}"
        ref = "https://ok.ru/"
        return (ref, ID, u)
    if "smoothpre" in src:
        return ("smoothpre", src.split("/")[-1].split("?")[0])
    if "dailymotion" in src:
        ID = src.split("=")[-1]
        u = f"https://www.dailymotion.com/video/{ID}"
        ref = "https://www.dailymotion.com/"
        return (ref, ID, u)
    return None


us = [
    "https://www.footarchives.com/2025/08/2025_27.html",
]
infos = [
    # (
    #     "https://www.dailymotion.com/=x9kktk4",
    #     "PSG VS Inter Milan First Half [Final 2025]",
    # ),
    # (
    #     "https://www.dailymotion.com/=x9kkvri",
    #     "PSG VS Inter Milan Ceromony [Final 2025]",
    # ),
]
if infos:
    datas = [
        (
            *formate(k),
            ".".join(
                e
                for e in re.sub(r"[^a-z0-9]", r" ", t, flags=re.IGNORECASE).split(" ")
                if e
            ),
        )
        for k, t in infos
    ]

# print(datas)


# datas = [(u, f"{t}.({k})") for k, u, t in infos]

datas = []
for u in us:
    soup = monhtml(u, headers=headers)
    ts = re.sub(r"[/\.]", r" ", soup.h1.text).split(" ")
    t = ".".join(e for e in ts if e)
    iframes = [formate(link["src"]) for link in soup.find_all("iframe", src=True)]

    datas += [(*dd, f"[H-{i}].{t}") for i, dd in enumerate(iframes, start=1) if dd]


dirc = Path("/home/mohamed/Videos/Matches/ArchKoora")
datas = [
    (u, dirc / f"{t}.[%(height)sp].({c}).mp4", r)
    for r, c, u, t in datas
    if c not in uns
]

for dt in datas:
    download_m3u8_with_aria2c(*dt)
