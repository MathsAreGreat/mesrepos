import os
from concurrent.futures import ThreadPoolExecutor


def ins_video(k):
    u = f"https://www.instagram.com/reel/{k}/"
    doc = "Instagram"
    dp = f"/home/mohamed/Documents/.Socials/{doc}/%(uploader)s/%(id)s.%(ext)s"
    cmd = f'yt-dlp -f b "{u}" -o "{dp}" '
    cmd += "--write-sub --sub-langs all,-live_chat --ignore-errors"
    os.system(cmd)


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


def twitter_video(k):
    url = f"https://x.com/user/status/{k}"
    doc = "Twitter"
    dp = f"/home/mohamed/Documents/.Socials/{doc}/%(uploader)s/%(id)s.%(ext)s"
    cmd = f'yt-dlp -f "bestvideo+bestaudio/best" "{url}" -o "{dp}" '
    cmd += "--write-sub --sub-langs all,-live_chat --ignore-errors"
    os.system(cmd)


ks = "1913978463478071662", "1914078105041330259"

with ThreadPoolExecutor(10) as executor:
    datas = executor.map(
        twitter_video,
        ks
    )
