from datetime import datetime
import json
import os
from pathlib import Path
import re
import m3u8
import requests
from Crypto.Cipher import AES
from urllib.parse import urljoin
from Mido.variables import run_tasks

USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
OUTPUT_DIR = "/home/mohamed/Videos/Ts"
CHANNELS_FILE = "/home/mohamed/Documents/Projects/PYTHON/BeinLive/chz.json"
sess = requests.Session()
sess.headers.update({"user-agent": USER_AGENT})

with open("infos.json", "r") as f:
    infos = json.load(f)


with open("chz.json", "r") as f:
    chz = json.load(f)


def decrypt_aes128(key, iv, encrypted_data):
    # Remove '0x' prefix and convert to bytes
    iv_bytes = bytes.fromhex(iv[2:])
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def download(uri):
    try:
        response = sess.get(uri, timeout=3)
        return response.content
    except:
        return None


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
    def __init__(self, key, titre="Live"):
        self.key = key
        self.titre = titre if titre else f"Live-{self.key}"

    def online_stream(self):
        url = self.base_stream_url(True)
        if not url:
            print("not allowed !")
            return 0
        agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        setting = f'--http-user-agent="{agent}" --adaptive-use-access'
        cmd = f"""vlc --loop "{url}" {setting}"""
        os.system(cmd)

    def base_stream_url(self, force=False):
        if self.key in [f"premium{i}" for i in range(500, 521)]:
            return None
        if self.key in infos and not force:
            return infos[self.key]
        url = f"https://andrenalynrushplay.cfd/server_lookup.php?channel_id={self.key}"
        r = sess.get(url)
        data = r.json()
        serverKey = data.get("server_key")
        if serverKey == "top1/cdn":
            uri = f"https://top1.newkso.ru/top1/cdn/{self.key}/mono.m3u8"
        else:
            uri = f"https://{serverKey}new.newkso.ru/{serverKey}/{self.key}/mono.m3u8"
        infos[self.key] = uri
        with open("infos.json", "w") as inf:
            json.dump(infos, inf, indent=4)
        return uri

    def download_stream(self):
        url = self.base_stream_url(True)
        if not url:
            print("not allowed !")
            return 0
        DOC = f"{OUTPUT_DIR}/{self.titre}"
        output_file = f"{DOC}/{self.key}.ts"
        if os.path.exists(output_file):
            return 1
        print("Base URL", url)
        r = m3u8.load(url)
        stream_info = r.data["segments"]
        if len(stream_info) < 1:
            url = self.base_stream_url(True)
        if len(stream_info) < 1:
            print("New Base URL", url)
            print("Stream Vide ...")
            return 0
        for element in stream_info:
            uri = urljoin(url, element["uri"])
            stream_key = element.get("key")
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

    def live_stream(self, stop=None):
        url = self.base_stream_url(True)
        if not url:
            print("not allowed !")
            return 0
        if not stop:
            stop = "2026"
        kayn = []
        lekey = None
        output_file = f"{OUTPUT_DIR}/{self.titre}.ts"
        with open(output_file, "wb") as m3f:
            while True:
                current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
                if current_time >= stop:
                    break
                try:
                    r = m3u8.load(url)
                except:
                    url = self.base_stream_url(True)
                    print("Base URL", url.split("/")[-1])
                    continue
                stream_info = r.data["segments"]
                if len(stream_info) < 1:
                    url = self.base_stream_url(True)
                    print("New Base URL", url)
                    print("Stream Vide ...")

                for element in stream_info:
                    uri = urljoin(url, element["uri"])
                    stream_key = element.get("key")
                    k = element["uri"].rsplit(".", 1)[0]
                    ks = re.findall(r"[0-9]+", k)
                    k = "-".join(f"{int(e):04}" for e in ks)
                    if k in kayn:
                        continue
                    uri = urljoin(url, uri)
                    try:
                        data = download(uri)
                        if stream_key:
                            key_uri = stream_key["uri"]
                            iv = stream_key["iv"]
                            lekey = download(key_uri)
                            data = decrypt_aes128(lekey, iv, data)
                        m3f.write(data)
                        kayn.append(k)
                        ps = uri.split("/")[-1].split("?")[0]
                        print(
                            '>>', len(kayn), ""
                            f"{len(data) // 1000:,}kb :",
                            f"{ps:<20}",
                            end="\r"
                        )
                    except:
                        break


channelKey = "bet7789207"


def dev(channelKey):
    s = Stream(channelKey)
    s.download_stream()
    return 1


run_tasks(
    dev,
    [(f"premium{i}",) for i in range(300, 500)]
)
