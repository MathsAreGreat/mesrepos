import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def ft_video(k):
    u = f"https://www.instagram.com/reel/{k}/"
    cmd = f'yt-dlp "{u}" --flat-playlist --dump-json > datas/t{k}.json'
    os.system(cmd)


def fb_video(k):
    url = f"https://www.facebook.com/reel/{k}"
    doc = "Facebook"
    dp = f"/home/mohamed/Documents/.Socials/{doc}/%(uploader)s/%(id)s.%(ext)s"
    cmd = f'yt-dlp -f b "{url}" -o "{dp}" '
    cmd += "--write-sub --sub-langs all,-live_chat --ignore-errors"
    os.system(cmd)


def ins_video(k):
    u = f"https://www.instagram.com/p/{k}/"
    doc = "Instagram"
    dp = f"/home/mohamed/Documents/.Socials/{doc}/%(uploader)s/%(id)s.%(ext)s"
    cmd = f'yt-dlp -f b "{u}" -o "{dp}" '
    cmd += "--write-sub --sub-langs all,-live_chat --ignore-errors"
    os.system(cmd)


ks = ["v550620867832754", "v585568267160594"]

uns = [f.stem for f in Path("/home/mohamed/Documents/.Socials").rglob("*mp4")]

ks = [k[1:] for k in ks if k[0] == "v"]
ks = [k for k in ks if k not in uns]

with ThreadPoolExecutor(10) as executor:
    executor.map(fb_video, ks)
