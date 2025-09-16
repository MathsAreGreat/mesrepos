from playwright.sync_api import sync_playwright

from urllib.parse import urljoin

import requests

from Crypto.Cipher import AES
import m3u8

playwright = sync_playwright().start()
agent = "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"

mts = []

sess = requests.session()
referrer = ""

ref = "https://www.shoot4live.com"
base_url = "https://a3.bein-match.tech/broadcast/0DIbKajGrKXClFyPfY119A/1745768562/1745768301/1/multi-09.m3u8"

sess.headers = {
    "user-agent": agent,
    "Referer": ref
}

rs = sess.get(base_url, stream=True)
r = m3u8.loads(rs.text)

stream_info = r.data["segments"]

segs = [
    (element["uri"], element.get("key"))
    for element in stream_info
]
# Segments info
segments = [
    {"uri": uri, "key_uri": key["uri"], "iv": key["iv"]}
    for uri, key in segs
    if key
]

# Cache for keys
keys_cache = {}

# Helper function to download a key


def get_key(key_uri):
    if key_uri not in keys_cache:
        key_base_url = urljoin(base_url, key_uri)
        print(f"Downloading key {key_uri}...")
        r = sess.get(key_base_url)
        keys_cache[key_uri] = r.content
    return keys_cache[key_uri]


# Start downloading and decrypting
with open("output.ts", "wb") as outfile:
    for seg in segments:
        segment_url = urljoin(base_url, seg["uri"])
        key_uri = seg["key_uri"]
        iv_hex = seg["iv"]

        # Download segment
        print(f"Downloading {seg['uri']}...")
        r = sess.get(segment_url)
        encrypted_data = r.content

        # Get decryption key
        key = get_key(key_uri)

        # Prepare AES decryptor
        iv = bytes.fromhex(iv_hex[2:])  # remove '0x' and convert
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Make sure the data length is a multiple of 16
        padding = 16 - (len(encrypted_data) % 16)
        if padding != 16:
            encrypted_data += b'\x00' * padding  # pad with null bytes

        # Decrypt
        decrypted_data = cipher.decrypt(encrypted_data)

        # Write decrypted segment
        outfile.write(decrypted_data)

print("Download and decryption finished!")
