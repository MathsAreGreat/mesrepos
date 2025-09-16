import os
from pathlib import Path
import re
from time import sleep
from urllib.parse import urljoin

import m3u8
import requests
from Crypto.Cipher import AES
from Mido.variables import upclear

USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
OUTPUT_DIR = "/home/mohamed/Videos/Ts"

sess = requests.Session()


def decrypt_aes128(key, iv, encrypted_data):
    # Remove '0x' prefix and convert to bytes
    iv_bytes = bytes.fromhex(iv[2:])
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def download(uri):
    try:
        response = sess.get(uri)
        return response.content
    except:
        return None


def bundle_to_m3u8(channel_key: str, server_key: str, bundle: str = "") -> str:
    """
    Convert the JavaScript BUNDLE string into the final m3u8 link.

    :param bundle: The base64 string assigned to BUNDLE in the JS.
    :param channel_key: The channel id (CHANNEL_KEY in JS).
    :param server_key: The value returned by server_lookup.php['server_key'].
    :return: The final m3u8 URL.
    """
    # # Step 1: Decode the JSON wrapper
    # parts = json.loads(base64.b64decode(bundle).decode())

    # # Step 2: Decode each base64 part
    # for k, v in parts.items():
    #     parts[k] = base64.b64decode(v).decode()

    # Step 3: Construct the final m3u8 link based on server_key
    if server_key == "top1/cdn":
        m3u8 = f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8"
    else:
        m3u8 = f"https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8"

    return m3u8


ref = "https://jxoxkplay.xyz"
# ref="https://jxoxkplay.xyz/premiumtv/daddyhd.php?id=91"
sess = requests.Session()
sess.headers.update({"user-agent": USER_AGENT, "Referer": f"{ref}/"})
infos = {}


args = os.sys.argv
prnb = 91
if len(args) > 1:
    prnb = args[-1]

# # Example usage:
u = f"{ref}/premiumtv/daddyhd.php?id={prnb}"

r = sess.get(u, timeout=10)
for k, v in re.findall(r"const ([^=]+)([^;]+)", r.text):
    k = k.lower().strip()
    if "bundle" not in k and "channel_key" not in k:
        continue
    print(k, ":", v)
    infos[k] = v.split('"')[1]

us = f"{ref}/server_lookup.php?channel_id={infos["channel_key"]}"
r = sess.get(us)
infos.update(r.json())

url = bundle_to_m3u8(**infos)

kayn = []
lekey = None

fn = Path(f"/home/mohamed/Videos/Daddylive/premium{re.sub(r"[^0-9]", r"", prnb)}.ts")

fn.parent.mkdir(parents=True, exist_ok=True)

with fn.open("wb") as m3f:
    while True:
        r = sess.get(url)
        r = m3u8.loads(r.text)
        stream_info = r.data["segments"]
        for element in stream_info:
            try:
                k = element["uri"].split("/")[-1].split(".")[0]
                if k in kayn:
                    continue
                print(f"{upclear}>", k)
                kayn.append(k)
                uri = urljoin(url, element["uri"])
                stream_key = element.get("key")
                uri = urljoin(url, uri)
                data = download(uri)
                if not data:
                    break
                if stream_key:
                    if not lekey:
                        key_uri = urljoin(url, stream_key["uri"])
                        iv = stream_key["iv"]
                        lekey = download(key_uri)
                        if not lekey:
                            break
                    data = decrypt_aes128(lekey, iv, data)
                m3f.write(data)
            except:
                break
        sleep(1)
