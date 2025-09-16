import re
import m3u8
from pathlib import Path
from urllib.parse import urljoin

import requests

from Mido.variables import download_m3u8_with_aria2c, print

sess = requests.Session()
referrer = "https://snrt.player.easybroadcast.io/"

sess.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Referer": referrer,
}

token_url = "https://token.easybroadcast.io/all"


def get_token(key):
    u = f"https://cdn.live.easybroadcast.io/abr_corp/{key}/playlist_dvr.m3u8"
    r = sess.get(f"{token_url}?url={u}")

    lien = f"https://cdn.live.easybroadcast.io/abr_corp/{key}/corp/{key}_480p/chunks_dvr.m3u8?{r.text}"

    r = m3u8.load(lien)

    return r.data["segments"]


key = "73_aloula_w1dqfwm"
segs = get_token(key)
for seg in segs:
    print(seg["program_date_time"].strftime("%Y-%m-%d-%H-%M-%S"))
