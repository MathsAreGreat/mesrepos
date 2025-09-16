import os
import re
import json
from time import sleep
import requests
import m3u8
from datetime import datetime
from urllib.parse import urljoin, unquote
from Crypto.Cipher import AES


# Constants
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
OUTPUT_DIR = "/home/mohamed/Videos/Ts"
CHANNELS_FILE = "/home/mohamed/Documents/Projects/PYTHON/BeinLive/chz.json"

# ANSI escape codes for terminal manipulation
CURSOR_UP = "\033[1A"
CLEAR_LINE = "\x1b[2K"
UP_CLEAR = CURSOR_UP + CLEAR_LINE
# Setup
os.makedirs(OUTPUT_DIR, exist_ok=True)
sess = requests.Session()
sess.headers.update({"user-agent": USER_AGENT})


def get_aes_cipher(key, iv):
    return AES.new(key, AES.MODE_CBC, iv) if key and iv else None


def download_segment(referrer, base_url, segment_uri, cipher):
    sess.headers.update({"Referer": referrer})
    url = urljoin(base_url, segment_uri)
    response = sess.get(url, stream=True, timeout=20)

    if response.status_code == 200:
        content = response.content
        return cipher.decrypt(content) if cipher else content
    return None


def get_playlist_segments(referrer, base_url, redirect=False):
    sess.headers.update({"Referer": referrer})
    if redirect:
        return sess.get(base_url, stream=True, allow_redirects=True).url

    response = sess.get(base_url, stream=True)
    playlist = m3u8.loads(response.text)
    cipher = None
    if not cipher and playlist.keys and playlist.keys[0]:
        myurl = urljoin(base_url, playlist.keys[0].uri)
        key = sess.get(myurl).content
        iv = int(playlist.keys[0].iv, 16).to_bytes(16, "big")
        cipher = get_aes_cipher(key, iv)

    return [(referrer, response.url, seg.uri, cipher) for seg in playlist.segments]


def main(channel, video_name="Live"):
    with open(CHANNELS_FILE, "r") as f:
        channels = json.load(f)

    if channel.endswith("teri"):
        ch = channel.split("teri")[0]
        url = f"https://live.simogames.pro/hls/yallalive{ch}/index.m3u8"
        referrer = "https://yallateri.com"
    else:
        referrer = "https://ilovetoplay.xyz"
        ch = channels.get(
            channel, channel.replace("-", "prima").replace("=", "premium")
        )
        url = f"https://webufffit.webhd.ru/lb/{ch}/index.m3u8"

    output_file = os.path.join(OUTPUT_DIR, f"{video_name}.ts")
    if os.path.exists(output_file):
        os.remove(output_file)

    url = get_playlist_segments(referrer, url, redirect=True).replace(
        "playlist", "tracks-v1a1/mono"
    )
    downloaded_segments = set()

    while True:
        os.system("clear")
        print(f"Channel: {channel}")
        print(f"URL: {url}")

        segments = get_playlist_segments(referrer, url)
        print(f":: {datetime.now().strftime('%H:%M:%S')} - {len(segments)} items!")

        for i, (ref, base, uri, cipher) in enumerate(segments, start=1):
            if uri in downloaded_segments:
                print(f"XX {i}. {uri}")
                print(UP_CLEAR, end="")
                sleep(1)
                continue
            content = None
            for _ in range(5):
                try:
                    content = download_segment(ref, base, uri, cipher)
                    if content:
                        break
                except:
                    sleep(0.5)
                    continue
            if not content:
                break
            bz = 1
            if cipher:
                print("ciphered !")
                bz += 1

            print(f"> {i} {len(content)}. {uri}")
            print(UP_CLEAR * bz, end="")
            with open(output_file, "ab") as f:
                f.write(content)
                downloaded_segments.add(uri)


def choose(streamUrl, ch, key):
    sess = requests.session()
    referrer = streamUrl.rsplit("/", 1)[0]
    sess.headers = {"Referer": referrer}
    streamUrl = sess.post(streamUrl, data={"ch": ch, "key": key})
    streamUrl = streamUrl.json()
    streamUrl = unquote(re.sub(r"(.{1,2})", r"%\1", streamUrl["url"]))
    return referrer, streamUrl


def liveit(referrer, ch, key):
    referrer, url = choose(referrer, ch, key)
    print(f"> {ch=}")
    print(f"> {key=}")
    print(f"> {url=}")
    print(f"> {referrer=}")
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    http = f'--http-referrer="{referrer}"'
    setting = f'--http-user-agent="{agent}" --adaptive-use-access'
    cmd = f"""vlc --loop --play-and-exit "{url}" {http} {setting}"""
    os.system(cmd)


c, k = "1", "1"
ch = f"bein{c:>02}"
if re.search(r"[a-z]", c):
    ch = c
key = f"key{k:>03}"
doom = "https://4k.kooora4lives.net"
referer, b_uri = choose(f"{doom}/token.php", ch, key)
sess.headers.update({"Referer": referer})
print(f"> {ch = }")
print(f"> {key = }")
print(f"> {b_uri = }")
print(f"> {referer = }")

downloaded_segments = set()
output_file = os.path.join(OUTPUT_DIR, "live.ts")
while True:
    segments = get_playlist_segments(referer, b_uri)
    print(f":: {datetime.now().strftime('%H:%M:%S')} - {len(segments)} items!")

    for i, (ref, base, uri, cipher) in enumerate(segments, start=1):
        if uri in downloaded_segments:
            print(f"XX {i}. {uri}")
            print(UP_CLEAR, end="")
            sleep(1)
            continue
        content = None
        for _ in range(5):
            try:
                content = download_segment(ref, base, uri, cipher)
                if content:
                    break
            except:
                sleep(0.5)
                continue
        if not content:
            break
        bz = 1
        if cipher:
            print("ciphered !")
            bz += 1

        print(f"> {i} {len(content)}. {uri}")
        print(UP_CLEAR * bz, end="")
        with open(output_file, "ab") as f:
            f.write(content)
            downloaded_segments.add(uri)
