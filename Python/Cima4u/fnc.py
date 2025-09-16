import re
from pathlib import Path

from Mido.variables import download_m3u8_with_aria2c, get_m3u8, monhtml

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": "https://www.cimaa4u.com/",
}

# u = "https://a2.file-hd.com/hls2/02/00010/qc3pjombbbjh_,l,h,.urlset/master.m3u8?t=cbqcZDIpTRIWuihWS9AMyhm_ZveUgUXL-jiZOhnA5L8&s=1747345631&e=10800&f=52896&i=105.157&sp=2500"
# t = "live"
# c = "key"
# r = None
# dt = (
#     u,
#     f"{t}.[%(height)sp].({c}).mp4",
#     r
# )


# plus = "--downloader ffmpeg --hls-use-mpegts"
# download_m3u8_with_aria2c(*dt, plus=plus)


def dlink(u):
    p = get_m3u8(u, headers)
    us = [e for e in re.findall(r"http[^\"']+", p) if "m3u8" in e]
    return us[0]


def infos(u):
    soup = monhtml(u)
    shortlink = soup.select_one("[rel='shortlink']").get("href")
    *_, key = shortlink.split("=")
    ts = soup.select_one(".SingleContent h1").text.split(" ")
    titre = ".".join(e for e in ts if re.search(r"[0-9a-z]", e, flags=re.IGNORECASE))
    return key, titre


def dserver(k):
    u = f"https://cimaa4u.show/?p={k}&wat=1"
    soup = monhtml(u)
    return soup.select_one(".sever_link").get("data-embed")


u = "https://cimaa4u.show/%d9%81%d9%8a%d9%84%d9%85-the-baby-in-the-basket-2025-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
u = "https://www.cimaa4u.com/%D9%81%D9%8A%D9%84%D9%85-indrani-epic-1-dharam-vs-karam-2024-%D9%85%D8%AA%D8%B1%D8%AC%D9%85/?wat=1"


def dwn(u):
    k, t = infos(u)
    sr = dserver(k)
    dl = dlink(sr)

    print(dl)

    r = None
    dt = (dl, f"{t}.[%(height)sp].({k}).mp4", r)

    download_m3u8_with_aria2c(*dt)


sp = monhtml(u)

f = ".".join(e.title() for e in u.split("/")[-2].split("-") if "%" not in e)

vu = sp.select_one(".sever_link").get("data-embed")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": vu,
}
r = get_m3u8(vu, headers=headers)

dd = re.findall(r'file:"([^"]+)"', r)

uri = max(dd)

pl = Path("/home/mohamed/Videos/Movies")

fl = pl / f"[Cima4u].[{f}].[%(height)s].%(ext)s"

download_m3u8_with_aria2c(uri, fl, vu)
