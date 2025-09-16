import json
import os
from pathlib import Path
import re
import m3u8
import requests
from Crypto.Cipher import AES
from urllib.parse import urljoin


USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
OUTPUT_DIR = "/home/mohamed/Videos/Ts"
CHANNELS_FILE = "/home/mohamed/Documents/Projects/PYTHON/BeinLive/chz.json"
sess = requests.Session()
sess.headers.update({"user-agent": USER_AGENT})

with open("infos.json", "r") as f:
    infos = json.load(f)


def decrypt_aes128(key, iv, encrypted_data):
    # Remove '0x' prefix and convert to bytes
    iv_bytes = bytes.fromhex(iv[2:])
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def download(uri):
    response = sess.get(uri)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(
            "Failed to download the video segment. Status code:", response.status_code
        )


def concatize(*files, o: str | Path = "output", ex: str = "ts"):
    filenames = "|".join(files[:])
    cmd = f'ffmpeg -i "concat:{filenames}" -c copy "{o}.{ex}"'
    os.system(cmd)
    msg = f"* {o}.{ex} Created !"
    print(f"{msg:<40}")


def combine_vids(pt):
    try:
        p = Path(pt)
    except:
        return 0
    nb = 0
    for v_out in p.rglob("*"):
        if v_out.is_file():
            continue
        fs = [
            f"{f}"
            for f in v_out.glob("*.part")
        ]
        if fs:
            nb += 1
            continue
        fn = v_out.with_suffix(f"{v_out.suffix}.mp4")
        if not fn.exists():
            fs = [
                f"{f}"
                for f in v_out.glob("*.ts")
            ]
            fs = sorted(
                fs,
                key=lambda e: re.sub(
                    r"[^0-9]",
                    r"",
                    e.rsplit(".", 1)[0]
                ).zfill(20)
            )
            ph = 0
            j = 1
            NBR = 900
            while len(fs) > NBR:
                i = 0
                ph += 1
                while fs:
                    i += 1
                    concatize(*fs[:NBR], o=f"{v_out}_{j}_{i}")
                    fs = fs[NBR:]
                fs = [
                    f"{v_out}_{j}_{n+1}.ts"
                    for n in range(i)
                ]
                j += 1
            concatize(*fs, o=v_out, ex="mp4")
            if ph:
                for f in fs:
                    os.remove(f)
                    msg = f"** Removing {f}"
                    print(f"{msg:<40}")
    msg = "> All is Done !"
    print(f"{msg:<40}")
    return nb


class Stream:
    def __init__(self, key, titre=None):
        self.key = key
        self.titre = titre if titre else f"Live-{self.key}"

    def base_stream_url(self):
        u = f"https://webufffit.mizhls.ru/lb/{self.key}/index.m3u8"
        referrer = "https://cookiewebplay.xyz/"
        sess.headers.update({"Referer": referrer})
        r = sess.get(u)
        r = m3u8.loads(r.text)
        pl = max(r.data["playlists"],
                 key=lambda e: e["stream_info"]["bandwidth"])
        url = pl["uri"]
        infos[self.key] = url
        with open("infos.json", "w") as inf:
            json.dump(infos, inf)
        print(url)
        return url

    def download_stream(self):
        DOC = f"{OUTPUT_DIR}/{self.titre}"
        url = self.base_stream_url(True)
        print("Base URL", url)
        r = m3u8.load(url)
        stream_info = r.data["segments"]
        if len(stream_info) < 1:
            url = self.base_stream_url(True)
        if len(stream_info) < 1:
            print("New Base URL", url)
            print("Stream Vide ...")
            return 0
        stream_key = stream_info[0].get("key")
        for element in stream_info:
            uri = urljoin(url, element["uri"])
            k = uri.split(self.key)[-1].rsplit(".", 1)[0]
            ks = re.findall(r"[0-9]+", k)
            k = "-".join(f"{int(e):04}" for e in ks)
            output_file = f"{DOC}/{self.key}-{k}.ts"
            if os.path.exists(output_file):
                continue
            os.makedirs(DOC, exist_ok=True)
            uri = urljoin(url, uri)
            try:
                data = download(uri)
                print(uri)
                if stream_key:
                    key_uri = stream_key["uri"]
                    iv = stream_key["iv"]
                    key = download(key_uri)
                    data = decrypt_aes128(key, iv, data)
                with open(output_file, "wb") as f:
                    f.write(data)
                    print(f"Downloaded stream saved to {output_file}")
                    break
            except:
                continue

    def live_stream(self):
        kayn = []
        output_file = f"{OUTPUT_DIR}/{self.titre}.ts"
        with open(output_file, "wb") as m3f:
            url = self.base_stream_url()
            while True:
                r = sess.get(url)
                r = m3u8.loads(r.text)
                stream_info = r.data["segments"]
                if len(stream_info) < 1:
                    url = self.base_stream_url()
                    print("New Base URL", url)
                    print("Stream Vide ...")
                stream_key = stream_info[0].get("key")
                for element in stream_info:
                    uri = urljoin(url, element["uri"])
                    k = element["uri"].rsplit(".", 1)[0]
                    ks = re.findall(r"[0-9]+", k)
                    k = "-".join(f"{int(e):04}" for e in ks)
                    if k in kayn:
                        continue
                    uri = urljoin(url, uri)
                    data = download(uri)
                    print(uri)
                    if stream_key:
                        key_uri = stream_key["uri"]
                        iv = stream_key["iv"]
                        key = download(key_uri)
                        data = decrypt_aes128(key, iv, data)
                    m3f.write(data)
                    kayn.append(k)
                    print(f"Downloaded {output_file}")


# s = Stream("beINAR2", "RV VS ESP")
# s.live_stream()

# end_time = datetime.now().strftime("%Y%m%d-%H%M%S")

# end_time = "20241004-214254"

# while True:
#     s.download_stream()
#     if datetime.now().strftime("%Y%m%d-%H%M%S") > end_time:
#         break

# pt = "/home/mohamed/Videos/Ts"
# combine_vids(pt)

# for i in range(100):
#     s = Stream(f"premium{i+100}", "RM VS CV")
#     try:
#         s.download_stream()
#     except:
#         pass


# key = "eplayerTSN_1_HD"
# u = f"https://lovecdn.ru/maxsport.php?stream=beINAR2"
# referrer = f"https://cookiewebplay.xyz/"
# sess.headers.update({"Referer": u})

# r = sess.get(u)
# t = re.findall(r'<iframe.+src="([^"]+)', r.text)[0]
# sess.headers.update({"Referer": t})

# video_url = t.replace("embed.html", "tracks-v1/index.fmp4.m3u8")
# audio_url = t.replace("embed.html", "tracks-a1/index.fmp4.m3u8")

# output_file = "/home/mohamed/Videos/TS/Items/beINAR2.mp4"


# # Open VLC with videsx1neweo and audio streams
# subprocess.run(["mpv", "--audio-file="+audio_url, video_url])


key = "premium91"
# # https://esx1new.iosplayer.ru/esx1/primanovasport2/mono.m3u8
u = f"https://azo.iosplayer.ru/lb/{key}/index.m3u8"
referrer = f"https://cookiewebplay.xyz/maxsport.php?id={key}"
sess.headers.update({"Referer": referrer})
r = sess.get(u)
print(r.url)
r = m3u8.loads(r.text)
print(r.data)
