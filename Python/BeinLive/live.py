import os
import json
from time import sleep
import requests
import m3u8
from datetime import datetime
from urllib.parse import urljoin
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
        key = sess.get(playlist.keys[0].uri).content
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
        ch = channels.get(channel, channel.replace(
            "-", "prima").replace("=", "premium"))
        url = f"https://webufffit.webhd.ru/lb/{ch}/index.m3u8"

    output_file = os.path.join(OUTPUT_DIR, f"{video_name}.ts")
    if os.path.exists(output_file):
        os.remove(output_file)

    url = get_playlist_segments(referrer, url, redirect=True).replace(
        "playlist", "tracks-v1a1/mono")
    downloaded_segments = set()

    while True:
        os.system("clear")
        print(f"Channel: {channel}")
        print(f"URL: {url}")

        segments = get_playlist_segments(referrer, url)
        print(
            f":: {datetime.now().strftime('%H:%M:%S')} - {len(segments)} items!")

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
                    sleep(.5)
                    continue
            if not content:
                break
            bz = 1
            if cipher:
                print('ciphered !')
                bz += 1

            print(f"> {i} {len(content)}. {uri}")
            print(UP_CLEAR*bz, end="")
            with open(output_file, "ab") as f:
                f.write(content)
                downloaded_segments.add(uri)


if __name__ == "__main__":
    # channel = sys.argv[1] if len(sys.argv) > 1 else "eplayerTSN_1_HD"
    # main(channel, channel)
    referrer = "https://cookiewebplay.xyz/"
    ch = "premium91"
    url = f"https://azo.iosplayer.ru/lb/{ch}/index.m3u8"
    url = get_playlist_segments(referrer, url, redirect=True)
    print(url)
